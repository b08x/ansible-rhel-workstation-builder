# RPM DEVELOPMENT ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `rpm-dev` role sets up a complete RPM development environment, including Mock, rpm-build, rpmdevtools, and other packaging tools for Fedora/RHEL.

## STRUCTURE
```
roles/rpm-dev/
├── tasks/          # RPM development tasks
│   ├── main.yml    # Orchestrates task includes
│   ├── packages.yml # Installs RPM toolchain
│   └── config.yml  # Configures Mock and build environment
├── handlers/       # Service handlers
├── templates/      # Jinja2 templates for Mock configs
├── vars/           # Role-specific variables
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static files
    └── etc/mock/templates/  # Non-standard directory for Mock templates
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **RPM Toolchain** | `tasks/packages.yml` | Installs Mock, rpm-build, rpmdevtools, etc. |
| **Mock Configuration** | `tasks/config.yml` | Configures Mock for clean builds |
| **Templates** | `templates/` | Jinja2 templates for Mock configs (e.g., `mock.cfg.j2`) |
| **Non-Standard Directory** | `files/etc/mock/templates/` | Mock templates (non-standard location) |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `packages.yml`, `config.yml`).
- **Jinja2 Templates**: Dynamic configurations for Mock (e.g., `templates/mock.cfg.j2`).
- **Non-Standard Directory**: Mock templates are stored in `files/etc/mock/templates/` (unusual for Ansible).
- **Role Dependencies**: Requires `common` and `repos` roles for baseline setup.

## ANTI-PATTERNS
- **Non-Standard Directories**: Templates should not be nested in `files/`. Move to `templates/`.

## UNIQUE STYLES
- **Component-Specific Task Files**: Tasks are organized by functionality (e.g., `packages.yml`, `config.yml`).
- **Mock Integration**: Configures Mock for clean RPM builds.
- **Non-Standard Directory**: Mock templates are stored in `files/etc/mock/templates/` (deviation from Ansible conventions).

## NOTES
- **Dependencies**: Requires `common` and `repos` roles for baseline system and repository setup.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/roles/rpm-dev/README.md`.