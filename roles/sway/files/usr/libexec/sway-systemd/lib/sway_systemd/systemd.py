import re

SD_SLICE_FORMAT = "app-{app_id}.slice"
SD_UNIT_FORMAT = "app-{app_id}-{unique}.scope"
SD_UNIT_ESCAPE_RE = re.compile(r"[^\w:.\\]", re.ASCII)

# Ids of known launcher applications that are not special surfaces. When the app is
# started using one of those, it should be moved to a new cgroup.
# Launcher should only be listed here if it creates cgroup of its own.
LAUNCHER_APPS = ["nwgbar", "nwgdmenu", "nwggrid", "onagre"]

def escape_app_id(app_id: str) -> str:
    """Escape app_id for systemd APIs.

    The "unit prefix" must consist of one or more valid characters (ASCII letters,
    digits, ":", "-", "_", ".", and "\\"). The total length of the unit name including
    the suffix must not exceed 256 characters. [systemd.unit(5)]

    We also want to escape "-" to avoid creating extra slices.
    """

    def repl(match):
        return "".join([f"\\x{x:02x}" for x in match.group().encode()])

    return SD_UNIT_ESCAPE_RE.sub(repl, app_id)

LAUNCHER_APP_CGROUPS = [
    SD_SLICE_FORMAT.format(app_id=escape_app_id(app)) for app in LAUNCHER_APPS
]
