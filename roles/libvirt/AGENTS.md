# LIBVIRT ROLE

**Purpose:** QEMU/KVM virtualization stack with GPU passthrough capabilities.

**Status:** Established virtualization platform role.

## OVERVIEW
Installs and configures libvirt virtualization stack including QEMU, KVM, and management tools. Supports both system and user session virtualization.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Libvirt Install** | `tasks/main.yml` | Core virtualization packages |
| **KVM Setup** | `tasks/kvm.yml` | Kernel module configuration |
| **User Access** | `tasks/user.yml` | Libvirt group membership |
| **Variables** | `vars/main.yml` | Virtualization settings |

## CONVENTIONS
- **System Libvirt**: Full system virtualization capabilities
- **User Sessions**: Unprivileged user virtualization
- **Group Access**: Users added to libvirt group for VM management

## ANTI-PATTERNS (THIS PROJECT)
- **Root-equivalent privileges**: Libvirt group provides system access
- **Never** run unpatched VMs with network access
- **Never** share host directories without considering security

## UNIQUE STYLES
- **Dual Mode**: System and user session support
- **Hardware Detection**: KVM availability checking
- **Bridge Networking**: Optional network bridge configuration

## NOTES
- **Hardware**: Requires CPU virtualization extensions (Intel VT-x/AMD-V)
- **Performance**: KVM provides near-native performance
- **GPU Passthrough**: Advanced configuration for dedicated GPU access