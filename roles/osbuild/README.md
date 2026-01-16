# OSBuild - Custom Fedora Workstation ISO Builder

An Ansible role for building custom Fedora Workstation ISOs using osbuild-composer. Designed for creating high-performance workstation images with GNOME, Sway, NVIDIA drivers, CUDA, Intel oneAPI, and container tooling.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Role Variables](#role-variables)
- [Usage Examples](#usage-examples)
- [Blueprint Customization](#blueprint-customization)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Testing & Validation](#testing--validation)
- [Secure Boot Considerations](#secure-boot-considerations)
- [License](#license)

## Overview

This role automates the complete workflow for building custom Fedora Workstation ISOs:

1. **Infrastructure Setup**: Installs and configures osbuild-composer on a Fedora build host
2. **Repository Configuration**: Loads third-party repository sources (RPM Fusion, NVIDIA, Intel oneAPI)
3. **Blueprint Management**: Creates and validates blueprint definitions
4. **Build Execution**: Compiles the ISO image and monitors progress
5. **Image Delivery**: Downloads the final ISO to a specified output directory

The role supports both **static blueprints** (TOML files) and **dynamic templating** (Jinja2) for maximum flexibility.

## Features

✅ **Dual Desktop Environments**: GNOME 49 + Sway window manager
✅ **NVIDIA Support**: Proprietary drivers, CUDA toolkit, Container Device Interface (CDI)
✅ **Intel oneAPI**: Configurable image-time or first-boot installation
✅ **Container Tooling**: Podman, Docker CE, GPU-accelerated containers
✅ **Development Tools**: GCC, Python, Node.js, Ansible collections
✅ **Virtualization**: libvirt, QEMU/KVM, Vagrant
✅ **First-Boot Automation**: Embedded Ansible playbook for post-install configuration
✅ **Comprehensive Error Handling**: Detailed logging, retry logic, helpful diagnostics

## Requirements

### Build Host

- **Operating System**: Fedora 43 Workstation (or compatible version)
- **Disk Space**: Minimum 50GB free in `/var/lib/osbuild-composer`
  - Add ~30GB more if using `include_oneapi_in_image: true`
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Network**: Internet connectivity for repository access
- **Privileges**: Sudo access for package installation and service management

### Ansible

- **Ansible Version**: 2.9 or higher
- **Python**: Python 3.6+
- **Collections**: `ansible.posix`, `community.general` (auto-installed via dependencies)

## Installation

### From Ansible Galaxy (future)

```bash
ansible-galaxy install b08x.osbuild
```

### From Source

```bash
cd /path/to/your/ansible/project
git clone https://github.com/yourusername/ansible-role-osbuild.git roles/osbuild
```

## Role Variables

### Essential Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `blueprint_name` | `fedora-workstation-custom` | Name of the blueprint and output image |
| `osbuild_distro` | `fedora-43` | Fedora distribution version |
| `osbuild_image_type` | `workstation-live-installer` | Image type (`live-iso`, `qcow2`, etc.) |
| `use_nvidia` | `true` | Enable NVIDIA proprietary drivers and CUDA |
| `use_sway` | `true` | Include Sway window manager alongside GNOME |
| `include_oneapi_in_image` | `false` | Install Intel oneAPI in image (vs first-boot) |

### Feature Toggles

| Variable | Default | Description |
|----------|---------|-------------|
| `include_development_tools` | `true` | Add GCC, Python, Node.js, etc. |
| `include_container_tools` | `true` | Add Podman, Docker CE, buildah |
| `use_blueprint_template` | `true` | Use Jinja2 template (vs static blueprint) |

### Build Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `osbuild_build_timeout` | `14400` (4 hours) | Maximum build time in seconds |
| `osbuild_poll_interval` | `30` | Status check interval in seconds |
| `osbuild_build_retries` | `1` | Number of retry attempts on failure |
| `osbuild_output_dir` | `/var/tmp/osbuild-images` | Directory for final ISO |
| `osbuild_log_dir` | `/var/tmp/osbuild-logs` | Directory for build logs |

### User Customization

| Variable | Default | Description |
|----------|---------|-------------|
| `osbuild_user_name` | `ansible` | Default user account name |
| `osbuild_user_password` | *(hash)* | Encrypted password (change this!) |
| `osbuild_user_groups` | `[wheel, libvirt]` | User group memberships |
| `osbuild_hostname` | `fedora-workstation` | System hostname |
| `osbuild_timezone` | `America/New_York` | System timezone |

### Package Lists

Customize packages via these list variables:

- `osbuild_extra_packages`: Additional packages to include
- `osbuild_sway_packages`: Sway desktop components (if `use_sway: true`)
- `osbuild_nvidia_packages`: NVIDIA driver stack (if `use_nvidia: true`)
- `osbuild_oneapi_packages`: Intel oneAPI components
- `osbuild_development_packages`: Development tools
- `osbuild_container_packages`: Container runtime packages

See `defaults/main.yml` for complete variable definitions.

## Usage Examples

### Basic Usage - NVIDIA Workstation

```yaml
- hosts: builder
  roles:
    - role: osbuild
      vars:
        blueprint_name: "my-nvidia-workstation"
        use_nvidia: true
        use_sway: true
        osbuild_user_name: "johndoe"
        osbuild_user_password: "$6$..."  # mkpasswd --method=sha-512
```

### Minimal Workstation (No NVIDIA)

```yaml
- hosts: builder
  roles:
    - role: osbuild
      vars:
        blueprint_name: "minimal-workstation"
        use_nvidia: false
        use_sway: false
        include_development_tools: false
```

### Intel oneAPI in Image (Large ISO)

```yaml
- hosts: builder
  roles:
    - role: osbuild
      vars:
        blueprint_name: "hpc-workstation"
        include_oneapi_in_image: true
        osbuild_build_timeout: 21600  # 6 hours for large build
```

### Using Static Blueprint

```yaml
- hosts: builder
  roles:
    - role: osbuild
      vars:
        use_blueprint_template: false
        static_blueprint_path: "files/fedora-43/x86_64/workstation/custom.toml"
```

### Custom Package List

```yaml
- hosts: builder
  roles:
    - role: osbuild
      vars:
        osbuild_extra_packages:
          - vim-enhanced
          - tmux
          - neovim
          - ripgrep
          - fd-find
```

## Blueprint Customization

### Using Dynamic Templates (Recommended)

The role includes a comprehensive Jinja2 template (`templates/fedora-workstation.toml.j2`) that generates blueprints based on role variables. This is the default mode (`use_blueprint_template: true`).

**Advantages**:
- No blueprint file editing required
- Consistent configuration via Ansible variables
- Easy version control and sharing
- Automatic integration of feature flags

### Using Static Blueprints

For advanced customization, create your own blueprint TOML file:

```bash
# Create custom blueprint
cp roles/osbuild/files/fedora-43/x86_64/workstation/fedora-43-workstation-nvidia.toml \
   my-custom-blueprint.toml

# Edit as needed
vi my-custom-blueprint.toml
```

Then reference it in your playbook:

```yaml
vars:
  use_blueprint_template: false
  static_blueprint_path: "path/to/my-custom-blueprint.toml"
```

See [Blueprint Reference](https://osbuild.org/docs/user-guide/blueprint-reference/) for TOML syntax.

## Advanced Configuration

### Fedora 42 vs Fedora 43

The role supports both Fedora 42 and 43. To use Fedora 42:

```yaml
vars:
  osbuild_distro: "fedora-42"
  osbuild_sources:
    - rpmfusion-free
    - rpmfusion-nonfree
    - cuda-fedora42-x86_64  # Note: version-specific
```

### Multiple Builds in Parallel

Run multiple builders simultaneously:

```yaml
# inventory
[builders]
builder1.example.com
builder2.example.com

# playbook
- hosts: builders
  strategy: free  # Parallel execution
  roles:
    - osbuild
```

### Custom Repository Sources

Add your own repositories:

1. Create a source TOML file in `files/fedora-43/x86_64/sources/my-repo.toml`:

```toml
id = "my-custom-repo"
name = "My Custom Repository"
type = "yum-baseurl"
url = "https://example.com/repo"
check_gpg = true
gpgkeys = ["https://example.com/RPM-GPG-KEY"]
```

2. Reference it in your playbook:

```yaml
vars:
  osbuild_sources:
    - rpmfusion-free
    - my-custom-repo
```

### First-Boot Customization

The role embeds an Ansible playbook that runs on first boot. Customize it by modifying the template or using a static blueprint.

Default first-boot tasks:
- Install Intel oneAPI (if not in image)
- Configure repository priorities
- Set graphical target

## Troubleshooting

### Build Fails with Dependency Errors

**Symptom**: `composer-cli blueprints depsolve` fails

**Solutions**:
1. Verify all sources are loaded: `composer-cli sources list`
2. Check repository accessibility: `composer-cli sources info <source-name>`
3. Review package names for typos in blueprint
4. Ensure distro version matches repository versions

### NVIDIA Driver Not Loading After Boot

**Symptom**: `nvidia-smi` shows "No devices found"

**Solutions**:
1. Check if nouveau is blacklisted: `lsmod | grep nouveau` (should be empty)
2. Verify akmod compilation: `sudo akmods --force`
3. Check logs: `journalctl -xe | grep nvidia`
4. Ensure kernel-devel matches running kernel

### Build Timeout

**Symptom**: Build exceeds `osbuild_build_timeout`

**Solutions**:
1. Increase timeout: `osbuild_build_timeout: 21600`
2. Consider disabling `include_oneapi_in_image` for faster builds
3. Check network speed for repository downloads
4. Monitor build: `composer-cli compose info <uuid>`

### Insufficient Disk Space

**Symptom**: Build fails with "No space left on device"

**Solutions**:
1. Check free space: `df -h /var/lib/osbuild-composer`
2. Clean old composes: `composer-cli compose delete <uuid>`
3. Increase disk allocation to build host

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to load source` | TOML syntax error | Validate TOML with `python3 -c "import tomli; tomli.load(open('file.toml'))"` |
| `GPG key retrieval failed` | Network/firewall issue | Check `gpgkeys` URL accessibility |
| `Package not found` | Typo or missing repo | Review package name and enabled sources |
| `Blueprint already exists` | Duplicate blueprint | Delete with `composer-cli blueprints delete <name>` |

## Testing & Validation

### 1. Virtual Machine Testing (Recommended First)

```bash
# After build completes
virt-install \
  --name test-custom-iso \
  --memory 4096 \
  --vcpus 2 \
  --disk size=40 \
  --cdrom /var/tmp/osbuild-images/my-blueprint-fedora-43.iso \
  --os-variant fedora43 \
  --graphics spice
```

**Verification Steps**:
- Boot ISO in VM
- Verify Anaconda installer launches
- Check both GNOME and Sway sessions appear in GDM
- Install to virtual disk
- Test installed system

### 2. Physical Hardware Testing

```bash
# Flash to USB drive
sudo dd if=/var/tmp/osbuild-images/my-blueprint-fedora-43.iso \
        of=/dev/sdX \
        bs=4M \
        status=progress \
        oflag=sync
```

**NVIDIA Hardware Verification**:
```bash
# After installation and reboot
nvidia-smi  # Should show GPU info
podman run --device nvidia.com/gpu=all nvidia/cuda:12.3.2-base-ubuntu22.04 nvidia-smi
```

### 3. Manifest Inspection

```bash
# Mount ISO and query packages
sudo mkdir /mnt/iso
sudo mount -o loop /var/tmp/osbuild-images/my-blueprint.iso /mnt/iso
rpm -qa --dbpath /mnt/iso/var/lib/rpm | grep -i nvidia
sudo umount /mnt/iso
```

## Secure Boot Considerations

### NVIDIA Driver Compatibility

**Challenge**: NVIDIA akmod drivers are compiled locally on first boot, resulting in unsigned kernel modules that Secure Boot will reject.

**Options**:

1. **Disable Secure Boot** (Easiest)
   - Enter BIOS/UEFI and disable Secure Boot
   - No MOK enrollment required
   - ✅ Simplest for development/testing systems

2. **Enroll MOK (Machine Owner Key)**
   - During first boot, akmod creates a signing key
   - Follow prompts to enroll MOK in UEFI
   - ⚠️ Requires physical access to console
   - ⚠️ Different key per machine

3. **Pre-signed Drivers** (Future Enhancement)
   - Use RPM Fusion's pre-built kmod packages
   - Signed by RPM Fusion's trusted key
   - ❌ Not currently implemented in this role

### Documentation

The role automatically includes instructions in the first-boot Ansible playbook output. Users will see MOK enrollment prompts if Secure Boot is enabled.

## License

MIT-0 (See LICENSE file)

This role is released into the public domain. You may use, modify, and distribute it freely without attribution.

## References

- [OSBuild Documentation](https://osbuild.org/docs/)
- [Blueprint Reference](https://osbuild.org/docs/user-guide/blueprint-reference/)
- [composer-cli Guide](https://osbuild.org/docs/developer-guide/projects/composer-cli/)
- [Fedora Image Builder](https://osbuild.org/docs/hosted/fedora-console/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)
- [Intel oneAPI Documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/documentation.html)

## Contributing

Contributions welcome! Please open issues or pull requests on the project repository.

---

**Generated by**: Ansible OSBuild Role
**Last Updated**: 2026-01-16
