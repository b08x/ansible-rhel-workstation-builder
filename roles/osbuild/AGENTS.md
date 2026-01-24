# OSBUILD ROLE KNOWLEDGE BASE

Blueprint-based Fedora Workstation ISO generation using OSBuild Composer (TOML-driven).

## WHERE TO LOOK
| Task                      | File                                        | Notes                                            |
|---------------------------|---------------------------------------------|--------------------------------------------------|
| **Build Orchestration**   | `tasks/build.yml`                           | 253 lines, retry logic, async/poll, cleanup      |
| **Blueprint Management**  | `tasks/blueprint.yml`                       | 179 lines, TOML validation, push/depsolve        |
| **Blueprint Definitions** | `defaults/main.yml`                         | 260 lines, monolithic TOML blueprints + packages |
| **Source Config**         | `tasks/sources.yml`                         | 149 lines, repo source validation                |
| **Static Blueprints**     | `files/fedora/43/x86_64/workstation/*.toml` | Pre-defined workstation variants                 |

## CONVENTIONS
- **Blueprint System**: TOML files define packages/services/users/customizations
- **Composer CLI**: `composer-cli` for blueprint push, build start, status checks
- **Async Workflows**: `async: 10800`, `poll: 0` for large builds (60-120min)
- **TOML Validation**: Requires `tomli` Python library (skipped if unavailable - anti-pattern)
- **Build Artifacts**: `/var/tmp/osbuild-images/<blueprint-name>-*.iso`

## ANTI-PATTERNS (THIS ROLE)
- **Skipped TOML Validation**: No hard fail if `tomli` unavailable
- **Monolithic Defaults**: 260-line defaults needs split (blueprints/packages/sources)
- **Hardcoded Retry Logic**: 3 retries with 60s delay not variablized
- **Empty Password**: Blueprint defaults to no root password

## UNIQUE STYLES
- **Static vs Dynamic Blueprints**: Can use pre-defined TOML files or generate from variables
- **Depsolve Phase**: Blueprint dependency resolution before build (can fail early)
- **Blueprint Versioning**: `composer-cli` tracks blueprint versions, not this role
- **RHEL Ecosystem Only**: Unlike KIWI, OSBuild limited to Fedora/RHEL/CentOS

## CONSOLIDATION TARGETS
- Split `defaults/main.yml` into `blueprints.yml`, `packages.yml`, `sources.yml`
- Extract retry logic into `common/tasks/retry.yml`
- Variablize retry counts/delays (`osbuild_build_retries`, `osbuild_retry_delay`)
- Enforce TOML validation (fail if `tomli` unavailable)

## COMPARISON TO KIWI
| Feature           | KIWI NG                         | OSBuild Composer                  |
|-------------------|---------------------------------|-----------------------------------|
| **Live ISOs**     | ✅ Native                        | ⚠️ Limited                        |
| **NVIDIA Akmods** | ✅ Full support                  | ❌ Challenging                     |
| **Multi-distro**  | ✅ Yes                           | ❌ RHEL ecosystem only             |
| **Flexibility**   | ✅ High (XML/Jinja2)             | ⚠️ Blueprint constraints          |
| **Build Time**    | 45-90min                        | 60-120min                         |
| **Best For**      | Live ISOs, AI/HPC, multi-distro | Standard Fedora variants, servers |

## NOTES
- **Disk Space**: 50GB minimum (100GB+ with large package sets)
- **Blueprint Syntax**: TOML format, different from Kickstart
- **Testing**: `composer-cli compose status` monitors builds
- **When to Use**: Choose OSBuild for standard Fedora Workstation variants without NVIDIA
