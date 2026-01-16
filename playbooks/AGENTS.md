# PLAYBOOKS KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `playbooks/` directory contains top-level automation scripts for Ansible, targeting specific use cases or system configurations.

## STRUCTURE
```
playbooks/
├── facts.yml            # System facts gathering
├── rpm-dev.yml          # RPM development environment setup
├── nas.yml              # Network-attached storage configuration
├── oneAPI.yml           # Intel oneAPI MKL installation
├── postfix_gmail.yml    # Postfix Gmail relay configuration
└── jacktrip-pi.yml      # JackTrip on Raspberry Pi (non-standard)
```

## WHERE TO LOOK
| Playbook | Purpose | Roles Used | Notes |
|----------|---------|------------|-------|
| **facts.yml** | Gather system facts and baseline configuration | - | Debug playbook for system introspection |
| **rpm-dev.yml** | Configure RPM development environment | `common`, `repos`, `rpm-dev` | Fedora 42 focus with Mock support |
| **nas.yml** | Configure network-attached storage services | `nas` | Manually configurable for NFS/Samba/Rsync |
| **oneAPI.yml** | Install Intel oneAPI MKL toolkit | - | Adds Intel repository and scientific computing libraries |
| **postfix_gmail.yml** | Configure Postfix to relay via Gmail SMTP | - | Requires encrypted `secrets.yml` with Gmail credentials |
| **jacktrip-pi.yml** | Configure JackTrip on Raspberry Pi | - | Non-standard playbook for specific use case |

## CONVENTIONS
- **Non-Standard Playbook Names**: Playbooks target specific use cases (e.g., `jacktrip-pi.yml`, `postfix_gmail.yml`) rather than roles or system types.
- **Modular Composition**: Playbooks compose roles and tasks for specific workflows (e.g., `rpm-dev.yml` uses `common`, `repos`, and `rpm-dev` roles).
- **Security-First**: Playbooks like `postfix_gmail.yml` require encrypted secrets (Ansible Vault).

## ANTI-PATTERNS
- **Non-Standard Names**: Avoid playbook names that target specific tools/use cases (e.g., `jacktrip-pi.yml`). Prefer role-based names (e.g., `workstation.yml`).

## UNIQUE STYLES
- **Use-Case-Specific Playbooks**: Playbooks like `jacktrip-pi.yml` and `postfix_gmail.yml` target niche use cases.
- **Role Composition**: Playbooks compose roles for specific workflows (e.g., `rpm-dev.yml` uses `common`, `repos`, and `rpm-dev`).
- **Security Integration**: Playbooks like `postfix_gmail.yml` require Ansible Vault for secrets.

## NOTES
- **Dependencies**: Some playbooks depend on roles (e.g., `rpm-dev.yml` requires `common`, `repos`, and `rpm-dev`).
- **Security**: Playbooks like `postfix_gmail.yml` require Gmail App Passwords (enable 2FA).
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand playbook-specific docs in `docs/PLAYBOOKS.md`.