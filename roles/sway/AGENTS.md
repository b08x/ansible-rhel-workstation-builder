# SWAY ROLE KNOWLEDGE BASE

Sway Wayland compositor configuration with 29 automation scripts and theme management.

## WHERE TO LOOK
| Task | File | Notes |
|------|------|-------|
| **29 Scripts** | `files/usr/share/sway/scripts/` | Waybar, screenshots, recorder, notifications |
| **Theme System** | `files/usr/share/sway/themes/` | Nordic, Matcha variants (5 themes) |
| **Sway Config** | `files/usr/share/sway/config.d/` | 13 config snippets (modular) |
| **Systemd Integration** | `files/usr/libexec/sway-systemd/` | Session management, cgroup assignment |
| **Package Lists** | `vars/Fedora.yml` | 100-line Sway/Wayland package definitions |
| **Main Tasks** | `tasks/main.yml` | 128 lines, orchestrates file deployment |

## CONVENTIONS
- **Script-Based Automation**: Shell scripts for user workflows (not systemd units)
- **Modular Config**: Split config into `config.d/` snippets (keybinds, outputs, bar, etc.)
- **Theme Structure**: `themes/<theme-name>/sway.conf` for color schemes
- **System-Wide Deploy**: Files to `/usr/share/sway/` (not user home)
- **Wayland-Only**: No X11 fallback, assumes Wayland session

## UNIQUE STYLES
- **Script Density**: 29 scripts (highest script count in project)
- **User Workflow Focus**: Screenshot, screen recording, notifications, waybar toggles
- **Theme System**: 5 color schemes (Nordic, Matcha variants) with consistent structure
- **Systemd Integration**: `sway-systemd` for proper session lifecycle management
- **Hybrid Desktop**: Often deployed alongside GNOME (use Sway for tiling workflows)

## CONSOLIDATION TARGETS
- **Script Organization**: Categorize scripts (media/, notifications/, system/, bar/)
- **Variable Consolidation**: Merge Sway packages into `common/vars/packages.yml`
- **Template Scripts**: Convert hardcoded paths in scripts to Jinja2 templates
- **Theme Management**: Consider dynamic theme generation from color variables

## NOTES
- **130 Files**: Second largest role (after audio)
- **Wayland Requirement**: Fails on X11-only systems (no validation check)
- **Waybar Dependency**: Scripts assume waybar installed and running
- **GNOME Integration**: Can run alongside GNOME (switch via login manager)
- **User Scripts**: Deployed system-wide but typically invoked per-user via keybinds
- **Testing**: `swaymsg -t get_tree` validates config, `MOD+Return` opens terminal
