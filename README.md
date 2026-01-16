# RHEL Workstation Configuration Management

Ansible-driven automation for RHEL-family workstations (Fedora, Rocky Linux, RHEL).
This collection enforces **consistent, reproducible, and secure** configurations for development, NAS, and RPM packaging environments.

## Core Principles

1. **Modularity**: Roles encapsulate discrete system components (e.g., `nas`, `rpm-dev`, `zsh`).
2. **Reproducibility**: Declarative YAML ensures identical outcomes across deployments.
3. **Security-First**: Hardened defaults, Ansible Vault for secrets, and explicit firewall rules.
4. **Workflow-Specific**: Tailored for RPM development, NAS configuration, and shell customization.

## Structure

```shell
ansible-rhel-workstation-builder/
├── playbooks/          # Workflow-specific automation
│   ├── rpm-dev.yml     # RPM development environment
│   ├── nas.yml         # Network-attached storage
│   └── postfix_gmail.yml # Email relay
├── roles/              # Modular system components
│   ├── common/         # Baseline configuration
│   ├── repos/          # Repository management
│   ├── rpm-dev/        # RPM toolchain
│   ├── nas/            # NFS/Samba/Rsync
│   └── zsh/            # Shell customization
├── vars/               # Encrypted/decrypted variables
├── plugins/            # Custom Ansible extensions
└── AGENTS.md           # Project knowledge base
```

## Key Roles

| Role        | Purpose                                                          | Dependencies  |
|-------------|------------------------------------------------------------------|---------------|
| **common**  | Baseline system configuration (GRUB, timezone, locale, rc.local) | None          |
| **repos**   | DNF/YUM repository management and optimization                   | None          |
| **rpm-dev** | RPM development environment (Mock, rpm-build, rpmdevtools)       | common, repos |
| **nas**     | Network-attached storage (NFS, Samba, Rsync)                     | None          |
| **zsh**     | ZSH shell customization (Oh My Zsh, plugins, themes)             | common        |

## Quick Start

### Prerequisites
- Ansible 2.9+
- Python 3.6+
- Target: Fedora 39-42, Rocky Linux 9, RHEL 9+

### Execution
```bash
# Clone repository
git clone <repository-url>
cd ansible-rhel-workstation-builder

# Install dependencies
ansible-galaxy collection install ansible.posix

# Deploy RPM development environment
ansible-playbook playbooks/rpm-dev.yml -i inventory/inventory.ini

# Deploy NAS configuration
ansible-playbook playbooks/nas.yml -i inventory/inventory.ini

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

## Workflow Integration

### RPM Development
```bash
# Initialize Mock environment
mock -r fedora-42-x86_64 --init

# Build RPM from SRPM
mock -r fedora-42-x86_64 package.src.rpm
```

### NAS Configuration
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

## Extensibility

### Custom Plugins
- **Path**: `plugins/filter/`, `plugins/callback/`
- **Configuration**: Defined in `ansible.cfg`
  ```ini
  [defaults]
  filter_plugins = ./plugins/filter:/usr/share/ansible/plugins/filter
  callback_plugins = ./plugins/callback:/usr/share/ansible/plugins/callback
  ```

### AGENTS.md
- **Purpose**: Hierarchical knowledge base for project conventions.
- **Locations**: Root, `playbooks/`, `roles/`, and role-specific directories.

## Compliance

- **Ansible Lint**: Enforce best practices.
  ```bash
  ansible-lint
  ```
- **YAML Lint**: Validate syntax.
  ```bash
  yamllint -c .yamllint.yaml .
  ```

## License

MIT-0 (No Attribution)