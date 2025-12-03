# Repository Management Role

This Ansible role **transforms** RHEL-family systems by configuring DNF package manager optimization settings and establishing third-party repository access. It provides intelligent, distribution-specific repository setup with comprehensive error handling and performance tuning.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Task Breakdown](#task-breakdown)
- [Handlers](#handlers)
- [Dependencies](#dependencies)
- [Example Playbooks](#example-playbooks)
- [Distribution-Specific Usage](#distribution-specific-usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Author Information](#author-information)

## Features

### DNF Performance Optimization

- **Parallel downloads**: Configures DNF to download up to 10 packages simultaneously, significantly reducing installation time
- **Fastest mirror selection**: Enables automatic selection of the quickest repository mirrors based on network latency
- **Dependency cleanup**: Automatically removes unused dependencies when packages are removed, reducing disk usage

### Third-Party Repository Support

- **EPEL (Extra Packages for Enterprise Linux)**: Provides access to thousands of additional packages
- **PowerTools/CRB**: Enables CodeReady Builder repository for development packages
- **RPM Fusion**: Adds Free and Non-Free repositories for multimedia and proprietary software
- **Distribution-specific repositories**: Fedora Workstation repos, Google Chrome, and more

### Intelligent Distribution Detection

- **Fedora configuration**: Optimized for Fedora with Workstation-specific repositories
- **Rocky/RHEL configuration**: Tailored setup for Enterprise Linux distributions
- **Automatic version detection**: Uses `ansible_distribution_major_version` for version-specific repository URLs

### Robust Error Handling

- **Graceful degradation**: System remains functional even if repository setup encounters issues
- **Detailed error logging**: Provides actionable error messages for troubleshooting
- **Fallback strategies**: Continues with default settings if optimizations fail

## Requirements

- **Ansible Version**: 2.9 or higher
- **Supported Distributions**:
  - Fedora 38+
  - Rocky Linux 8, 9
  - RHEL 8, 9
  - AlmaLinux 8, 9
- **Collections**: None (uses only `ansible.builtin` modules)
- **Privileges**: Requires `become: true` (root privileges) for DNF configuration and repository management

## Role Variables

### General Repository Settings

Available in `defaults/main.yml`:

```yaml
# Enable or disable third-party repository configuration
enable_third_party_repos: true

# Network timeout for repository operations (seconds)
network_timeout: 30

# Number of retry attempts for failed repository operations
retry_count: 3
```

### RHEL-Specific Repository Toggles

```yaml
# Enable EPEL repository (Extra Packages for Enterprise Linux)
enable_epel: true

# Enable PowerTools (Rocky 8) or CRB/CodeReady Builder (Rocky 9+)
enable_powertools: true

# Enable RPM Fusion Free and Non-Free repositories
enable_rpmfusion: true
```

### DNF Configuration Settings

These settings are applied automatically via `/etc/dnf/dnf.conf`:

| Setting | Value | SFL Process Analysis |
|---------|-------|---------------------|
| `fastestmirror` | `1` | **Material Process**: Enables automatic selection of the fastest repository mirror, reducing download times |
| `max_parallel_downloads` | `10` | **Material Process**: Allows 10 simultaneous package downloads, significantly improving installation speed |
| `clean_requirements_on_remove` | `True` | **Material Process**: Removes unused dependencies when packages are uninstalled, maintaining system cleanliness |

## Task Breakdown

### 1. DNF Performance Optimization

**Material Process**: **Transforms** the DNF configuration file (`/etc/dnf/dnf.conf`) by inserting or updating performance optimization directives.

- **Participants**: `/etc/dnf/dnf.conf` file, DNF configuration variables
- **Circumstances**: Creates backup before modification; uses `block/rescue` pattern for error handling
- **Modality**: **Ensures** settings are applied; **may fail** if file permissions are incorrect

**Tag**: `dnf_configuration`, `dnf_config`

### 2. Distribution-Specific Repository Configuration

**Relational Process**: **Includes** distribution-specific task files based on `ansible_distribution` fact.

#### Fedora Repository Setup (`tasks/fedora.yml`)

**Material Processes**:

1. **Installs** prerequisite packages:
   - `python3-libdnf5`: Modern DNF API library
   - `fedora-workstation-repositories`: Repository management utilities

2. **Installs** RPM Fusion repositories:
   - RPM Fusion Free: Open-source multimedia and software
   - RPM Fusion Non-Free: Proprietary drivers and codecs
   - Uses version-specific URLs: `rpmfusion-free-release-{{ ansible_distribution_major_version }}.noarch.rpm`

3. **Enables** Google Chrome repository via `dnf config-manager`

4. **Configures** repository priorities:
   - RPM Fusion priority: 40 (lower priority than system repos)

**Circumstances**: Only executes when `ansible_distribution == "Fedora"` and `enable_third_party_repos == true`

#### Rocky/RHEL Repository Setup (`tasks/rocky.yml`)

**Material Processes**:

1. **Installs** EPEL repository:
   - Package: `epel-release`
   - Provides thousands of additional packages for Enterprise Linux

2. **Enables** PowerTools/CRB repository:
   - Rocky 8: `powertools`
   - Rocky 9+: `crb` (CodeReady Builder)
   - Provides development headers and build dependencies

3. **Enables** additional repositories:
   - `plus`: Additional packages
   - `rt`: Real-time kernel packages

4. **Installs** RPM Fusion repositories:
   - Enterprise Linux-specific URLs: `rpmfusion-free-release-{{ ansible_distribution_major_version }}.noarch.rpm`

5. **Configures** repository priorities:
   - Base OS repositories: priority 10 (highest)
   - EPEL/RT: priority 20
   - PowerTools/CRB/Plus: priority 30
   - RPM Fusion: priority 40 (lowest)

**Circumstances**: Only executes when `ansible_distribution == "Rocky"` (also applies to RHEL/AlmaLinux) and `enable_third_party_repos == true`

**Tags**: `repos`, `repositories`, `epel`, `powertools`, `crb`, `rpmfusion`, `repo_priorities`

### 3. Package Cache Management

**Material Process**: **Refreshes** the DNF package cache to ensure repository metadata is current.

- **Participants**: DNF package cache, repository metadata
- **Circumstances**: Executed after repository configuration
- **Modality**: **Attempts** to refresh cache; **may fail** if network connectivity issues exist
- **Error Handling**: Logs failure and provides manual remediation command

**Tag**: `cache`, `cache_update`

## Handlers

### Update cache

**Material Process**: **Refreshes** DNF package cache when repository configuration changes.

```yaml
- name: Update cache
  ansible.builtin.dnf:
    update_cache: true
  listen: "Update cache"
```

**Trigger**: Notified by repository configuration tasks when changes are made.

## Dependencies

**None**. This role has no dependencies on other Ansible roles.

## Example Playbooks

### Basic Usage with Defaults

```yaml
---
- name: Configure system repositories
  hosts: workstations
  become: true
  roles:
    - repos
```

**Process**: Installs all third-party repositories with default settings for the detected distribution.

### Fedora with Selective Repository Configuration

```yaml
---
- name: Configure Fedora repositories
  hosts: fedora_systems
  become: true
  vars:
    enable_third_party_repos: true
    enable_rpmfusion: true
  roles:
    - repos
```

**Process**: Enables RPM Fusion repositories on Fedora systems while using default DNF optimizations.

### RHEL without RPM Fusion

```yaml
---
- name: Configure RHEL with EPEL only
  hosts: rhel_servers
  become: true
  vars:
    enable_third_party_repos: true
    enable_epel: true
    enable_powertools: true
    enable_rpmfusion: false  # Disable RPM Fusion for servers
  roles:
    - repos
```

**Process**: Sets up EPEL and PowerTools/CRB but excludes RPM Fusion repositories.

### Tag-Based Execution

```bash
# Configure DNF settings only
ansible-playbook playbook.yml --tags "dnf_configuration"

# Set up repositories without DNF optimization
ansible-playbook playbook.yml --tags "repos"

# Refresh package cache only
ansible-playbook playbook.yml --tags "cache"

# Configure only EPEL repository
ansible-playbook playbook.yml --tags "epel"

# Set up RPM Fusion repositories only
ansible-playbook playbook.yml --tags "rpmfusion"
```

## Distribution-Specific Usage

### Fedora Considerations

**Material Processes Applied**:

1. Installs `fedora-workstation-repositories` for additional repository management
2. Configures RPM Fusion Free and Non-Free using Fedora-specific URLs
3. Enables Google Chrome repository via `dnf config-manager`
4. Sets RPM Fusion priority to 40

**Important**: Fedora versions update rapidly. Ensure `ansible_distribution_major_version` correctly detects your Fedora version (38, 39, 40, 41, 42, etc.).

**Repository Priority Strategy**:
- Fedora Base repositories: Default priority (typically 50)
- RPM Fusion: Priority 40 (lower number = higher priority in DNF)

### RHEL/Rocky/AlmaLinux Considerations

**Material Processes Applied**:

1. Installs EPEL repository via `epel-release` package
2. Enables PowerTools (RHEL 8, Rocky 8) or CRB (RHEL 9+, Rocky 9+)
3. Enables additional repositories: `plus`, `rt`
4. Configures RPM Fusion using Enterprise Linux-specific URLs
5. Sets comprehensive repository priority hierarchy

**Important**:
- **PowerTools vs CRB**: Rocky 8 uses `powertools`, Rocky 9+ uses `crb`. The role automatically tries both with fallback logic.
- **EPEL Requirement**: Many packages in PowerTools/CRB depend on EPEL packages. Always enable EPEL when enabling PowerTools/CRB.

**Repository Priority Strategy**:
- Base OS (baseos, appstream): Priority 10 (highest)
- EPEL, RT: Priority 20
- PowerTools/CRB, Plus: Priority 30
- RPM Fusion: Priority 40 (lowest)

This ensures system stability by preferring official repositories over third-party sources.

### Version-Specific Repository URLs

The role uses `ansible_distribution_major_version` to construct repository URLs:

```yaml
# Fedora RPM Fusion URL
https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{{ ansible_distribution_major_version }}.noarch.rpm

# RHEL/Rocky RPM Fusion URL
https://download1.rpmfusion.org/free/el/rpmfusion-free-release-{{ ansible_distribution_major_version }}.noarch.rpm
```

**Verification Command**:

```bash
ansible -m setup -a 'filter=ansible_distribution*' localhost
```

## Testing

### Verification Commands

After running this role, verify the configuration:

#### Check DNF Configuration

```bash
# View DNF settings
cat /etc/dnf/dnf.conf | grep -E "fastestmirror|max_parallel_downloads|clean_requirements"

# Expected output:
# fastestmirror=1
# max_parallel_downloads=10
# clean_requirements_on_remove=True
```

#### Verify Repository List

```bash
# List all enabled repositories
dnf repolist

# Check specific repositories (Fedora)
dnf repolist | grep -E "rpmfusion|google-chrome"

# Check specific repositories (RHEL/Rocky)
dnf repolist | grep -E "epel|powertools|crb|rpmfusion"
```

#### Test Repository Priorities

```bash
# View repository configuration with priorities
dnf config-manager --dump | grep -E "^\[|^priority"
```

#### Verify Repository Metadata

```bash
# Test repository connectivity and metadata download
dnf clean all
dnf makecache

# Should complete without errors if repositories are correctly configured
```

### Expected Repository State

#### Fedora Systems

```
rpmfusion-free                 RPM Fusion for Fedora 42 - Free
rpmfusion-free-updates         RPM Fusion for Fedora 42 - Free - Updates
rpmfusion-nonfree              RPM Fusion for Fedora 42 - Nonfree
rpmfusion-nonfree-updates      RPM Fusion for Fedora 42 - Nonfree - Updates
google-chrome                  google-chrome
```

#### Rocky/RHEL Systems

```
baseos                         Rocky Linux 9 - BaseOS
appstream                      Rocky Linux 9 - AppStream
epel                           Extra Packages for Enterprise Linux 9
crb                            Rocky Linux 9 - CRB (CodeReady Builder)
plus                           Rocky Linux 9 - Plus
rpmfusion-free                 RPM Fusion for EL 9 - Free
rpmfusion-nonfree              RPM Fusion for EL 9 - Nonfree
```

### Functionality Tests

#### Test Parallel Downloads

```bash
# Install multiple packages and observe parallel downloads
dnf install -y htop iotop iftop vim-enhanced

# You should see multiple download progress bars simultaneously
```

#### Test Fastest Mirror

```bash
# Force metadata refresh to trigger mirror selection
dnf clean metadata
dnf makecache

# Check DNF logs for mirror selection
grep -i "fastest" /var/log/dnf.log
```

#### Test EPEL Package Installation (RHEL/Rocky)

```bash
# Install a package only available in EPEL
dnf info htop

# Should show repository: epel
```

## Troubleshooting

### Common Issues

#### Issue: DNF Configuration Not Applied

**Symptoms**:
- `/etc/dnf/dnf.conf` unchanged after role execution
- `dnf_config_failed` fact is set to `true`

**Possible Causes**:
- Insufficient file permissions
- SELinux context preventing file modification
- File is immutable (`chattr +i`)

**Resolution**:

```bash
# Check file permissions
ls -lZ /etc/dnf/dnf.conf

# Check if file is immutable
lsattr /etc/dnf/dnf.conf

# Remove immutable flag if present
chattr -i /etc/dnf/dnf.conf

# Restore SELinux context
restorecon -v /etc/dnf/dnf.conf

# Re-run the role
ansible-playbook playbook.yml --tags "dnf_configuration"
```

#### Issue: Repository Installation Failed

**Symptoms**:
- `repository_setup_failed` fact is set to `true`
- Error message: "Failed to set up repositories"

**Possible Causes**:
- Network connectivity issues
- Repository GPG key problems
- Incorrect distribution version detection
- Repository URLs are unreachable

**Resolution**:

```bash
# Test network connectivity
curl -I https://download1.rpmfusion.org/

# Verify distribution detection
ansible -m setup -a 'filter=ansible_distribution*' localhost

# Manually install repository (example for Fedora 42)
sudo dnf install -y \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-42.noarch.rpm

# Check for GPG key errors
sudo dnf config-manager --dump | grep gpgcheck
```

#### Issue: PowerTools/CRB Repository Not Found

**Symptoms**:
- Error: "Error: Unknown repo: 'powertools'" or "Error: Unknown repo: 'crb'"

**Possible Causes**:
- Distribution version mismatch (Rocky 8 vs Rocky 9)
- Repository name variation

**Resolution**:

The role includes fallback logic, but you can verify manually:

```bash
# List all available repositories (including disabled)
dnf repolist --all

# Rocky 8 - Enable PowerTools
sudo dnf config-manager --set-enabled powertools

# Rocky 9+ - Enable CRB
sudo dnf config-manager --set-enabled crb
```

#### Issue: Network Timeout During Repository Setup

**Symptoms**:
- Operations hang or timeout during repository configuration
- "Failed to download metadata" errors

**Resolution**:

Adjust network timeout and retry settings:

```yaml
- hosts: servers
  become: true
  vars:
    network_timeout: 60      # Increase timeout to 60 seconds
    retry_count: 5           # Increase retry attempts
  roles:
    - repos
```

Or manually refresh cache:

```bash
# Clear all cached metadata
sudo dnf clean all

# Rebuild cache with verbose output
sudo dnf makecache --verbose

# If specific repository fails, disable it temporarily
sudo dnf config-manager --set-disabled <repository-name>
```

#### Issue: Package Cache Update Failed

**Symptoms**:
- Role completes but displays "Failed to update package cache"
- Suggests running `dnf clean all && dnf makecache` manually

**Resolution**:

```bash
# Execute the suggested command
sudo dnf clean all && sudo dnf makecache

# If persistent, check repository configurations
sudo dnf config-manager --dump

# Test each repository individually
sudo dnf repolist --verbose
```

### Repository Safety Warnings

#### Third-Party Repository Risks

**Important**: Third-party repositories **may introduce** package conflicts and stability issues.

- **Package Conflicts**: RPM Fusion packages **might conflict** with official repository packages
- **Security Considerations**: Third-party packages **may not receive** the same security auditing as official packages
- **Stability vs Features**: Enabling third-party repos provides access to newer software but **could introduce** system instability

**Best Practices**:

1. **Enable selectively**: Only enable repositories you actively need
2. **Use repository priorities**: The role configures priorities to prefer official packages
3. **Monitor updates**: Review package updates before applying them in production
4. **Test before deployment**: Verify third-party packages in a test environment

```yaml
# Conservative server configuration (production)
- hosts: production_servers
  become: true
  vars:
    enable_epel: true           # Safe, well-maintained
    enable_powertools: true     # Official repository
    enable_rpmfusion: false     # Avoid on production servers
  roles:
    - repos

# Permissive workstation configuration (development)
- hosts: developer_workstations
  become: true
  vars:
    enable_third_party_repos: true  # Enable all repositories
  roles:
    - repos
```

### Error Handling and Logging

The role uses **block/rescue** patterns for comprehensive error handling:

**When DNF configuration fails**:
- Sets fact: `dnf_config_failed: true`
- Logs error details to Ansible output
- System **continues functioning** with default DNF settings

**When repository setup fails**:
- Sets fact: `repository_setup_failed: true`
- Logs detailed error message with troubleshooting hints
- System **remains operational** with existing repositories

**When cache update fails**:
- Logs error with manual remediation command
- Suggests: `dnf clean all && dnf makecache`

**Check for failures after role execution**:

```yaml
- name: Check for configuration failures
  ansible.builtin.debug:
    msg: "Warning: {{ item }} failed"
  when: hostvars[inventory_hostname][item] | default(false)
  loop:
    - dnf_config_failed
    - repository_setup_failed
```

## License

**MIT-0** (MIT No Attribution)

This role is released under the MIT-0 license, allowing unrestricted use without attribution requirements.

## Author Information

This role was created for comprehensive repository management across RHEL-family distributions, with a focus on performance optimization, distribution-specific configuration, and robust error handling.

For issues, suggestions, or contributions, please refer to the project repository.

---

## Cross-References

- **Main Documentation**: See [Main README](/home/b08x/WorkspaceV2/RHEL/ansible/README.md) for project overview
- **Related Roles**:
  - `common`: Base system configuration (should run before this role)
  - `rpm-dev`: RPM development environment (requires repositories configured by this role)
- **Variable Documentation**: For advanced variable configuration, see the [defaults/main.yml](/home/b08x/WorkspaceV2/RHEL/ansible/roles/repos/defaults/main.yml) file

## Quick Reference Commands

```bash
# Apply role to all systems
ansible-playbook -i inventory site.yml --tags "repos"

# Configure only DNF optimization
ansible-playbook -i inventory site.yml --tags "dnf_configuration"

# Set up repositories without cache refresh
ansible-playbook -i inventory site.yml --tags "repos" --skip-tags "cache"

# Verify repository configuration
ansible all -m shell -a "dnf repolist"

# Check DNF configuration
ansible all -m shell -a "grep -E 'fastestmirror|max_parallel' /etc/dnf/dnf.conf"
```
