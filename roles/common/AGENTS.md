# COMMON ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `common` role provides system baseline configuration, including GRUB, timezone, locale, rc.local, and YADM integration.

## STRUCTURE
```
roles/common/
├── tasks/          # System baseline tasks
│   ├── main.yml    # Orchestrates task includes
│   ├── rclocal.yml # rc.local configuration
│   ├── grub.yml    # GRUB bootloader configuration
│   └── yadm.yml    # YADM dotfile management
├── handlers/       # Service handlers
├── templates/      # Jinja2 templates for system files
├── vars/           # Role-specific variables
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static files
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **GRUB Configuration** | `tasks/grub.yml` | Configures GRUB bootloader settings |
| **Timezone/Locale** | `tasks/main.yml` | Sets system timezone and locale |
| **rc.local** | `tasks/rclocal.yml` | Configures system rc.local script |
| **YADM** | `tasks/yadm.yml` | Manages dotfiles with YADM |
| **Templates** | `templates/` | Jinja2 templates for system files (e.g., `rc.local.j2`) |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `rclocal.yml`, `grub.yml`).
- **Jinja2 Templates**: Dynamic configurations (e.g., `templates/rc.local.j2`).
- **Non-Standard Task Names**: Task files named after system components (e.g., `rclocal.yml` instead of `boot_scripts.yml`).
- **Role Dependencies**: Required by `workstation`, `rpm-dev`, and other roles for baseline setup.

## ANTI-PATTERNS
- **Non-Standard Task Names**: Avoid naming task files after system components (e.g., `rclocal.yml`). Use functional names (e.g., `boot_scripts.yml`).

## UNIQUE STYLES
- **Component-Specific Task Files**: Tasks are organized by system component (e.g., `grub.yml`, `rclocal.yml`).
- **Jinja2 Templates**: Dynamic configurations for system files (e.g., `rc.local.j2`).
- **YADM Integration**: Manages dotfiles using YADM (Yet Another Dotfiles Manager).

## NOTES
- **Dependencies**: This role is a prerequisite for `workstation`, `rpm-dev`, and other roles.
- **Security**: rc.local and GRUB configurations may have security implications. Review carefully.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.