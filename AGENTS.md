# ANSIBLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)
**Commit:** N/A (No Git repo detected)
**Branch:** N/A

---

## OVERVIEW
This Ansible project automates Linux workstation provisioning, NAS configuration, and RPM development environments for RHEL-family systems (Fedora, Rocky Linux, RHEL). It uses modular roles, playbooks, and custom plugins for extensibility.

## STRUCTURE
```
./
├── playbooks/          # Top-level automation scripts (non-standard names)
├── roles/              # Modular roles (common, nas, repos, rpm-dev, workstation, zsh)
├── vars/               # Global variables (unencrypted secrets anti-pattern)
├── plugins/            # Custom Ansible plugins (modules, filters, callbacks)
├── inventory/          # Inventory files (non-standard location)
├── docs/               # Project documentation
├── ansible.cfg         # Custom plugin paths, fact caching, SSH optimization
├── .ansible-lint       # Custom linting rules (skips best practices)
└── .yamllint.yaml      # YAML formatting rules
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Playbooks** | `playbooks/` | Non-standard names (e.g., `jacktrip-pi.yml`, `postfix_gmail.yml`) |
| **NAS Setup** | `roles/nas/` | NFS, Samba, Rsync configurations (security implications) |
| **Workstation** | `roles/workstation/` | Application installs (non-standard task files) |
| **RPM Dev** | `roles/rpm-dev/` | Mock templates, RPM build environment (non-standard dir structure) |
| **Repositories** | `roles/repos/` | DNF/YUM repository management (Fedora/RHEL-specific) |
| **ZSH** | `roles/zsh/` | Oh-My-Zsh, custom plugins, themes |
| **Variables** | `vars/` | Unencrypted secrets (anti-pattern), distro-specific vars |
| **Plugins** | `plugins/` | Custom modules, filters, callbacks (defined in `ansible.cfg`) |

## CONVENTIONS
- **YAML Style**: 2-space indentation (Ansible standard).
- **Non-Standard Playbook Names**: Playbooks target specific use cases (e.g., `oneAPI.yml`, `postfix_gmail.yml`).
- **Non-Standard Task Files**: Task files named after components/tools (e.g., `google-chrome.yml`, `rclocal.yml`).
- **Custom Plugin Paths**: Defined in `ansible.cfg` (e.g., `./plugins/filter:/usr/share/ansible/plugins/filter`).

## UNIQUE STYLES
- **Modular Roles**: Each role (e.g., `nas`, `workstation`) is self-contained with distinct conventions.
- **Jinja2 Templates**: Dynamic configurations (e.g., `roles/nas/templates/`).
- **Task Includes**: Reusable tasks via `include_tasks` (e.g., `roles/common/tasks/`).
- **Custom Plugins**: Project-specific modules, filters, and callbacks (defined in `ansible.cfg`).
- **Distribution-Specific Variables**: Fedora vs. RHEL package lists (e.g., `roles/repos/vars/Fedora.yml`).
- **Non-Standard Directory Structure**: `roles/rpm-dev/files/etc/mock/templates/` (templates nested in `files/`).

## COMMANDS
```bash
# Run a playbook
ansible-playbook playbooks/<playbook>.yml -i inventory/inventory.ini

# Syntax check
ansible-playbook --syntax-check playbooks/<playbook>.yml

# Dry run
ansible-playbook -C playbooks/<playbook>.yml -i inventory/inventory.ini

# Encrypt secrets with Ansible Vault
ansible-vault encrypt vars/secrets.yml

# Run playbook with vault password
ansible-playbook playbooks/postfix_gmail.yml --ask-vault-pass
```

## NOTES
- **Security**: NAS role exposes NFS/Samba/Rsync. Restrict to trusted networks and use firewalld.
- **Gmail App Passwords**: Required for `postfix_gmail.yml`. Enable 2FA and generate an App Password.
- **SMB1 Deprecation**: Override default SMB1 protocol in production.
- **Custom Plugins**: Defined in `ansible.cfg`. Ensure compatibility with Ansible 2.9+.