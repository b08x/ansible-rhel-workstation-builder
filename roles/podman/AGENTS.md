# PODMAN ROLE

**Purpose:** Podman container runtime with NVIDIA GPU passthrough and CDI support.

**Recent Changes (7a89076):** New role for container management with GPU acceleration.

## OVERVIEW
Installs and configures Podman as Docker alternative with NVIDIA Container Toolkit integration. Supports GPU passthrough via Container Device Interface (CDI) for AI/ML workloads.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Podman Install** | `tasks/main.yml` | Container runtime setup |
| **NVIDIA CDI** | `tasks/nvidia.yml` | GPU passthrough configuration |
| **User Config** | `tasks/user.yml` | Rootless container setup |
| **Variables** | `vars/main.yml` | Package lists, CDI settings |

## CONVENTIONS
- **Rootless First**: Prefer rootless containers over root
- **CDI Standard**: Use Container Device Interface for GPU access
- **Socket Alias**: Provide Docker-compatible socket for tools

## ANTI-PATTERNS
- **Never** run privileged containers unnecessarily
- **Never** skip CDI setup on NVIDIA systems

## UNIQUE STYLES
- **GPU Passthrough**: `nvidia-ctk` generates CDI specs for GPU access
- **Socket Compatibility**: `/var/run/docker.sock` alias for Podman
- **Systemd Integration**: User services for rootless containers

## NOTES
- **GPU Support**: Requires `roles/video` for NVIDIA driver installation
- **Docker Compat**: Many tools work with Podman via socket alias
- **Performance**: Rootless containers slightly slower but more secure