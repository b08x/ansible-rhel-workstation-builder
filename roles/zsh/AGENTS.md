# ZSH ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `zsh` role customizes the ZSH shell environment, including Oh My Zsh, plugins, themes, and utilities like Zoxide.

## STRUCTURE
```
roles/zsh/
├── tasks/          # ZSH customization tasks
│   ├── main.yml    # Orchestrates task includes
│   ├── zsh.yml     # Installs ZSH and Oh My Zsh
│   └── plugins.yml # Configures plugins and themes
├── handlers/       # Service handlers
├── templates/      # Jinja2 templates for shell configs
├── vars/           # Role-specific variables
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static files
    └── usr/share/oh-my-zsh/plugins/  # Custom plugins
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **ZSH Installation** | `tasks/zsh.yml` | Installs ZSH, Oh My Zsh, and Zoxide |
| **Plugin Configuration** | `tasks/plugins.yml` | Configures Oh My Zsh plugins and themes |
| **Custom Plugins** | `files/usr/share/oh-my-zsh/plugins/` | Custom plugins (e.g., `ripgrep`, `fd`) |
| **Templates** | `templates/` | Jinja2 templates for shell configurations (e.g., `.zshrc.j2`) |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `zsh.yml`, `plugins.yml`).
- **Jinja2 Templates**: Dynamic configurations for shell files (e.g., `.zshrc.j2`).
- **Custom Plugins**: Custom plugins are stored in `files/usr/share/oh-my-zsh/plugins/`.
- **Role Dependencies**: Requires `common` role for baseline setup.

## ANTI-PATTERNS
- **None specific to this role.**

## UNIQUE STYLES
- **Custom Plugins**: Custom Oh My Zsh plugins (e.g., `ripgrep`, `fd`) are stored in `files/usr/share/oh-my-zsh/plugins/`.
- **Zoxide Integration**: Installs and configures Zoxide for smart directory navigation.
- **Jinja2 Templates**: Dynamic configurations for `.zshrc` and other shell files.

## NOTES
- **Dependencies**: Requires `common` role for baseline system setup.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/roles/zsh/README.md`.