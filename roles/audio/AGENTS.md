# AUDIO ROLE KNOWLEDGE BASE

**Generated:** 07:26:41 AM (America/New_York)
**Commit:** 8940810
**Branch:** development

---

## OVERVIEW
Professional-grade audio subsystem for low-latency, realtime performance on Linux workstations. Supports PipeWire (modern) and JACK+PulseAudio (legacy) with comprehensive system tuning.

## STRUCTURE
```
roles/audio/
├── tasks/          # Modular audio tasks
│   ├── main.yml    # Orchestrates workflow
│   ├── pipewire.yml
│   ├── tuning.yml  # Realtime optimization (150 lines)
│   ├── applications.yml
│   └── configure_pipewire.yml
├── files/home/local/share/applications/  # 97 desktop files
├── templates/wireplumber/    # WirePlumber Lua configs
├── vars/           # Distro-specific packages (Fedora.yml, RedHat.yml)
└── defaults/       # Buffer sizes, sample rates, JACK params
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **PipeWire Setup** | `tasks/pipewire.yml` | Modern audio stack (default) |
| **System Tuning** | `tasks/tuning.yml` | Realtime privileges, tuned profiles, RTIRQ |
| **Applications** | `tasks/applications.yml` | COPR repos, DAW installs |
| **Desktop Files** | `files/home/local/share/applications/` | 97 audio app .desktop files |
| **WirePlumber Config** | `templates/wireplumber/` | Pro-audio Lua templates |
| **Package Lists** | `vars/Fedora.yml` | Audinux COPR, audio packages |

## CONVENTIONS
- **Audio Stack Selection**: `audio_system: "pipewire"` (default) or `"pulseaudio_jack"`
- **Deep File Structure**: 97 desktop files at depth 5 (`files/home/local/share/applications/`)
- **User-Specific Configs**: Deployed to `~/.config/pipewire/` via `getent` user resolution
- **Realtime Optimization**: Custom tuned profiles, IRQ prioritization, CPU governor
- **Distribution-Aware**: Separate package lists for Fedora vs RHEL/Rocky

## ANTI-PATTERNS (THIS PROJECT)
- **Templates in files/**: Desktop entries stored in `files/` instead of `templates/` 
- **Mixed responsibilities**: `tuning.yml` handles kernel, audio, and system configs (150 lines)

## UNIQUE STYLES
- **Professional Audio Focus**: Optimized for DAW/music production workflows
- **Lua Configuration**: WirePlumber configs use Jinja2-templated Lua scripts
- **COPR Integration**: Audinux stable-audio repo for bleeding-edge packages
- **Realtime Tuning**: Custom `realtime-modified` tuned profile, disabled irqbalance
- **Cross-Role Integration**: JackTrip playbook extends audio for network streaming

## AUDIO FLOW
```
PipeWire Stack (default):
packages → user services → configs → tuning → applications

Legacy Stack (pro-audio):
JACK + PulseAudio → realtime privileges → tuned profiles → applications
```

## NOTES
- **Buffer Size**: Default 1024 samples (adjustable via `audio_buffer_size`)
- **Realtime Groups**: Users added to `audio` and `realtime` groups  
- **JackTrip Support**: Network audio streaming via dedicated playbook
- **Post-Install**: Logout/login required for group membership changes