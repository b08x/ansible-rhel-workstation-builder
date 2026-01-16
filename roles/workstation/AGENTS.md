# WORKSTATION ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `workstation` role automates the setup of a Linux workstation, including application installations, development tools, and repository configurations.

## STRUCTURE
```
roles/workstation/
├── tasks/          # Workstation setup tasks
│   ├── main.yml    # Orchestrates task includes
│   ├── google-chrome.yml  # Google Chrome installation
│   ├── rust_utils.yml     # Rust toolchain setup
│   ├── rpmfusion.yml      # RPM Fusion repository setup
│   └── yadm.yml          # YADM dotfile management
├── handlers/       # Service handlers
├── templates/      # Jinja2 templates for application configs
├── vars/           # Role-specific variables
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static files
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Google Chrome** | `tasks/google-chrome.yml` | Installs Google Chrome browser |
| **Rust Toolchain** | `tasks/rust_utils.yml` | Installs Rust and utilities (e.g., `cargo`) |
| **RPM Fusion** | `tasks/rpmfusion.yml` | Configures RPM Fusion repositories |
| **YADM** | `tasks/yadm.yml` | Manages dotfiles with YADM |
| **Templates** | `templates/` | Jinja2 templates for application configurations |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `google-chrome.yml`, `rust_utils.yml`).
- **Non-Standard Task Names**: Task files named after applications/tools (e.g., `google-chrome.yml` instead of `browsers.yml`).
- **Role Dependencies**: Requires `common` and `repos` roles for baseline setup.

## ANTI-PATTERNS
- **Non-Standard Task Names**: Avoid naming task files after applications/tools (e.g., `google-chrome.yml`). Use functional names (e.g., `browsers.yml`).

## UNIQUE STYLES
- **Application-Specific Task Files**: Tasks are organized by application/tool (e.g., `google-chrome.yml`, `rust_utils.yml`).
- **Jinja2 Templates**: Dynamic configurations for application setups.
- **YADM Integration**: Manages dotfiles using YADM (Yet Another Dotfiles Manager).

## NOTES
- **Dependencies**: Requires `common` and `repos` roles for baseline system and repository setup.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/roles/workstation/README.md`.