# ANSIBLE KNOWLEDGE BASE

**Generated:** 08:50:55 PM (America/New_York)
**Commit:** 2030f3f
**Branch:** development

---

## OVERVIEW
Ansible collection automating RHEL-family workstation provisioning, NAS configuration, and custom ISO generation (KIWI NG/OSBuild). Modular roles support Fedora 43, Rocky Linux 9/10, RHEL 9+ with specialized AI/HPC workstation images featuring NVIDIA drivers, Intel oneAPI, and hybrid desktop environments.

**Current State:** Production collection capturing existing architecture with planned consolidation of package/var declarations, code normalization, style guide adoption, and GenAI tool integration.

## STRUCTURE
```
./
├── playbooks/          # Use-case-specific automation (non-standard naming)
├── roles/              # Modular roles (12 total: audio, common, docker, kiwi, libvirt, nas, osbuild, repos, rpm-dev, sway, workstation, zsh)
├── vars/               # Global variables (CRITICAL: unencrypted secrets)
├── plugins/            # Custom Ansible plugins (callbacks, filters)
├── inventory/          # Inventory files
├── docs/               # Documentation (PLAYBOOKS.md, VARIABLES.md)
├── ansible.cfg         # Custom plugins, fact caching, SSH optimization
├── .ansible-lint       # Custom linting rules
└── .yamllint.yaml      # YAML formatting (2-space indent, no line limits)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Custom ISO Building** | `roles/kiwi/`, `playbooks/build-kiwi-iso.yml` | KIWI NG live ISOs with NVIDIA/oneAPI (async build, 281 lines) |
| **Blueprint ISOs** | `roles/osbuild/` | OSBuild Composer TOML-based images (253-line build task) |
| **Audio Workstation** | `roles/audio/` | PipeWire/JACK, realtime tuning (97 desktop files, 149 total files) |
| **Sway WM** | `roles/sway/` | Wayland compositor configs (130 files, 29 scripts) |
| **NAS Services** | `roles/nas/` | NFS/Samba/Rsync (CRITICAL: SMB1/NTLMv1 enabled, 239-line defaults) |
| **RPM Development** | `roles/rpm-dev/` | Mock templates (anti-pattern: templates in `files/`) |
| **Workstation Apps** | `roles/workstation/` | **Target for GenAI tools** (ollama, whisper.cpp, gemini-cli, claude-code, opencode) |
| **Shell Customization** | `roles/zsh/` | Oh-My-Zsh, plugins, themes (38 files) |
| **Repositories** | `roles/repos/` | DNF/YUM management (Fedora/RHEL-specific) |
| **Baseline Config** | `roles/common/` | GRUB, timezone, locale, rc.local, YADM |
| **Variables** | `vars/` | **CRITICAL**: Unencrypted secrets, distro-specific vars (140 lines Fedora.yml) |
| **Custom Plugins** | `plugins/callback/llm_analyzer.py` | LLM-based playbook analysis callback |

## PROJECT SCALE
- **Files:** 474 total (149 in `audio`, 130 in `sway`, 51 in `osbuild`)
- **YAML Lines:** 6,633 total (281 in `kiwi/tasks/build.yml`, 273 in `kiwi/defaults/main.yml`)
- **Directory Depth:** 9 levels (complexity hotspots at depth 4+)
- **Large Files (>100 lines):** 19 files (complexity indicators)
- **Roles:** 12 distinct domains

## CONVENTIONS
- **YAML Style**: 2-space indentation, no line limits, `document-start: error`
- **Non-Standard Naming**: Playbooks/tasks named after tools (e.g., `google-chrome.yml`, `jacktrip-pi.yml`)
- **Modular Task Includes**: `include_tasks` for dynamic loading (e.g., `{{ ansible_distribution }}.yml`)
- **Distribution Variables**: `Fedora.yml` vs `Rocky.yml`/`RedHat.yml` in `roles/*/vars/`
- **Async Build Patterns**: KIWI/OSBuild use `async`/`poll: 0` (avoid timeouts on 45-90min builds)
- **Component-Specific Tasks**: Tool-named files (not `install.yml`/`configure.yml`)

## ANTI-PATTERNS (THIS PROJECT)
**SECURITY CRITICAL:**
- **Unencrypted secrets**: `vars/secrets.yml` (Gmail passwords, credentials)
- **SMB1/NTLMv1**: `roles/nas/defaults/main.yml` enables deprecated protocols
- **Empty passwords**: `roles/kiwi/defaults/main.yml`, `roles/osbuild/` (live ISO defaults)
- **Root-equivalent privileges**: Docker/libvirt group membership

**STRUCTURAL:**
- **Templates in files/**: `roles/rpm-dev/files/etc/mock/templates/` violates conventions
- **Monolithic defaults**: 273-line `kiwi/defaults/main.yml`, 260-line `osbuild/defaults/main.yml`
- **Package duplication**: Common packages (firewalld, policycoreutils) repeated across roles
- **97 desktop files**: `roles/audio/files/home/local/share/applications/` (no organization)
- **Stdout parsing**: Unreliable error detection

## UNIQUE STYLES
- **Split-Brain Design**: Fedora 43 (bleeding-edge ISO builds) vs Rocky 9/10 (stable configs)
- **Deep Nesting**: NAS role modularizes services into subdirs (`nfs/`, `samba/`, `rsync/`)
- **User-Specific Deploys**: Audio/ZSH deploy to user directories (`home/local/share/`)
- **Async Workflows**: KIWI/OSBuild complex polling for ISO generation (7200s timeout)
- **No `site.yml`**: Use-case-specific playbooks (must know exact names)
- **Dynamic Inclusion**: Role inclusion with complex conditionals based on build status

## CONSOLIDATION ROADMAP
**Package/Var Normalization:**
- Consolidate package lists from 12 role defaults into `common/vars/packages.yml`
- Merge distribution-specific variables using `ansible_distribution` conditionals
- Deduplicate common packages (firewalld, policycoreutils appear 8+ times)

**GenAI Tools Integration (roles/workstation/):**
- Add ollama (LLM runtime)
- Add whisper.cpp (speech-to-text)
- Add gemini-cli (Google Gemini CLI)
- Add claude-code (Anthropic Claude Code)
- Add opencode (Oh My OpenCode)

**Ruby/Python Environments:**
- Investigate rbenv/pyenv/asdf integration patterns
- Define systemwide vs user-local installation strategy
- Add virtual environment management

**Style Guide Adoption:**
- Flatten monolithic defaults (split into `packages.yml`, `build_configs.yml`)
- Move templates from `files/` to `templates/`
- Consolidate handlers into `common/handlers/`
- Extract reusable tasks to `common/tasks/` (packages, services, firewall)

## CODE MAP (COMPLEXITY HOTSPOTS)
| File | Lines | Complexity | Priority |
|------|-------|------------|----------|
| `roles/kiwi/tasks/build.yml` | 281 | Async polling, nested conditionals, hardcoded timeouts | **HIGH** |
| `roles/kiwi/defaults/main.yml` | 273 | Monolithic package lists, no separation of concerns | **HIGH** |
| `roles/osbuild/tasks/build.yml` | 253 | Retry logic, nested block/rescue, cleanup tasks | **HIGH** |
| `roles/osbuild/defaults/main.yml` | 260 | Monolithic blueprints, package lists | **HIGH** |
| `roles/nas/defaults/main.yml` | 239 | NFS/Samba/Rsync configs, SMB1 anti-pattern | **MEDIUM** |
| `roles/osbuild/tasks/blueprint.yml` | 179 | Validation logic, error handling | **MEDIUM** |
| `roles/kiwi/tasks/structure.yml` | 168 | Directory validation, hardcoded paths | **MEDIUM** |
| `roles/nas/tasks/nfs/firewall.yml` | 155 | Large loops, hardcoded port lists | **LOW** |
| `roles/osbuild/tasks/main.yml` | 153 | Build orchestration, nested blocks | **LOW** |
| `roles/audio/tasks/tuning.yml` | 150 | Realtime kernel tuning, IRQ balance | **LOW** |

## COMMANDS
```bash
# Custom ISO builds (primary use case)
ansible-playbook playbooks/build-kiwi-iso.yml  # KIWI NG (45-90min)
ansible-playbook -i inventory playbooks/osbuild-example.yml  # OSBuild Composer

# System configuration
ansible-playbook playbooks/workstation.yml -i inventory/inventory.ini
ansible-playbook playbooks/nas.yml -i inventory/inventory.ini
ansible-playbook playbooks/rpm-dev.yml -i inventory/inventory.ini

# Dry run
ansible-playbook -C playbooks/<playbook>.yml -i inventory/inventory.ini --diff

# Security
ansible-vault encrypt vars/secrets.yml
ansible-playbook playbooks/postfix_gmail.yml --ask-vault-pass

# Linting
ansible-lint
yamllint -c .yamllint.yaml .

# Testing (role-specific)
ansible-playbook roles/<role>/tests/test.yml -i roles/<role>/tests/inventory
```

## NOTES
- **Project Scale:** 474 files, 6633 YAML lines, depth 9 - significant complexity
- **No Molecule:** Custom test playbooks in `roles/*/tests/` (non-standard)
- **NVIDIA First Boot:** Black screen 2-5min normal (akmods compiling drivers)
- **Secure Boot:** NVIDIA akmods unsigned - disable or enroll MOK
- **DNF5 Instability:** Fedora 43+ retry logic (3 attempts) for download failures
- **Disk Space:** KIWI 50-80GB, OSBuild 50GB, both active 100GB+
- **Security:** Restrict NAS to trusted networks, use firewalld
- **Gmail App Passwords:** Required for `postfix_gmail.yml` (enable 2FA)
- **Large Files:** 19 files >100 lines indicate refactoring opportunities
- **AI-Generated:** Much of codebase generated with Claude Code, Antigravity, OpenCode
