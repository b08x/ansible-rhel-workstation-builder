# RHEL Workstation Configuration Management

**Work In Progress**: Ansible collection for building custom Fedora/Rocky Linux workstation environments with focus on **custom ISO generation** and future **Docker/Podman application management**.

This collection provides automation for RHEL-family workstations (Fedora 43, Rocky Linux 9/10, RHEL 9+) with specialized capabilities for AI/HPC workstation images featuring NVIDIA drivers, Intel oneAPI, and hybrid desktop environments (GNOME + Sway).

## Project Status

🚧 **Active Development** - Generated using generative AI coding assistants:
- **KIWI & OSBuild Roles**: Compiled with Claude Code
- **Agent Instructions**: Generated using OpenCode/oh-my-opencode
- **Additional Edits**: Antigravity and various LLM models

**Current Focus**: Custom ISO generation (KIWI NG + OSBuild Composer)
**Future Roadmap**: Docker/Podman application lifecycle management

## Core Principles

1. **Modular Architecture**: Discrete roles for system components (`kiwi`, `osbuild`, `nas`, `rpm-dev`, `audio`, `sway`)
2. **Split-Brain Design**: Fedora 43 bleeding-edge development vs Rocky 9/10 enterprise stability
3. **Reproducibility**: Declarative YAML/TOML ensures identical outcomes across deployments
4. **AI/HPC Optimization**: First-class support for NVIDIA proprietary drivers, CUDA, Intel oneAPI
5. **Security-First**: Hardened defaults, Ansible Vault for secrets, explicit firewall rules

## Project Structure

```shell
ansible-rhel-workstation-builder/
├── playbooks/          # Workflow-specific automation
│   ├── build-kiwi-iso.yml    # Custom ISO generation (KIWI NG)
│   ├── rpm-dev.yml           # RPM development environment
│   ├── nas.yml               # Network-attached storage
│   ├── oneAPI.yml            # Intel Math Kernel Library
│   ├── docker.yml            # Container runtime
│   └── workstation.yml       # Full workstation stack
├── roles/              # Modular system components
│   ├── kiwi/           # ⭐ KIWI NG ISO builder (live ISOs, akmods)
│   ├── osbuild/        # ⭐ OSBuild Composer (blueprint-based images)
│   ├── systemd-networkd/ # ⭐ Systemd-networkd & resolved configuration
│   ├── audio/          # Low-latency audio workstation (PipeWire/JACK)
│   ├── sway/           # Wayland compositor (i3-compatible)
│   ├── common/         # Baseline system configuration
│   ├── repos/          # Repository management
│   ├── rpm-dev/        # RPM packaging toolchain
│   ├── nas/            # Network storage (NFS/Samba/Rsync)
│   ├── docker/         # Docker CE + NVIDIA Container Toolkit
│   ├── libvirt/        # Virtualization stack
│   └── zsh/            # Shell customization (Oh My Zsh)
├── vars/               # Encrypted/decrypted variables
├── plugins/            # Custom Ansible filters and callbacks
├── docs/               # Comprehensive documentation
│   ├── PLAYBOOKS.md    # Detailed playbook execution guide
│   └── VARIABLES.md    # Variable reference
└── AGENTS.md           # Hierarchical knowledge base (AI assistant context)
```

## Key Roles

### Custom ISO Generation (Primary Focus)

| Role        | Purpose                                                          | Technology Stack | Documentation |
|-------------|------------------------------------------------------------------|------------------|---------------|
| **kiwi**    | Build custom Fedora 43 live ISOs with NVIDIA/oneAPI/Sway support | KIWI NG, Jinja2 templates, akmods | [README](roles/kiwi/README.md) |
| **osbuild** | Blueprint-based Fedora Workstation images via OSBuild Composer | TOML blueprints, composer-cli | [README](roles/osbuild/README.md) |

### System Configuration Roles

| Role        | Purpose                                                          | Dependencies  |
|-------------|------------------------------------------------------------------|---------------|
| **common**  | Baseline system configuration (GRUB, timezone, locale, rc.local) | None          |
| **repos**   | DNF/YUM repository management and optimization                   | None          |
| **rpm-dev** | RPM development environment (Mock, rpm-build, rpmdevtools)       | common, repos |
| **nas**     | Network-attached storage (NFS, Samba, Rsync)                     | None          |
| **systemd-networkd** | systemd-networkd & resolved configuration               | None          |
| **audio**   | Low-latency audio workstation (PipeWire, JACK, realtime tuning)  | None          |
| **sway**    | Sway Wayland compositor for Fedora Workstation                   | None          |
| **docker**  | Docker CE with NVIDIA Container Toolkit                          | None          |
| **libvirt** | QEMU/KVM virtualization stack                                    | None          |
| **zsh**     | ZSH shell customization (Oh My Zsh, plugins, themes)             | common        |

## Quick Start

### Prerequisites
- **Operating System**: Fedora 43+ (for ISO building) or Rocky Linux 9/10 (for system configuration)
- **Ansible**: 2.14+ (2.15+ recommended)
- **Python**: 3.9+
- **Disk Space**:
  - System roles: 10GB
  - KIWI ISO builds: 50-80GB
  - OSBuild Composer: 50GB+
- **Privileges**: sudo/root access

### Install Dependencies
```bash
# Clone repository
git clone <repository-url>
cd ansible-rhel-workstation-builder

# Install Ansible collections
ansible-galaxy collection install ansible.posix community.general
```

### Build Custom ISO (Primary Use Case)

#### KIWI NG (Recommended for Live ISOs)
```bash
# Build Fedora 43 AI/HPC Workstation ISO with NVIDIA + oneAPI
ansible-playbook playbooks/build-kiwi-iso.yml

# Customize build features
ansible-playbook playbooks/build-kiwi-iso.yml \
  -e "kiwi_enable_nvidia=true" \
  -e "kiwi_enable_oneapi=true" \
  -e "kiwi_enable_sway=true"

# Template-only mode (skip build, validate configs)
ansible-playbook playbooks/build-kiwi-iso.yml -e "kiwi_execute_build=false"

# Output: /var/tmp/kiwi-output/fedora-43-ai-hybrid-*.iso
```

#### OSBuild Composer (Blueprint-based)
```bash
# Build using TOML blueprints
ansible-playbook -i inventory playbooks/osbuild-example.yml

# Output: /var/tmp/osbuild-images/<blueprint-name>-*.iso
```

### Deploy System Configurations

```bash
# RPM development environment
ansible-playbook playbooks/rpm-dev.yml

# Network-attached storage
ansible-playbook playbooks/nas.yml

# Intel oneAPI compiler suite
ansible-playbook playbooks/oneAPI.yml

# Full workstation stack
ansible-playbook playbooks/workstation.yml

# Dry run (preview changes)
ansible-playbook playbooks/rpm-dev.yml --check --diff
```

## Security

### Secrets Management
- **Ansible Vault**: Encrypt `vars/secrets.yml` for credentials.
  ```bash
  ansible-vault encrypt vars/secrets.yml
  ansible-playbook playbooks/postfix_gmail.yml --ask-vault-pass
  ```

### NAS Hardening
- **Firewalld**: Restrict NAS services to trusted networks.
  ```bash
  sudo firewall-cmd --permanent --zone=trusted --add-service={nfs,samba,rsync}
  sudo firewall-cmd --reload
  ```
- **SMB1 Deprecation**: Override default SMB1 protocol.
  ```yaml
  nas_samba_server_min_protocol: "SMB2"
  ```

## Anti-Patterns

| Anti-Pattern        | Risk                             | Solution                       |
|---------------------|----------------------------------|--------------------------------|
| Unencrypted secrets | Credential exposure              | Use Ansible Vault              |
| Hardcoded values    | Reduced reusability              | Use `vars/` or `templates/`    |
| SMB1 protocol       | Security vulnerabilities         | Override with `SMB2` or higher |
| Monolithic tasks    | Poor readability/maintainability | Split into reusable tasks      |

## Key Features & Use Cases

### Custom ISO Generation

**KIWI NG vs OSBuild Composer**: The collection includes both tools for different scenarios:

| Feature | KIWI NG | OSBuild Composer |
|---------|---------|------------------|
| **Live ISOs** | ✅ Native support | ❌ Limited |
| **Akmods (NVIDIA)** | ✅ Full support | ⚠️ Challenging |
| **Flexibility** | ✅ High (XML/Jinja2) | ⚠️ Blueprint constraints |
| **Multi-distro** | ✅ Yes | ❌ Red Hat ecosystem only |
| **Build Speed** | ~45-90 min | ~60-120 min |
| **Best For** | Live ISOs, AI/HPC workstations | Standard Fedora variants, servers |

**When to use KIWI**: Custom live ISOs, NVIDIA driver compilation, hybrid desktops
**When to use OSBuild**: RHEL/CentOS compatibility, standard Fedora variants

### Split-Brain Design: Fedora vs Rocky

The collection maintains parallel support for:

- **Fedora 43 (Bleeding Edge)**: KIWI/OSBuild ISO generation, latest GNOME, Sway, oneAPI
- **Rocky Linux 9/10 (Enterprise)**: System configuration roles, stable package versions

This allows testing cutting-edge features on Fedora while deploying stable configs to Rocky production systems.

### AI/HPC Workstation Configuration

Out-of-the-box support for:
- **NVIDIA Drivers**: Proprietary drivers via akmods (auto-compile on first boot)
- **CUDA Toolkit**: GPU-accelerated computing
- **Intel oneAPI**: DPC++, MKL, optimized math libraries
- **Container GPU Passthrough**: Podman + NVIDIA Container Toolkit with CDI
- **Hybrid Desktop**: GNOME 49 + Sway tiling WM for Wayland workflows

### Workflow Examples

#### RPM Development
```bash
# Deploy development environment
ansible-playbook playbooks/rpm-dev.yml

# Initialize Mock environment
mock -r fedora-43-x86_64 --init

# Build RPM from SRPM
mock -r fedora-43-x86_64 package.src.rpm
```

#### NAS Configuration
```yaml
- hosts: nas_server
  roles:
    - role: nas
      vars:
        nas_enable_nfs: true
        nas_enable_samba: true
        nas_nfs_exports:
          - path: /srv/nfs
            create_dir: true
```

#### Low-Latency Audio Workstation
```bash
# Deploy PipeWire + JACK + realtime tuning
ansible-playbook playbooks/audio.yml
```

## Documentation

### Comprehensive Guides

- **[PLAYBOOKS.md](docs/PLAYBOOKS.md)**: Detailed execution guide for all playbooks with troubleshooting
- **[VARIABLES.md](docs/VARIABLES.md)**: Complete variable reference for roles
- **Role-Specific READMEs**:
  - [kiwi/README.md](roles/kiwi/README.md) - KIWI NG ISO builder
  - [osbuild/README.md](roles/osbuild/README.md) - OSBuild Composer
  - [audio/README.md](roles/audio/README.md) - Low-latency audio workstation
  - [nas/README.md](roles/nas/README.md) - Network storage services
  - [systemd-networkd/README.md](roles/systemd-networkd/README.md) - Systemd-networkd configuration
  - [docker/README.md](roles/docker/README.md) - Container runtime
  - [sway/README.md](roles/sway/README.md) - Wayland compositor

### AGENTS.md Knowledge Base

The collection includes hierarchical `AGENTS.md` files providing context for AI coding assistants:
- **Purpose**: Project conventions, architectural decisions, anti-patterns
- **Locations**: Root, `playbooks/`, `roles/`, and role-specific directories
- **Usage**: Generated using OpenCode/oh-my-opencode for consistent LLM context

## Extensibility

### Custom Plugins
- **Path**: `plugins/filter/`, `plugins/callback/`
- **Configuration**: Defined in `ansible.cfg`
  ```ini
  [defaults]
  filter_plugins = ./plugins/filter:/usr/share/ansible/plugins/filter
  callback_plugins = ./plugins/callback:/usr/share/ansible/plugins/callback
  ```

### Adding Custom Blueprints (OSBuild)
```bash
# Create blueprint
cp roles/osbuild/files/fedora-43/x86_64/workstation/example.toml my-blueprint.toml
# Edit and deploy
ansible-playbook -i inventory playbooks/osbuild-example.yml -e "static_blueprint_path=my-blueprint.toml"
```

### Extending KIWI Templates
```yaml
# Override package lists
kiwi_extra_packages:
  - my-custom-package
  - another-tool
```

## Compliance

- **Ansible Lint**: Enforce best practices.
  ```bash
  ansible-lint
  ```
- **YAML Lint**: Validate syntax.
  ```bash
  yamllint -c .yamllint.yaml .
  ```

## Testing & Validation

### ISO Testing
```bash
# Test KIWI-generated ISO in QEMU
qemu-system-x86_64 \
  -m 8G \
  -enable-kvm \
  -boot d \
  -cdrom /var/tmp/kiwi-output/fedora-43-ai-hybrid-*.iso

# Flash to USB drive
sudo dd if=/var/tmp/kiwi-output/*.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

### Role Testing
```bash
# Validate role syntax
ansible-playbook roles/kiwi/tests/test.yml

# Dry-run mode
ansible-playbook playbooks/build-kiwi-iso.yml --check --diff

# Verbose debugging
ansible-playbook playbooks/rpm-dev.yml -vvv
```

## Known Issues & Limitations

### NVIDIA First Boot
⚠️ **Black screen for 2-5 minutes on first boot** - Normal behavior! Akmods is compiling NVIDIA kernel modules. Switch to TTY2 (Ctrl+Alt+F2) to monitor with `sudo journalctl -fu akmods`.

### Secure Boot
NVIDIA akmod drivers are unsigned. Options:
1. Disable Secure Boot (easiest)
2. Enroll Machine Owner Key (MOK) during first boot
3. Use pre-signed kmod packages (not yet implemented)

### DNF5 Instability
Fedora 43+ mandates DNF5, which can have intermittent package download failures. Roles include retry logic (3 attempts).

### Disk Space
KIWI + OSBuild builds require significant space:
- KIWI: 50-80GB (80GB with oneAPI in image)
- OSBuild: 50GB minimum
- Both active: 100GB+

## Roadmap

### Current Focus (v1.x)
- ✅ KIWI NG ISO generation
- ✅ OSBuild Composer integration
- ✅ NVIDIA driver support (akmods)
- ✅ Intel oneAPI integration
- ✅ Hybrid desktop (GNOME + Sway)
- 🚧 Audio workstation role refinement

### Future (v2.x)
- 🔜 Docker/Podman application management
- 🔜 Container-based app lifecycle automation
- 🔜 Kubernetes/OpenShift integration
- 🔜 Immutable OS variants (OSTree/rpm-ostree)

## Contributing

This is a personal learning project demonstrating AI-assisted Ansible development. Contributions, suggestions, and feedback are welcome via issues or pull requests.

**Note**: Much of this codebase was generated using AI coding assistants (Claude Code, Antigravity, OpenCode), making it an interesting case study in LLM-driven infrastructure-as-code development.

## License

MIT-0 (No Attribution)