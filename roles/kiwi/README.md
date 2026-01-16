# Ansible Role: kiwi

Automate the generation of custom Fedora 43 Workstation ISO images using KIWI NG with support for AI/HPC toolchains, proprietary GPU drivers, and hybrid desktop environments.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
- [Usage](#usage)
- [Build Process](#build-process)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [License](#license)

## Overview

This Ansible role provides a declarative, reproducible way to build custom Fedora 43 Workstation ISO images using KIWI NG. It's specifically designed for AI/HPC workstations requiring:

- **NVIDIA proprietary drivers** (via akmods for kernel compatibility)
- **Intel oneAPI compiler suite** (DPC++, MKL)
- **Hybrid desktop environment** (GNOME 49 + Sway tiling WM)
- **Container runtime** with GPU passthrough (Podman + NVIDIA Container Toolkit)

The role follows the "configuration-repository" pattern from the existing `osbuild` role, using Jinja2 templates to generate KIWI image descriptions dynamically.

## Features

### Core Capabilities

- ✅ **Automated ISO Building**: Full automation of KIWI NG build pipeline
- ✅ **Template-Driven**: Jinja2 templates for config.xml, config.sh, and images.sh
- ✅ **Feature Toggles**: Enable/disable components via boolean variables
- ✅ **SELinux Handling**: Automatic SELinux mode management during build
- ✅ **Async Execution**: Long-running builds with progress tracking
- ✅ **Validation**: XML syntax and KIWI schema validation
- ✅ **Build Manifests**: Detailed build logs with checksums and metadata

### Supported Components

| Component | Variable | Description |
|-----------|----------|-------------|
| GNOME Workstation | `kiwi_enable_gnome` | Full GNOME 49 desktop environment |
| Sway WM | `kiwi_enable_sway` | i3-compatible Wayland compositor |
| NVIDIA Drivers | `kiwi_enable_nvidia` | Proprietary drivers via akmods |
| Intel oneAPI | `kiwi_enable_oneapi` | DPC++ compilers and MKL libraries |
| Podman | Always enabled | Container runtime with Buildah/Skopeo |

## Requirements

### System Requirements

- **Operating System**: Fedora 43 or newer
- **Disk Space**: 50GB minimum (recommended: 80GB)
  - Base Fedora packages: ~5GB
  - GNOME Desktop: ~3GB
  - Intel oneAPI: ~15GB
  - NVIDIA drivers/CUDA: ~5GB
  - Build artifacts: ~15GB
  - ISO workspace: ~7GB
- **Memory**: 8GB minimum (recommended: 16GB)
- **Network**: Internet connection for package downloads (~20GB)
- **Privileges**: sudo/root access required

### Software Requirements

- Ansible 2.14 or newer
- Python 3.9+
- KIWI NG (installed automatically by role)

### Ansible Collections

```yaml
collections:
  - ansible.builtin
```

## Role Variables

### Image Configuration

```yaml
# Image identification
kiwi_image_name: "fedora-43-ai-hybrid"
kiwi_image_description: "Fedora 43 Workstation: GNOME/Sway/NVIDIA/CUDA/oneAPI"
kiwi_image_version: "1.0.0"
iso_label: "Fedora-43-AI-Hybrid"

# Fedora version
fedora_version: 43
```

### Build Directories

```yaml
# Build workspace
kiwi_build_dir: "/var/tmp/kiwi-build"        # KIWI description files
kiwi_output_dir: "/var/tmp/kiwi-output"      # Generated ISO location
```

### Feature Toggles

```yaml
# Enable/disable components
kiwi_enable_gnome: true      # GNOME 49 desktop
kiwi_enable_sway: true       # Sway window manager
kiwi_enable_nvidia: true     # NVIDIA proprietary drivers
kiwi_enable_oneapi: true     # Intel oneAPI compilers
```

### Image Size

```yaml
# Root filesystem size (GB)
# Must accommodate all enabled features
kiwi_root_size_gb: 45
```

### Repository URLs

```yaml
fedora_base_url: "https://dl.fedoraproject.org/pub/fedora/linux/releases/{{ fedora_version }}/Everything/x86_64/os/"
fedora_updates_url: "https://dl.fedoraproject.org/pub/fedora/linux/updates/{{ fedora_version }}/Everything/x86_64/"
rpmfusion_free_url: "https://mirrors.rpmfusion.org/free/fedora/releases/{{ fedora_version }}/Everything/x86_64/os/"
rpmfusion_nonfree_url: "https://mirrors.rpmfusion.org/nonfree/fedora/releases/{{ fedora_version }}/Everything/x86_64/os/"
intel_oneapi_url: "https://yum.repos.intel.com/oneapi"
nvidia_container_url: "https://nvidia.github.io/libnvidia-container/stable/rpm/x86_64"
```

### Kernel Parameters

```yaml
# Boot command line
kiwi_kernel_cmdline: "rhgb quiet rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1"
```

### Build Options

```yaml
# Execution control
kiwi_execute_build: true              # Set to false to skip build (template-only)
kiwi_allow_existing_root: true        # Reuse existing root for iterative builds
kiwi_clean_build_dir: false           # Clean build directory before starting
kiwi_clean_output_dir: false          # Clean output directory before starting

# Async task configuration
kiwi_async_timeout: 7200              # 2 hours timeout
kiwi_async_poll: 30                   # Poll every 30 seconds
```

### User Configuration

```yaml
kiwi_default_user: "fedora"
kiwi_default_groups: "wheel,video,render"
kiwi_default_password: ""             # Empty for live ISO
```

### Package Lists

See `defaults/main.yml` for complete package lists:
- `kiwi_core_packages`: Base system packages
- `kiwi_gnome_packages`: GNOME desktop components
- `kiwi_sway_packages`: Sway WM and dependencies
- `kiwi_nvidia_packages`: NVIDIA driver stack
- `kiwi_oneapi_packages`: Intel compiler suite
- `kiwi_container_packages`: Podman, Buildah, Skopeo
- `kiwi_devel_packages`: Development tools

## Dependencies

None. The role can optionally integrate with the `repos` role for repository management, but it manages its own repositories by default.

## Example Playbook

### Basic Usage

```yaml
---
- name: Build Fedora 43 AI Workstation ISO
  hosts: localhost
  become: true
  roles:
    - role: kiwi
```

### Custom Configuration

```yaml
---
- name: Build Custom Fedora ISO
  hosts: localhost
  become: true
  vars:
    fedora_version: 43
    kiwi_image_name: "my-custom-fedora"
    kiwi_image_version: "2.0.0"

    # Disable oneAPI to reduce size
    kiwi_enable_oneapi: false

    # Custom build directory
    kiwi_build_dir: "/mnt/fast-disk/kiwi-build"
  roles:
    - role: kiwi
```

### Template-Only Mode (Testing)

```yaml
---
- name: Test KIWI Templates
  hosts: localhost
  become: true
  vars:
    kiwi_execute_build: false  # Skip actual build
  roles:
    - role: kiwi
```

## Usage

### Basic Build

```bash
# Run the example playbook
ansible-playbook playbooks/build-kiwi-iso.yml

# Monitor build progress
tail -f /var/log/kiwi-build.log
```

### Skip Build (Template Generation Only)

```bash
ansible-playbook playbooks/build-kiwi-iso.yml -e "kiwi_execute_build=false"
```

### Custom Configuration

```bash
ansible-playbook playbooks/build-kiwi-iso.yml \
  -e "kiwi_enable_nvidia=false" \
  -e "kiwi_enable_oneapi=false" \
  -e "kiwi_image_name=minimal-fedora"
```

### Using Tags

```bash
# Only install prerequisites
ansible-playbook playbooks/build-kiwi-iso.yml --tags kiwi-prerequisites

# Only render templates
ansible-playbook playbooks/build-kiwi-iso.yml --tags kiwi-templates

# Only execute build (assumes templates exist)
ansible-playbook playbooks/build-kiwi-iso.yml --tags kiwi-build
```

## Build Process

### Phases

1. **Prerequisites** (`tasks/prerequisites.yml`)
   - Install KIWI NG and dependencies
   - Verify installation

2. **SELinux Handling** (`tasks/selinux_handling.yml`)
   - Check current SELinux status
   - Set to Permissive mode (required for KIWI)

3. **Structure Creation** (`tasks/structure.yml`)
   - Create build/output directories
   - Validate disk space (50GB minimum)
   - Check available memory

4. **Template Rendering** (`tasks/templates.yml`)
   - Render config.xml (KIWI image description)
   - Render config.sh (chroot configuration script)
   - Render images.sh (post-create customization)
   - Validate XML syntax and KIWI schema

5. **Build Execution** (`tasks/build.yml`)
   - Execute `kiwi-ng system build` (async)
   - Poll for completion (2-hour timeout)
   - Restore SELinux to original state
   - Generate build manifest with checksums

### Timeline

| Phase | Duration | Notes |
|-------|----------|-------|
| Prerequisites | 2-5 min | Download KIWI packages |
| Template Rendering | <1 min | Fast |
| Package Download | 15-30 min | Depends on bandwidth (~20GB) |
| Chroot Setup | 10-20 min | Install packages, run config.sh |
| Image Creation | 15-30 min | Squashfs compression |
| ISO Assembly | 5-10 min | Create bootable ISO |
| **Total** | **45-90 min** | Varies by system |

### First Boot (Important!)

**⚠️ NVIDIA Users: First boot will take 2-5 minutes with a black screen**

This is normal! The system is compiling NVIDIA kernel modules via akmods. Once complete, GDM will start automatically.

To check status during first boot:
```bash
# Switch to TTY2 (Ctrl+Alt+F2)
sudo journalctl -fu akmods
```

## Testing

### Run Role Tests

```bash
cd roles/kiwi
ansible-playbook tests/test.yml
```

This validates:
- Role structure
- Template rendering
- Variable expansion
- XML syntax

### Verify Generated ISO

```bash
# Check ISO integrity
sha256sum -c /var/tmp/kiwi-output/BUILD_MANIFEST.txt

# Test in QEMU/KVM
qemu-system-x86_64 \
  -m 8G \
  -enable-kvm \
  -boot d \
  -cdrom /var/tmp/kiwi-output/*.iso
```

### Runtime Verification (Boot ISO)

1. **NVIDIA Driver Check**
   ```bash
   lsmod | grep nvidia
   nvidia-smi
   ```

2. **Container GPU Passthrough**
   ```bash
   podman run --rm --device nvidia.com/gpu=all ubuntu nvidia-smi
   ```

3. **Intel oneAPI**
   ```bash
   source /opt/intel/oneapi/setvars.sh
   icx --version
   ```

4. **Sway Session**
   - Select "Sway" from GDM session menu
   - Verify Wayland compositor starts

## Troubleshooting

### Build Failures

#### Insufficient Disk Space

**Symptom**: Build fails with "No space left on device"

**Solution**:
```yaml
# Use a different build directory with more space
kiwi_build_dir: "/mnt/large-disk/kiwi-build"
```

#### Repository GPG Errors

**Symptom**: "GPG signature verification failed"

**Solution**: Already handled in role via `kiwi_rpm_check_signatures: false` for Intel/NVIDIA repos.

#### DNF5 Instability

**Symptom**: Random package download failures

**Solution**: Role includes retry logic (3 attempts with 10s delay)

#### SELinux Denials

**Symptom**: KIWI fails with permission errors

**Solution**: Role automatically sets Permissive mode. Verify with:
```bash
getenforce  # Should show "Permissive" during build
```

### Runtime Issues

#### Black Screen on First Boot (NVIDIA)

**Expected behavior!** Wait 2-5 minutes for akmods to compile drivers.

To monitor:
```bash
# Boot with 'e' in GRUB, add 'systemd.unit=multi-user.target'
# Then after boot:
sudo journalctl -fu akmods
```

#### Container GPU Not Working

**Check CDI specification**:
```bash
sudo nvidia-ctk cdi list
```

**Regenerate if missing**:
```bash
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
```

#### Intel oneAPI Not in PATH

**Manual activation**:
```bash
source /opt/intel/oneapi/setvars.sh
```

**Persistent activation**: Already configured in `/etc/profile.d/oneapi.sh`

### Debug Mode

Enable verbose KIWI output:
```yaml
kiwi_verbose: true
```

Check logs:
```bash
tail -f /var/log/kiwi-build.log
```

## Architecture

### Directory Structure

```
roles/kiwi/
├── defaults/
│   └── main.yml              # User-configurable variables
├── tasks/
│   ├── main.yml              # Entry point
│   ├── prerequisites.yml     # Install KIWI NG
│   ├── selinux_handling.yml  # Manage SELinux mode
│   ├── structure.yml         # Create directories, validate resources
│   ├── templates.yml         # Render Jinja2 templates
│   └── build.yml             # Execute KIWI build
├── templates/
│   ├── config.xml.j2         # KIWI image description
│   ├── config.sh.j2          # Chroot configuration
│   └── images.sh.j2          # Post-create customization
├── handlers/
│   └── main.yml              # Post-build handlers
├── meta/
│   └── main.yml              # Ansible Galaxy metadata
└── tests/
    ├── test.yml              # Role validation tests
    └── inventory             # Test inventory
```

### KIWI Script Execution Flow

```
KIWI Build Phases:
1. prepare    → Run config.sh inside chroot
2. create     → Assemble root filesystem
3. images.sh  → Post-create customization
4. bundle     → Create ISO
```

### Key Design Decisions

1. **DNF5**: Fedora 43 mandates DNF5 (no fallback to DNF4)
2. **Akmods**: NVIDIA drivers compile on first boot (can't pre-compile in ISO)
3. **OverlayFS**: Enables writable filesystem for akmods compilation
4. **Signature Validation Disabled**: Pragmatic workaround for Intel/NVIDIA repos with weak GPG keys
5. **Async Execution**: Long builds use Ansible async tasks to prevent SSH timeouts

## Comparison: OSBuild vs KIWI NG

| Feature | OSBuild | KIWI NG (this role) |
|---------|---------|---------------------|
| Format | TOML blueprints | XML descriptions |
| Live ISO | Limited | Native support |
| Akmods | Difficult | Full support |
| Flexibility | Red Hat ecosystem | Multi-distro |
| Use Case | Standard images | Custom live ISOs |

**When to use KIWI**:
- Building custom live ISOs
- Need for akmods (NVIDIA)
- Hybrid desktop environments
- AI/HPC workstation images

**When to use OSBuild**:
- Standard Fedora variants
- Server images
- RHEL/CentOS compatibility

## License

MIT

## Author Information

Platform Engineering

For issues and contributions, see the project repository.

---

**Generated by**: Ansible Role for KIWI NG
**Last Updated**: 2026-01-16
**Compatible with**: Fedora 43+
