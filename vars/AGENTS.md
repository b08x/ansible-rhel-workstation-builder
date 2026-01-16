# VARIABLES KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `vars/` directory contains global and distribution-specific variables for Ansible automation, including unencrypted secrets (security anti-pattern).

## STRUCTURE
```
vars/
├── secrets.yml    # Unencrypted secrets (security anti-pattern)
├── Fedora.yml     # Fedora-specific variables
└── RedHat.yml     # RHEL/Rocky Linux-specific variables
```

## WHERE TO LOOK
| Variable File | Purpose | Notes |
|---------------|---------|-------|
| **secrets.yml** | Sensitive credentials (e.g., Gmail passwords) | **Unencrypted (security risk)**. Use Ansible Vault. |
| **Fedora.yml** | Fedora-specific package lists and configurations | Overrides for Fedora systems |
| **RedHat.yml** | RHEL/Rocky Linux-specific package lists and configurations | Overrides for RHEL/Rocky Linux systems |

## CONVENTIONS
- **Distribution-Specific Variables**: Fedora and RHEL configurations are separated (e.g., `Fedora.yml`, `RedHat.yml`).
- **Role-Prefixed Variables**: Variables are prefixed with role names (e.g., `nas_nfs_exports`, `rpm_dev_user`).
- **Variable Precedence**: `vars/` > `group_vars/` > `host_vars/` (if added later).

## ANTI-PATTERNS
- **Unencrypted Secrets**: `secrets.yml` contains plaintext credentials (security risk). Use Ansible Vault.
- **Generic Variable Names**: Avoid generic names (e.g., `user`, `path`). Use role-prefixed variables (e.g., `nas_user`, `rpm_dev_path`).

## UNIQUE STYLES
- **Distribution-Specific Variables**: Fedora and RHEL configurations are separated for clarity.
- **Role-Prefixed Variables**: Variables are prefixed with role names to avoid conflicts.
- **Security Anti-Pattern**: `secrets.yml` is unencrypted (security risk).

## SECURITY NOTES
- **Ansible Vault**: Use Ansible Vault to encrypt `secrets.yml`.
  ```bash
  ansible-vault encrypt vars/secrets.yml
  ```
- **Vault Password**: Store vault passwords securely (e.g., `~/.vault_pass`).
- **Secrets Rotation**: Rotate secrets regularly (e.g., Gmail App Passwords).
- **File Permissions**: Restrict permissions on `secrets.yml` (`chmod 600`).

## NOTES
- **Dependencies**: Variables in `vars/` are referenced by playbooks and roles.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand variable-specific docs in `docs/VARIABLES.md`.