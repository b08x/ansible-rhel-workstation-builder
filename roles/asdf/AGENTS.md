# ASDF ROLE

**Purpose:** Version manager for Ruby, Python, Node.js, and other development tools.

**Recent Changes (53c1198):** New role for managing multiple runtime versions.

## OVERVIEW
Installs asdf version manager enabling side-by-side installation of multiple versions of programming languages and tools. Replaces rbenv, pyenv, nvm with unified interface.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **ASDF Install** | `tasks/main.yml` | Version manager setup |
| **Plugin Setup** | `tasks/plugins.yml` | Language plugin installation |
| **Shell Integration** | `tasks/shell.yml` | Bash/Zsh configuration |
| **Variables** | `vars/main.yml` | Default versions, plugin list |

## CONVENTIONS
- **Global Versions**: Set system-wide defaults in `.tool-versions`
- **Plugin Management**: Automatic plugin installation for common languages
- **Shell Integration**: Works with both Bash and Zsh

## ANTI-PATTERNS
- **Never** mix with other version managers (rbenv, pyenv, nvm)
- **Never** install language packages via system package manager when using asdf

## UNIQUE STYLES
- **Unified Interface**: Single tool for all language versions
- **Shell Shims**: Transparent version switching via PATH manipulation
- **Project-Local**: `.tool-versions` files override global settings

## NOTES
- **Conflicts**: Remove rbenv/pyenv/nvm before installing asdf
- **Performance**: Slight shell startup delay due to shim lookup
- **Compatibility**: Works with existing projects via `.tool-versions`