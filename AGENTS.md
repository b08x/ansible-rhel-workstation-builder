# ANSIBLE KNOWLEDGE BASE

**Generated:** 07:26:41 AM (America/New_York)
**Commit:** 8940810
**Branch:** development

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
| **Audio Production** | `roles/audio/` | PipeWire, JACK, audio applications (97 app desktop files) |
| **ISO Generation** | `roles/kiwi/` | KIWI NG image building (complex async logic) |
| **Repositories** | `roles/repos/` | DNF/YUM repository management (Fedora/RHEL-specific) |
| **ZSH** | `roles/zsh/` | Oh-My-Zsh, custom plugins, themes |
| **Variables** | `vars/` | Unencrypted secrets (anti-pattern), distro-specific vars |
| **Plugins** | `plugins/` | Custom modules, filters, callbacks (defined in `ansible.cfg`) |

## CONVENTIONS
- **YAML Style**: 2-space indentation (Ansible standard).
- **Non-Standard Playbook Names**: Playbooks target specific use cases (e.g., `oneAPI.yml`, `postfix_gmail.yml`).
- **Non-Standard Task Files**: Task files named after components/tools (e.g., `google-chrome.yml`, `rclocal.yml`).
- **Modular Task Includes**: Uses `include_tasks` for dynamic task loading.
- **Custom Plugin Paths**: No explicit paths in `ansible.cfg` (commented out).

## ANTI-PATTERNS (THIS PROJECT)
- **Unencrypted secrets**: `vars/secrets.yml` contains plaintext credentials (CRITICAL)
- **SMB1/NTLMv1**: Deprecated protocols enabled in `roles/nas/defaults/main.yml`
- **Empty passwords**: Default passwords in `roles/kiwi/` and `roles/osbuild/`
- **Privilege escalation**: Docker/libvirt group membership grants root-equivalent access
- **Templates in files/**: `roles/rpm-dev/files/etc/mock/templates/` violates conventions
- **Stdout parsing**: Error detection via stdout parsing (unreliable)

## UNIQUE STYLES
- **Modular Roles**: Each role (e.g., `nas`, `workstation`) is self-contained with distinct conventions.
- **Jinja2 Templates**: Dynamic configurations (e.g., `roles/nas/templates/`).
- **Task Includes**: Reusable tasks via `include_tasks` (e.g., `roles/common/tasks/`).
- **Distribution-Specific Variables**: Fedora vs. RHEL package lists (e.g., `roles/repos/vars/Fedora.yml`).
- **Deep File Structures**: Audio role has 97 desktop files in `roles/audio/files/home/local/share/applications/`
- **Async Build Logic**: KIWI role uses complex async patterns for image building
- **Component-Specific Tasks**: Tasks named after tools (e.g., `google-chrome.yml`, `noisetorch.yml`)

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

# Lint check
ansible-lint
yamllint -c .yamllint.yaml .
```

## NOTES
- **Security**: NAS role exposes NFS/Samba/Rsync. Restrict to trusted networks and use firewalld.
- **Gmail App Passwords**: Required for `postfix_gmail.yml`. Enable 2FA and generate an App Password.
- **SMB1 Deprecation**: Override default SMB1 protocol in production.
- **Large Files**: Several files >100 lines indicate complexity hotspots (especially `roles/kiwi/tasks/build.yml` at 280 lines).
- **Project Scale**: 519 files, 6602 YAML lines, depth 9 - significant complexity requiring careful navigation.