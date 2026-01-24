# BASE ROLE

**Purpose:** Consolidated system foundation combining repositories and common functionality.

**Recent Changes (52d5ab9):** Major refactoring to consolidate `repos` and `common` roles.

## OVERVIEW
Foundation role that consolidates repository management and baseline system configuration. Replaces separate `repos` and `common` roles with unified approach to system base setup.

## STRUCTURE
```
base/
├── tasks/          # Consolidated base system tasks
├── defaults/       # Unified default variables
├── handlers/       # System service handlers
└── templates/      # Base configuration templates
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Repository Setup** | `tasks/repos.yml` | DNF/YUM repository configuration |
| **Base Config** | `tasks/system.yml` | GRUB, timezone, locale, rc.local |
| **Package Management** | `tasks/packages.yml` | Core system packages |
| **Variables** | `defaults/main.yml` | Consolidated base system variables |

## CONVENTIONS
- **Consolidation**: Single role replaces `repos` + `common` functionality  
- **Distribution Aware**: Supports Fedora/RHEL/Rocky with conditional logic
- **Minimal Dependencies**: No external role dependencies

## ANTI-PATTERNS
- **Never** use alongside deprecated `repos` or `common` roles
- **Never** duplicate repository configuration in other roles

## UNIQUE STYLES
- **Unified Approach**: Single role handles all base system concerns
- **Conditional Logic**: Distribution-specific tasks based on `ansible_distribution`
- **Handler Consolidation**: Shared handlers for system services

## NOTES
- **Migration**: Replaces separate `repos` and `common` roles
- **Dependencies**: Other roles should depend on `base` instead of `repos`/`common`
- **Backwards Compatibility**: May need playbook updates for role name changes