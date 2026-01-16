# REPOSITORY ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `repos` role manages DNF/YUM repositories and optimizes package manager configurations for Fedora and RHEL systems.

## STRUCTURE
```
roles/repos/
├── tasks/          # Repository management tasks
│   └── main.yml    # Orchestrates repository setup
├── handlers/       # Service handlers
├── vars/           # Distribution-specific variables
│   ├── Fedora.yml  # Fedora-specific package lists
│   └── RedHat.yml  # RHEL/Rocky Linux-specific package lists
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static repository files
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Repository Setup** | `tasks/main.yml` | Configures DNF/YUM repositories and optimizations |
| **Distribution-Specific Variables** | `vars/Fedora.yml`, `vars/RedHat.yml` | Fedora vs. RHEL package lists and configurations |
| **DNF Optimization** | `tasks/main.yml` | Optimizes DNF performance (e.g., fastestmirror, parallel downloads) |

## CONVENTIONS
- **Distribution-Specific Variables**: Fedora and RHEL configurations are separated (e.g., `vars/Fedora.yml`, `vars/RedHat.yml`).
- **Modular Task Files**: Tasks are organized by functionality (e.g., `main.yml` for repository setup).
- **Jinja2 Templates**: Dynamic configurations for repository files (e.g., `/etc/yum.repos.d/`).

## ANTI-PATTERNS
- **None specific to this role.**

## UNIQUE STYLES
- **Distribution-Specific Variables**: Fedora and RHEL configurations are separated for clarity.
- **DNF Optimization**: Configures fastestmirror, parallel downloads, and other performance tweaks.
- **Modular Repository Management**: Supports enabling/disabling repositories dynamically.

## NOTES
- **Dependencies**: This role is a prerequisite for `workstation` and `rpm-dev` roles.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/roles/repos/README.md`.