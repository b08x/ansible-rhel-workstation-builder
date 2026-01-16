# PLAYBOOKS KNOWLEDGE BASE

**Generated:** 07:26:41 AM (America/New_York)
**Commit:** 8940810
**Branch:** development

---

## OVERVIEW
Top-level automation scripts with non-standard, use-case-specific naming that directly reflects their purpose rather than generic conventions.

## STRUCTURE
```
playbooks/
├── build-kiwi-iso.yml   # KIWI NG image building (107 lines)
├── nas.yml              # NFS/Samba/Rsync setup
├── jacktrip-pi.yml      # JackTrip audio streaming (Raspberry Pi)
├── workstation.yml      # Full workstation provisioning
├── facts.yml            # System facts gathering/debugging
├── rpm-dev.yml          # RPM development environment
├── docker.yml           # Docker + container tools
├── postfix_gmail.yml    # Gmail SMTP relay configuration
└── oneAPI.yml           # Intel oneAPI tools
```

## WHERE TO LOOK
| Playbook | Purpose | Key Roles | Target Hosts |
|----------|---------|-----------|--------------|
| **workstation.yml** | Full workstation setup | workstation, repos, common | localhost |
| **nas.yml** | Network storage services | nas | nas_server |
| **build-kiwi-iso.yml** | Custom ISO generation | kiwi | localhost |
| **rpm-dev.yml** | RPM packaging environment | rpm-dev, repos | dev |
| **jacktrip-pi.yml** | Network audio streaming | audio (partial) | pi |
| **postfix_gmail.yml** | Email relay via Gmail | N/A (standalone tasks) | all |
| **docker.yml** | Container platform | docker, libvirt | localhost |
| **oneAPI.yml** | Intel development tools | N/A (standalone tasks) | localhost |
| **facts.yml** | System information | N/A (debug only) | all |

## CONVENTIONS
- **Use-Case Names**: Playbooks named after specific functions (not generic like `site.yml`)
- **Target-Specific**: Each playbook targets specific host groups or use cases
- **Modular Structure**: Uses `pre_tasks`, `roles`, `post_tasks` for organized execution
- **Variable Validation**: Complex playbooks include variable validation in `pre_tasks`
- **Build Summaries**: Image building playbooks generate build reports

## ANTI-PATTERNS (THIS PROJECT)
- **Unencrypted credentials**: `postfix_gmail.yml` references plaintext Gmail passwords
- **Non-idempotent tasks**: `postmap` command not fully idempotent when credentials change
- **Hardcoded paths**: Some playbooks use hardcoded paths instead of variables

## UNIQUE STYLES
- **Non-Standard Entry Points**: No `site.yml` - must know specific playbook names
- **Build Orchestration**: `build-kiwi-iso.yml` has complex validation and summary logic
- **Cross-Platform**: `jacktrip-pi.yml` optimized for Raspberry Pi hardware
- **Standalone Tasks**: Some playbooks bypass roles for simple configurations
- **Dynamic Inclusion**: Role inclusion with complex conditionals based on build status

## NOTES
- **Dependencies**: Some playbooks depend on roles (e.g., `rpm-dev.yml` requires `common`, `repos`, and `rpm-dev`).
- **Security**: Playbooks like `postfix_gmail.yml` require Gmail App Passwords (enable 2FA).
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand playbook-specific docs in `docs/PLAYBOOKS.md`.