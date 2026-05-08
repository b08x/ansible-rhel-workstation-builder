import logging
import asyncio
from functools import lru_cache
from typing import Optional

from dbus_next import Variant
from dbus_next.aio import MessageBus
from dbus_next.errors import DBusError
from i3ipc import Event
from i3ipc.aio import Con, Connection
from psutil import Process
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from .proc import get_cgroup, get_pid_by_socket
from .systemd import (
    escape_app_id, 
    SD_SLICE_FORMAT, 
    SD_UNIT_FORMAT, 
    LAUNCHER_APP_CGROUPS
)
from .sway_utils import create_x11_pid_getter

LOG = logging.getLogger("assign-cgroups.manager")

SD_BUS_NAME = "org.freedesktop.systemd1"
SD_OBJECT_PATH = "/org/freedesktop/systemd1"

class CGroupHandler:
    """Main logic: handle i3/sway IPC events and start systemd transient units."""

    def __init__(self, bus: MessageBus, conn: Connection):
        self._bus = bus
        self._conn = conn

    @property
    @lru_cache(maxsize=1)
    def get_x11_window_pid(self) -> Optional[callable]:
        """On-demand initialization of X11 PID getter"""
        try:
            return create_x11_pid_getter()
        # pylint: disable=broad-except
        except Exception as exc:
            LOG.warning("Failed to create X11 PID getter: %s", exc)
            return None

    async def connect(self):
        """asynchronous initialization code"""
        # pylint: disable=attribute-defined-outside-init
        introspection = await self._bus.introspect(SD_BUS_NAME, SD_OBJECT_PATH)
        self._sd_proxy = self._bus.get_proxy_object(
            SD_BUS_NAME, SD_OBJECT_PATH, introspection
        )
        self._sd_manager = self._sd_proxy.get_interface(
            f"{SD_BUS_NAME}.Manager")

        self._compositor_pid = get_pid_by_socket(self._conn.socket_path)
        self._compositor_cgroup = get_cgroup(self._compositor_pid)
        assert self._compositor_cgroup is not None
        LOG.info("compositor:%s %s", self._compositor_pid,
                 self._compositor_cgroup)

        self._conn.on(Event.WINDOW_NEW, self._on_new_window)
        return self

    def get_pid(self, con: Con) -> Optional[int]:
        """Get PID from IPC response (sway), X-Resource or _NET_WM_PID (i3)"""
        if isinstance(con.pid, int) and con.pid > 0:
            return con.pid

        if con.window is not None and self.get_x11_window_pid is not None:
            return self.get_x11_window_pid(con.window)

        return None

    def cgroup_change_needed(self, cgroup: Optional[str]) -> bool:
        """Check criteria for assigning current app into an isolated cgroup"""
        if cgroup is None:
            return False
        for launcher in LAUNCHER_APP_CGROUPS:
            if launcher in cgroup:
                return True
        return cgroup == self._compositor_cgroup

    @retry(
        reraise=True,
        retry=retry_if_exception_type(DBusError),
        stop=stop_after_attempt(3),
    )
    async def assign_scope(self, app_id: str, proc: Process):
        """
        Assign process (and all unassigned children) to the
        app-{app_id}.slice/app{app_id}-{pid}.scope cgroup
        """
        escaped_app_id = escape_app_id(app_id)
        sd_slice = SD_SLICE_FORMAT.format(app_id=escaped_app_id)
        sd_unit = SD_UNIT_FORMAT.format(app_id=escaped_app_id, unique=proc.pid)
        
        pids = [proc.pid] + [
            x.pid
            for x in proc.children(recursive=True)
            if self.cgroup_change_needed(get_cgroup(x.pid))
        ]

        await self._sd_manager.call_start_transient_unit(
            sd_unit,
            "fail",
            [["PIDs", Variant("au", pids)], ["Slice", Variant("s", sd_slice)]],
            [],
        )
        LOG.debug(
            "window %s successfully assigned to cgroup %s/%s", app_id, sd_slice, sd_unit
        )

    async def _on_new_window(self, _: Connection, event: Event):
        """window:new IPC event handler"""
        con = event.container
        app_id = con.app_id if con.app_id else con.window_class
        try:
            pid = self.get_pid(con)
            if pid is None:
                LOG.warning("Failed to get pid for %s", app_id)
                return
            proc = Process(pid)
            cgroup = get_cgroup(proc.pid)
            if app_id is None:
                app_id = proc.name()
            LOG.debug("window %s(%s) cgroup %s", app_id, proc.pid, cgroup)
            if self.cgroup_change_needed(cgroup):
                await self.assign_scope(app_id, proc)
        except Exception as exc:
            LOG.error("Failed to modify cgroup for %s: %s", app_id, exc)

async def main_async():
    """Async entrypoint"""
    try:
        bus = await MessageBus().connect()
        conn = await Connection(auto_reconnect=False).connect()
        await CGroupHandler(bus, conn).connect()
        await conn.main()
    except DBusError as exc:
        LOG.error("DBus connection error: %s", exc)
    except (ConnectionError, EOFError) as exc:
        LOG.error("Sway IPC connection error: %s", exc)
