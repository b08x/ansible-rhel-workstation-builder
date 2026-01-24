# VIDEO ROLE

**Purpose:** Intel and NVIDIA GPU configuration with automatic detection and driver installation.

**Recent Changes (d69f85a, d9f95d8):** New role for GPU handling, NVIDIA tasks wrapped in detection block.

## OVERVIEW
Configures Intel integrated graphics and NVIDIA discrete GPUs with automatic hardware detection. Handles proprietary driver installation via akmods and ensures proper GPU acceleration.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **GPU Detection** | `tasks/main.yml` | Hardware detection logic |
| **Intel Setup** | `tasks/intel.yml` | Mesa drivers, VA-API |
| **NVIDIA Setup** | `tasks/nvidia.yml` | Wrapped in detection block (d9f95d8) |
| **Variables** | `vars/main.yml` | GPU-specific package lists |

## CONVENTIONS
- **Detection First**: All GPU tasks wrapped in hardware detection conditionals
- **Akmods Pattern**: NVIDIA drivers built via Dynamic Kernel Module Support
- **Fallback Logic**: Intel graphics always available as fallback

## ANTI-PATTERNS
- **Never** install NVIDIA drivers on systems without NVIDIA hardware
- **Never** skip detection - causes package conflicts

## UNIQUE STYLES
- **Hardware Detection**: `ansible_lspci` facts used for GPU identification
- **Conditional Execution**: Tasks only run if appropriate hardware detected
- **First Boot Delay**: NVIDIA akmods compilation causes 2-5min black screen (normal)

## NOTES
- **Secure Boot**: NVIDIA akmods unsigned - disable or enroll MOK
- **Hybrid Graphics**: Intel + NVIDIA configurations supported
- **First Boot**: Black screen 2-5min normal during driver compilation