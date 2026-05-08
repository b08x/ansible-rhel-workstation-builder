import logging
import sys
from typing import Optional

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Callable
else:
    from typing import Callable

LOG = logging.getLogger("assign-cgroups.sway_utils")

def create_x11_pid_getter() -> Callable[[int], int]:
    """Create fallback X11 PID getter.

    Sway 1.6.1/wlroots 0.14 can use XRes to get the PID for Xwayland apps from
    the server and won't ever reach that. The fallback is preserved for
    compatibility with i3 and earlier versions of Sway.
    """
    # pylint: disable=import-outside-toplevel
    # Defer Xlib import until we really need it.
    from Xlib import X
    from Xlib.display import Display

    try:
        # requires python-xlib >= 0.30
        from Xlib.ext import res as XRes
    except ImportError:
        XRes = None

    display = Display()

    def get_net_wm_pid(wid: int) -> int:
        """Get PID from _NET_WM_PID property of X11 window"""
        window = display.create_resource_object("window", wid)
        net_wm_pid = display.get_atom("_NET_WM_PID")
        pid = window.get_full_property(net_wm_pid, X.AnyPropertyType)

        if pid is None:
            raise RuntimeError("Failed to get PID from _NET_WM_PID")
        return int(pid.value.tolist()[0])

    def get_xres_client_id(wid: int) -> int:
        """Get PID from X server via X-Resource extension"""
        res = display.res_query_client_ids(
            [{"client": wid, "mask": XRes.LocalClientPIDMask}]
        )
        for cid in res.ids:
            if cid.spec.client > 0 and cid.spec.mask == XRes.LocalClientPIDMask:
                for value in cid.value:
                    return value
        raise RuntimeError("Failed to get PID via X-Resource extension")

    if XRes is None or display.query_extension(XRes.extname) is None:
        LOG.warning(
            "X-Resource extension is not supported. "
            "Process identification for X11 applications will be less reliable."
        )
        return get_net_wm_pid

    ver = display.res_query_version()
    LOG.info(
        "X-Resource version %d.%d",
        ver.server_major,
        ver.server_minor,
    )
    if (ver.server_major, ver.server_minor) < (1, 2):
        return get_net_wm_pid

    return get_xres_client_id
