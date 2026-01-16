# ROLES KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `roles/` directory contains modular, self-contained components for Ansible automation, each targeting a specific system configuration or service.

## STRUCTURE
```
roles/
├── common/         # System baseline configuration (GRUB, timezone, locale, YADM)
├── nas/            # Network-attached storage (NFS, Samba, Rsync)
├── repos/          # Repository management and DNF optimization (Fedora/RHEL)
├── rpm-dev/        # RPM development environment (Mock, rpm-build, rpmdevtools)
├── workstation/    # Linux workstation setup (applications, development tools)
├── zsh/            # ZSH shell customization (Oh My Zsh, plugins, themes)
├── osbuild/        # OSBuild integration (placeholder)
└── libvirt/        # Libvirt virtualization management (placeholder)
```

## WHERE TO LOOK
| Role | Purpose | Key Files |
|------|---------|-----------|
| **common** | System baseline (GRUB, timezone, locale, rc.local, YADM) | `tasks/rclocal.yml`, `tasks/grub.yml`, `tasks/yadm.yml` |
| **nas** | Network storage (NFS, Samba, Rsync) | `tasks/nfs/config.yml`, `tasks/samba/config.yml`, `templates/` |
| **repos** | Repository management (DNF/YUM) | `vars/Fedora.yml`, `vars/RedHat.yml`, `tasks/main.yml` |
| **rpm-dev** | RPM development environment | `files/etc/mock/templates/`, `tasks/main.yml` |
| **workstation** | Linux workstation setup | `tasks/google-chrome.yml`, `tasks/rust_utils.yml`, `tasks/rpmfusion.yml` |
| **zsh** | ZSH shell customization | `files/usr/share/oh-my-zsh/plugins/`, `tasks/zsh.yml` |
| **osbuild** | OSBuild integration | Placeholder |
| **libvirt** | Libvirt virtualization | Placeholder |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `google-chrome.yml`, `rclocal.yml`).
- **Role-Specific Variables**: Variables are scoped to roles (e.g., `roles/repos/vars/Fedora.yml`).
- **Jinja2 Templates**: Dynamic configurations (e.g., `roles/nas/templates/`).
- **Non-Standard Task Names**: Task files named after components/tools (e.g., `rust_utils.yml` instead of `development_tools.yml`).
- **Custom Plugins**: Roles may leverage custom plugins (e.g., filters, callbacks).

## ANTI-PATTERNS
- **Non-Standard Directories**: Templates should not be nested in `files/` (e.g., `roles/rpm-dev/files/etc/mock/templates/`).
- **Redundant Includes**: Avoid including the same task file multiple times.

## UNIQUE STYLES
- **Component-Specific Task Files**: Tasks are organized by component/tool (e.g., `google-chrome.yml`, `rpmfusion.yml`).
- **Distribution-Specific Variables**: Fedora vs. RHEL package lists (e.g., `roles/repos/vars/Fedora.yml`).
- **Custom Plugin Usage**: Roles may use custom plugins defined in `plugins/`.
- **Modular Includes**: Reusable tasks via `include_tasks` (e.g., `roles/common/tasks/main.yml`).

## NOTES
- **Dependencies**: Some roles depend on others (e.g., `workstation` requires `common` and `repos`).
- **Security**: NAS role has security implications (NFS/Samba/Rsync). Restrict to trusted networks.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/` (e.g., `roles/nas/README.md`).