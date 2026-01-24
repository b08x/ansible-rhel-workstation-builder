# AUDIO ROLE KNOWLEDGE BASE

Low-latency audio workstation with PipeWire/JACK, realtime tuning, and 97 application desktop files.

## WHERE TO LOOK
| Task | File | Notes |
|------|------|-------|
| **97 Desktop Files** | `files/home/local/share/applications/` | User-specific app launchers (unorganized) |
| **Realtime Tuning** | `tasks/tuning.yml` | 150 lines, IRQ balance, CPU governor, limits |
| **Package Installation** | `tasks/packages.yml` | Distro-specific audio packages |
| **PipeWire Config** | `templates/pipewire/`, `templates/wireplumber/` | JACK integration, buffer sizes, Lua configs |
| **JACK Control** | `templates/etc/default/jack_control.j2` | JACK daemon settings |
| **Distro Variables** | `vars/Fedora.yml`, `vars/RedHat.yml` | Audio packages, buffer defaults, Audinux COPR |

## CONVENTIONS
- **User-Specific Deploy**: Desktop files to `~/.local/share/applications/` (not `/usr/share/`)
- **Audio Stack Selection**: `audio_system: "pipewire"` (default) or `"pulseaudio_jack"` (legacy)
- **Realtime Kernel**: Assumes RT kernel available (no validation)
- **Audio Group**: Adds users to `audio` and `realtime` groups for device access
- **Buffer Configuration**: `audio_buffer_size` variable (default 1024 samples)
- **IRQ Balance**: Disables `irqbalance` for low-latency (use caution)

## UNIQUE STYLES
- **97 Desktop Files**: Largest static file count in project (no organization by category)
- **Rationale**: User-specific installs avoid conflicts with system packages
- **PipeWire/JACK Hybrid**: PipeWire with JACK API compatibility layer
- **Distro Split**: Fedora uses `pipewire-jack-audio-connection-kit`, RHEL differs
- **Professional Audio Focus**: Optimized for DAW/music production workflows
- **Lua Configuration**: WirePlumber configs use Jinja2-templated Lua scripts
- **COPR Integration**: Audinux stable-audio repo for bleeding-edge packages
- **Realtime Tuning**: Custom `realtime-modified` tuned profile

## CONSOLIDATION TARGETS
- **Organize Desktop Files**: Split into subdirectories (`audio/`, `midi/`, `utilities/`)
- **Dynamic Generation**: Replace static `.desktop` files with templated generation
- **Variable Consolidation**: Merge audio packages into `common/vars/packages.yml`
- **Realtime Validation**: Add kernel capability checks before tuning

## ANTI-PATTERNS (THIS ROLE)
- **No Organization**: 97 desktop files in flat directory (hard to maintain)
- **Assumption-Based Tuning**: No check for RT kernel before applying realtime settings
- **IRQ Balance Risk**: Disabling can impact system performance on non-audio workloads
- **Deprecated Variable**: `audio_system` variable pattern documented as deprecated
- **Templates in files/**: Desktop entries stored in `files/` instead of `templates/`
- **Mixed Responsibilities**: `tuning.yml` handles kernel, audio, and system configs (150 lines)

## NOTES
- **149 Files**: Largest role in project - candidate for splitting
- **Realtime Limits**: `/etc/security/limits.d/99-realtime-privileges.conf` allows memlock/rtprio
- **CPU Governor**: Sets `performance` mode (high power consumption)
- **Buffer Size**: Default 1024 samples (adjustable via `audio_buffer_size`)
- **Realtime Groups**: Users added to `audio` and `realtime` groups
- **Post-Install**: Logout/login required for group membership changes
- **Testing**: Use `jack_simple_client` to verify JACK configuration
- **Desktop Files**: Consider dynamic generation from package metadata
- **JackTrip Support**: Network audio streaming via dedicated playbook (`playbooks/jacktrip-pi.yml`)
