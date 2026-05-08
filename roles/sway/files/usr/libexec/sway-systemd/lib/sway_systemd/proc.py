import logging
import socket
import struct
from typing import Optional

LOG = logging.getLogger("assign-cgroups.proc")

def get_cgroup(pid: int) -> Optional[str]:
    """
    Get cgroup identifier for the process specified by pid.
    Assumes cgroups v2 unified hierarchy.
    """
    try:
        with open(f"/proc/{pid}/cgroup", "r") as file:
            cgroup = file.read()
        return cgroup.strip().split(":")[-1]
    except OSError:
        LOG.exception("Error getting cgroup info")
    return None

def get_pid_by_socket(sockpath: str) -> int:
    """
    getsockopt (..., SO_PEERCRED, ...) returns the following structure
    struct ucred
    {
      pid_t pid; /* s32: PID of sending process.  */
      uid_t uid; /* u32: UID of sending process.  */
      gid_t gid; /* u32: GID of sending process.  */
    };
    See also: socket(7), unix(7)
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(sockpath)
        ucred = sock.getsockopt(
            socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("iII")
        )
    pid, _, _ = struct.unpack("iII", ucred)
    return pid
