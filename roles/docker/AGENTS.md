# DOCKER ROLE

**Purpose:** Docker CE container runtime with NVIDIA Container Toolkit integration.

**Status:** Established role for Docker container platform.

## OVERVIEW
Installs Docker Community Edition with NVIDIA GPU support for containerized AI/ML workloads. Configures user access and systemd integration.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Docker Install** | `tasks/main.yml` | Docker CE installation |
| **NVIDIA Support** | `tasks/nvidia.yml` | GPU container support |
| **User Setup** | `tasks/user.yml` | Docker group membership |
| **Variables** | `vars/main.yml` | Package configuration |

## CONVENTIONS
- **Docker CE**: Community Edition from Docker repositories
- **GPU Support**: NVIDIA Container Toolkit for GPU passthrough
- **User Access**: Add users to docker group (security consideration)

## ANTI-PATTERNS (THIS PROJECT)
- **Root-equivalent privileges**: Docker group membership provides root access
- **Never** run untrusted containers with GPU access
- **Never** expose Docker socket without authentication

## UNIQUE STYLES
- **GPU Integration**: Automatic NVIDIA runtime configuration
- **Repository Management**: Official Docker CE repositories
- **Systemd Service**: Docker daemon managed by systemd

## NOTES
- **Security Risk**: Docker group = root privileges
- **GPU Requirements**: Needs NVIDIA drivers installed first
- **Alternative**: Consider `roles/podman` for rootless containers