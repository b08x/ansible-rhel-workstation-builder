# Common Role

This Ansible role provides foundational system configuration for RedHat family distributions. It establishes a baseline system state by configuring essential system settings, the GRUB bootloader, rc.local compatibility, and dotfile management.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Supported Platforms](#supported-platforms)
- [Role Variables](#role-variables)
  - [System Configuration](#system-configuration)
  - [GRUB Bootloader Configuration](#grub-bootloader-configuration)
  - [Kernel Parameters](#kernel-parameters)
  - [GRUB Visual Settings](#grub-visual-settings)
- [Tasks Breakdown](#tasks-breakdown)
  - [System Configuration](#system-configuration-1)
  - [GRUB Configuration](#grub-configuration)
  - [rc.local Management](#rclocal-management)
  - [yadm Dotfile Management](#yadm-dotfile-management)
- [Handlers](#handlers)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
  - [Basic Usage](#basic-usage)
  - [Custom Kernel Parameters](#custom-kernel-parameters)
  - [Different Timezone](#different-timezone)
- [Advanced Usage](#advanced-usage)
  - [Customizing GRUB Kernel Parameters](#customizing-grub-kernel-parameters)
  - [Disabling Specific Tasks](#disabling-specific-tasks)
- [Testing](#testing)
  - [Verification Commands](#verification-commands)
- [Troubleshooting](#troubleshooting)
  - [GRUB Regeneration](#grub-regeneration)
  - [Locale Problems](#locale-problems)
  - [rc.local Not Running](#rclocal-not-running)
- [License](#license)
- [Author Information](#author-information)

## Features

- **System Configuration**: Sets timezone, locale, and keymap
- **GRUB Bootloader**: Configures kernel parameters and visual settings
- **rc.local Compatibility**: Restores rc.local functionality on systemd-based systems
- **Dotfile Management**: Installs yadm (Yet Another Dotfiles Manager)
- **Performance Tuning**: Default kernel parameters optimized for performance
- **Idempotent**: Safe to run multiple times without side effects

## Requirements

- Ansible 2.9 or higher
- RedHat family distribution (Fedora, RHEL, Rocky Linux, AlmaLinux)
- Root/sudo privileges
- GRUB2 bootloader installed

## Supported Platforms

- Fedora 38+
- RHEL 8/9
- Rocky Linux 8/9
- AlmaLinux 8/9

## Role Variables

### System Configuration

```yaml
# System timezone (uses timedatectl)
timezone: "America/New_York"

# System locale setting
locale: "en_US.UTF-8"

# Console keyboard layout
keymap: "us"
```

### GRUB Bootloader Configuration

```yaml
# Bootloader type (currently only 'grub' is supported)
bootloader: grub

# Custom background image for GRUB menu
grub_background: "/usr/share/backgrounds/syncopated/syncopated016.png"

# Enable/disable os-prober for multi-boot detection
# Set to true to detect other operating systems
grub_enable_os_prober: false
```

### Kernel Parameters

The role separates kernel parameters into two categories for flexibility:

```yaml
# Default kernel parameters (quiet boot with performance optimizations)
kernel_parameters_default: "splash threadirqs mitigations=off"

# Additional kernel parameters
kernel_parameters: "ipv6.disable=1 net.ifnames=0"
```

**Default Kernel Parameters Explained**:

| Parameter | Purpose | Impact |
|-----------|---------|--------|
| `splash` | Display boot splash screen | Visual |
| `threadirqs` | Thread IRQ handling | Performance improvement for latency-sensitive workloads |
| `mitigations=off` | Disable CPU vulnerability mitigations | Significant performance gain, reduced security |

**Additional Kernel Parameters Explained**:

| Parameter | Purpose | Impact |
|-----------|---------|--------|
| `ipv6.disable=1` | Disable IPv6 networking | Simplifies network configuration if IPv6 not needed |
| `net.ifnames=0` | Use traditional network interface names (eth0, wlan0) | Predictable interface naming |

**Note on `mitigations=off`**: This parameter disables CPU-level security mitigations for Spectre, Meltdown, and related vulnerabilities. It provides substantial performance improvements but should only be used in trusted environments. For production systems, consider removing this parameter.

The template also includes:
- `crashkernel` parameters for kernel crash dumps (automatically sized based on system memory)
- `selinux=0` to disable SELinux (can be modified in the template)

### GRUB Visual Settings

The GRUB template (`templates/etc/default/grub.j2`) configures:

```bash
GRUB_TIMEOUT=5                          # 5-second boot menu timeout
GRUB_DEFAULT=saved                      # Remember last selected boot entry
GRUB_SAVEDEFAULT=true                   # Save default selection
GRUB_TIMEOUT_STYLE=menu                 # Always show boot menu
GRUB_GFXMODE=auto                       # Automatic graphics resolution
GRUB_GFXPAYLOAD_LINUX=keep              # Keep graphics mode in Linux
GRUB_DISABLE_RECOVERY=true              # Hide recovery mode entries
GRUB_ENABLE_BLSCFG=true                 # Use Boot Loader Specification
```

## Tasks Breakdown

### System Configuration

The main tasks file (`tasks/main.yml`) handles fundamental system settings:

1. **Timezone Configuration**
   - Uses `timedatectl set-timezone` to configure system timezone
   - Idempotent operation that only changes when necessary
   - Tagged with `timezone` for selective execution

2. **Locale Settings**
   - Configures system locale (defined in `defaults/main.yml`)
   - Triggers locale generation if changed

3. **Keymap Configuration**
   - Sets console keyboard layout
   - Persists across reboots

### GRUB Configuration

The GRUB configuration tasks (`tasks/grub.yml`) manage bootloader settings:

1. **Template GRUB Configuration**
   - Deploys `/etc/default/grub` from Jinja2 template
   - Creates backup of existing configuration
   - Ownership: root:root, mode: 0644
   - Registers changes to trigger rebuild

2. **Rebuild GRUB Configuration**
   - Executes `grub2-mkconfig -o /boot/grub2/grub.cfg`
   - Only runs when GRUB configuration changes
   - Ensures new kernel parameters take effect

**Material Process**: This task **transforms** the target host's boot configuration by **templating** the GRUB defaults file and **rebuilding** the GRUB configuration to apply kernel parameters and visual settings.

### rc.local Management

The rc.local tasks (`tasks/rclocal.yml`) restore traditional rc.local functionality:

1. **Check Existence**
   - Verifies if `/etc/rc.local` already exists
   - Registers result for conditional execution

2. **Create rc.local Script**
   - Creates `/etc/rc.local` with shebang if missing
   - Ownership: root:root, mode: 0750 (executable)
   - Only executes when file doesn't exist

3. **Create systemd Service**
   - Deploys `rc-local.service` unit file
   - Configures as oneshot service with no timeout
   - Runs at SysV priority 99 for compatibility
   - Registers changes to trigger daemon reload

4. **Reload systemd**
   - Reloads systemd daemon when service file changes
   - Ensures systemd recognizes new service

5. **Enable Service**
   - Enables `rc-local.service` to run at boot
   - Ensures rc.local scripts execute during startup

**Attribution**: Based on work by [James Cherti](https://www.jamescherti.com/ansible-config-etc-rc-local-linux-systemd/)

**Material Process**: This task sequence **transforms** systemd-based systems by **creating** the rc.local compatibility layer, enabling legacy boot scripts to execute in modern init systems.

### yadm Dotfile Management

The yadm tasks (`tasks/yadm.yml`) install dotfile management tooling:

1. **Download yadm**
   - Fetches latest yadm script from GitHub repository
   - Installs to `/usr/local/bin/yadm`
   - Sets ownership to configured user
   - Mode: 0755 (executable)
   - Tagged with `yadm` for selective execution

**Material Process**: This task **installs** the yadm dotfile manager, enabling users to manage their configuration files using Git-based workflows.

## Handlers

The role includes three handlers (`handlers/main.yml`) triggered by configuration changes:

| Handler Name | Command | Trigger Condition | Purpose |
|-------------|---------|-------------------|---------|
| `Generate locales` | `locale-gen` | Locale configuration changes | Regenerates locale data files |
| `Update hwclock` | `hwclock --systohc` | Timezone changes | Synchronizes hardware clock with system time |
| `Rebuild grub` | `grub2-mkconfig -o /boot/grub2/grub.cfg` | GRUB configuration changes | Regenerates GRUB boot menu |

**Execution Timing**: Handlers run at the **end of the play**, after all tasks complete. This ensures configuration changes are applied atomically.

## Dependencies

This role has no external dependencies. It can be used standalone or as a foundation for other roles.

## Example Playbook

### Basic Usage

```yaml
---
- hosts: workstations
  become: true
  roles:
    - role: common
```

This applies default system configuration with:
- America/New_York timezone
- en_US.UTF-8 locale
- US keyboard layout
- Performance-optimized kernel parameters
- rc.local compatibility
- yadm installation

### Custom Kernel Parameters

```yaml
---
- hosts: servers
  become: true
  roles:
    - role: common
      vars:
        # Keep security mitigations for production servers
        kernel_parameters_default: "splash threadirqs"
        # Enable IPv6 and use predictable network names
        kernel_parameters: ""
```

### Different Timezone

```yaml
---
- hosts: eu_servers
  become: true
  roles:
    - role: common
      vars:
        timezone: "Europe/London"
        locale: "en_GB.UTF-8"
        keymap: "uk"
```

### Minimal Installation (Skip Optional Components)

```yaml
---
- hosts: minimal_systems
  become: true
  roles:
    - role: common
  tags:
    - timezone
    - grub
  # This skips rc.local and yadm installation
```

## Advanced Usage

### Customizing GRUB Kernel Parameters

For specialized workloads, you may need custom kernel parameters:

#### Real-time Audio Workstation

```yaml
---
- hosts: audio_workstation
  become: true
  roles:
    - role: common
      vars:
        kernel_parameters_default: "splash threadirqs mitigations=off"
        kernel_parameters: "ipv6.disable=1 net.ifnames=0 quiet nowatchdog idle=poll"
```

#### Secure Production Server

```yaml
---
- hosts: production
  become: true
  roles:
    - role: common
      vars:
        # Keep all security mitigations
        kernel_parameters_default: "splash quiet"
        kernel_parameters: "audit=1 selinux=1"
```

#### Gaming/Performance Desktop

```yaml
---
- hosts: gaming_pc
  become: true
  roles:
    - role: common
      vars:
        kernel_parameters_default: "splash threadirqs mitigations=off"
        kernel_parameters: "ipv6.disable=1 pci=nomsi processor.max_cstate=1 intel_idle.max_cstate=0"
```

### Disabling Specific Tasks

Use Ansible tags to run only specific portions of the role:

```bash
# Only configure timezone
ansible-playbook playbook.yml --tags "timezone"

# Only configure GRUB
ansible-playbook playbook.yml --tags "grub"

# Only install yadm
ansible-playbook playbook.yml --tags "yadm"

# Skip yadm installation
ansible-playbook playbook.yml --skip-tags "yadm"
```

### Custom GRUB Background

To use a custom GRUB background image:

```yaml
---
- hosts: desktops
  become: true
  tasks:
    - name: Copy custom GRUB background
      ansible.builtin.copy:
        src: files/custom-grub-background.png
        dest: /usr/share/backgrounds/custom/grub-bg.png
        owner: root
        group: root
        mode: '0644'

  roles:
    - role: common
      vars:
        grub_background: "/usr/share/backgrounds/custom/grub-bg.png"
```

**Requirements**:
- Image should be PNG or TGA format
- Recommended resolution: 1920x1080 or lower
- Place image before running the common role

## Testing

### Verification Commands

After running the role, verify the configuration:

#### System Configuration

```bash
# Check timezone
timedatectl

# Expected output:
#                Local time: Wed 2025-12-03 15:30:45 EST
#            Universal time: Wed 2025-12-03 20:30:45 UTC
#                  RTC time: Wed 2025-12-03 20:30:45
#                 Time zone: America/New_York (EST, -0500)

# Check locale
localectl

# Expected output:
#    System Locale: LANG=en_US.UTF-8
#        VC Keymap: us
```

#### GRUB Configuration

```bash
# View GRUB defaults
cat /etc/default/grub

# Check active kernel parameters
cat /proc/cmdline

# Expected output should include your configured parameters:
# BOOT_IMAGE=(hd0,gpt2)/vmlinuz... splash threadirqs mitigations=off ipv6.disable=1 net.ifnames=0
```

#### rc.local Service

```bash
# Check service status
systemctl status rc-local

# Verify service is enabled
systemctl is-enabled rc-local

# Expected output: enabled
```

#### yadm Installation

```bash
# Verify yadm is installed
which yadm

# Expected output: /usr/local/bin/yadm

# Check version
yadm --version
```

### Test Playbook

Create a test playbook to verify idempotency:

```yaml
---
- hosts: test_host
  become: true
  roles:
    - role: common

  post_tasks:
    - name: Verify timezone
      ansible.builtin.command: timedatectl show -p Timezone --value
      register: tz_check
      changed_when: false
      failed_when: tz_check.stdout != timezone

    - name: Verify GRUB configuration exists
      ansible.builtin.stat:
        path: /etc/default/grub
      register: grub_check
      failed_when: not grub_check.stat.exists

    - name: Verify rc-local service is enabled
      ansible.builtin.systemd:
        name: rc-local
      register: rclocal_check
      failed_when: rclocal_check.status.UnitFileState != "enabled"
```

Run with check mode first:

```bash
# Dry run (check mode)
ansible-playbook -i inventory test-common.yml --check

# Apply configuration
ansible-playbook -i inventory test-common.yml

# Run again to verify idempotency (should show 0 changes)
ansible-playbook -i inventory test-common.yml
```

## Troubleshooting

### GRUB Regeneration

**Problem**: Kernel parameters not applied after running the role.

**Solution**:

```bash
# Manually verify GRUB configuration
sudo cat /etc/default/grub

# Manually rebuild GRUB
sudo grub2-mkconfig -o /boot/grub2/grub.cfg

# Reboot to apply
sudo reboot

# After reboot, check active parameters
cat /proc/cmdline
```

**Common Causes**:
- GRUB rebuild handler didn't trigger (handler only runs if template changed)
- UEFI systems may use different GRUB config path
- Manual edits to `/etc/default/grub` override template

**For UEFI Systems**:

```bash
# UEFI systems use a different path
sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

# Or for RHEL/Rocky/Alma
sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
```

### Locale Problems

**Problem**: Locale not applied or locale warnings.

**Solution**:

```bash
# Check available locales
localectl list-locales

# Generate locale if missing
sudo locale-gen en_US.UTF-8

# Set locale manually
sudo localectl set-locale LANG=en_US.UTF-8

# Verify
locale
```

**Common Causes**:
- Locale not installed on system
- Locale generation handler didn't run
- Conflicting locale settings in user profile

### rc.local Not Running

**Problem**: Scripts in `/etc/rc.local` don't execute at boot.

**Solution**:

```bash
# Check if rc.local is executable
ls -l /etc/rc.local
# Should show: -rwxr-x--- (0750)

# If not executable:
sudo chmod 0750 /etc/rc.local

# Check service status
sudo systemctl status rc-local

# View service logs
sudo journalctl -u rc-local

# Test manually
sudo /etc/rc.local
```

**Common Causes**:
- `/etc/rc.local` not executable
- Errors in rc.local script prevent execution
- Service not enabled
- rc.local script missing shebang (`#!/usr/bin/env bash`)

### GRUB Background Not Displaying

**Problem**: Custom background image not showing in GRUB menu.

**Solution**:

```bash
# Verify image exists
ls -l /usr/share/backgrounds/syncopated/syncopated016.png

# Check GRUB configuration
grep GRUB_BACKGROUND /etc/default/grub

# Rebuild GRUB with verbose output
sudo grub2-mkconfig -o /boot/grub2/grub.cfg -v 2>&1 | grep -i background

# Reboot to test
sudo reboot
```

**Common Causes**:
- Image file doesn't exist at specified path
- Image format not supported (use PNG or TGA)
- Image resolution too high
- GRUB graphics mode disabled

## License

MIT-0

This role is licensed under the MIT No Attribution License, allowing unrestricted use without attribution requirements.

## Author Information

Created for RedHat family system configuration.

**Contributions**: rc.local integration adapted from [James Cherti's work](https://www.jamescherti.com/ansible-config-etc-rc-local-linux-systemd/)

---

**Related Documentation**:
- [Main Ansible Project README](/home/b08x/WorkspaceV2/RHEL/ansible/README.md)
- [GRUB2 Manual](https://www.gnu.org/software/grub/manual/grub/grub.html)
- [yadm Documentation](https://yadm.io/)
- [systemd Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
