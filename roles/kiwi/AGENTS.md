# KIWI ROLE KNOWLEDGE BASE

Custom ISO generation using KIWI NG for Fedora live images with NVIDIA/oneAPI/Sway support.

## WHERE TO LOOK
| Task                | File                                               | Notes                                                    |
|---------------------|----------------------------------------------------|----------------------------------------------------------|
| **Async ISO Build** | `tasks/build.yml`                                  | 281 lines, async/poll, hardcoded timeouts (7200s)        |
| **Package Lists**   | `defaults/main.yml`                                | 273 lines, monolithic (core/nvidia/oneapi/sway packages) |
| **Directory Setup** | `tasks/structure.yml`                              | 168 lines, cleanup/validation, hardcoded paths           |
| **XML Config**      | `templates/config.xml.j2`                          | KIWI image definition, repo management                   |
| **Boot Scripts**    | `templates/config.sh.j2`, `templates/images.sh.j2` | Fedora-specific hooks                                    |

## CONVENTIONS
- **Async Workflows**: `async: 7200`, `poll: 0` for long builds (45-90min)
- **Template-Only Mode**: `kiwi_execute_build=false` validates configs without building
- **Artifact Naming**: `fedora-{{ kiwi_fedora_version }}-{{ kiwi_image_type }}-*.iso`
- **Build Directory**: `/var/tmp/kiwi-{{ kiwi_image_name }}/`
- **NVIDIA Integration**: `kiwi_enable_nvidia=true` adds akmods, drivers, CUDA

## ANTI-PATTERNS (THIS ROLE)
- **Empty Password**: `kiwi_default_password` (hashed but weak for live ISOs)
- **Hardcoded Timeouts**: `async: 7200` not variablized
- **Monolithic Defaults**: 273-line defaults needs split (packages/build_configs/nvidia)
- **No Error Recovery**: Failed builds leave artifacts, no cleanup

## UNIQUE STYLES
- **NVIDIA First Boot**: 2-5min black screen normal (akmods compiling)
- **Secure Boot Incompatible**: Unsigned kernel modules require disabled Secure Boot or MOK enrollment
- **Hybrid Desktop**: GNOME 49 + Sway optional (`kiwi_enable_sway=true`)
- **DNF5 Retry**: 3 attempts for package downloads (Fedora 43+ instability)

## CONSOLIDATION TARGETS
- Split `defaults/main.yml` into `packages.yml`, `build_configs.yml`, `nvidia.yml`
- Extract post-build tasks from `build.yml` into `tasks/post-build.yml`
- Replace hardcoded timeouts with `kiwi_async_timeout` variable
- Implement cleanup on build failure (currently manual)

## NOTES
- **Disk Space**: 50-80GB required (80GB with oneAPI in image)
- **Build Time**: 45-90min depending on packages/NVIDIA/oneAPI
- **Testing**: Flash to USB with `dd` or test in QEMU (8GB+ RAM recommended)
- **Vs OSBuild**: Use KIWI for live ISOs, NVIDIA integration, multi-distro; OSBuild for RHEL ecosystem only
