# PLUGINS KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `plugins/` directory contains custom Ansible plugins, including modules, filters, and callbacks, to extend Ansible functionality.

## STRUCTURE
```
plugins/
├── modules/    # Custom Ansible modules
├── filter/     # Custom Jinja2 filters
└── callback/   # Custom callback plugins
```

## WHERE TO LOOK
| Plugin Type | Location | Notes |
|-------------|----------|-------|
| **Custom Modules** | `plugins/modules/` | Extend Ansible with custom module logic |
| **Custom Filters** | `plugins/filter/` | Custom Jinja2 filters for variable manipulation |
| **Custom Callbacks** | `plugins/callback/` | Custom callback plugins for logging, notifications, etc. |

## CONVENTIONS
- **Custom Plugin Paths**: Defined in `ansible.cfg` (e.g., `./plugins/filter:/usr/share/ansible/plugins/filter`).
- **Modular Plugins**: Plugins are organized by type (modules, filters, callbacks).
- **Python-Based**: Custom plugins are written in Python and follow Ansible plugin conventions.

## ANTI-PATTERNS
- **None specific to this directory.**

## UNIQUE STYLES
- **Custom Modules**: Extend Ansible with project-specific module logic.
- **Custom Filters**: Provide Jinja2 filters for variable manipulation (e.g., `to_yaml`, `from_json`).
- **Custom Callbacks**: Enable custom logging, notifications, or integrations (e.g., Slack, email).

## NOTES
- **Dependencies**: Plugins are referenced in `ansible.cfg` for path configuration.
- **Compatibility**: Ensure plugins are compatible with Ansible 2.9+.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Test plugins manually.
- **Documentation**: Document plugin usage in `docs/PLUGINS.md`.