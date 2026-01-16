# NAS ROLE KNOWLEDGE BASE

**Generated:** 03:12:45 AM (America/New_York)

---

## OVERVIEW
The `nas` role configures network-attached storage services, including NFS, Samba, and Rsync, with support for firewalld and access control.

## STRUCTURE
```
roles/nas/
├── tasks/          # NAS service tasks
│   ├── main.yml    # Orchestrates task includes
│   ├── nfs/        # NFS configuration
│   │   └── config.yml
│   ├── samba/      # Samba configuration
│   │   └── config.yml
│   └── rsync/      # Rsync configuration
│       └── config.yml
├── handlers/       # Service handlers
├── templates/      # Jinja2 templates for service configs
├── vars/           # Role-specific variables
├── defaults/       # Default variables (lowest precedence)
└── files/          # Static files
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **NFS Configuration** | `tasks/nfs/config.yml` | Configures NFS exports and firewalld rules |
| **Samba Configuration** | `tasks/samba/config.yml` | Configures Samba shares and authentication |
| **Rsync Configuration** | `tasks/rsync/config.yml` | Configures Rsync modules and access control |
| **Templates** | `templates/` | Jinja2 templates for service configs (e.g., `nfs.exports.j2`) |
| **Firewalld** | `tasks/main.yml` | Configures firewalld for NAS services |

## CONVENTIONS
- **Modular Task Files**: Tasks are split into reusable files (e.g., `nfs/config.yml`, `samba/config.yml`).
- **Jinja2 Templates**: Dynamic configurations for service files (e.g., `templates/nfs.exports.j2`).
- **Non-Standard Task Organization**: Tasks are organized by service (e.g., `nfs/`, `samba/`, `rsync/`).
- **Security-First**: Firewalld rules and access control are enforced by default.

## ANTI-PATTERNS
- **SMB1 Protocol**: Defaults to `NT1` (deprecated). Override with `nas_samba_server_min_protocol: "SMB2"`.

## UNIQUE STYLES
- **Service-Specific Task Files**: Tasks are organized by service (e.g., `nfs/config.yml`, `samba/config.yml`).
- **Jinja2 Templates**: Dynamic configurations for NFS exports, Samba shares, and Rsync modules.
- **Firewalld Integration**: Firewalld rules are configured for all NAS services.
- **Access Control**: NFS exports, Samba shares, and Rsync modules support client restrictions.

## SECURITY NOTES
- **NFS**: Restrict exports to trusted networks. Use `firewalld` to limit access.
- **Samba**: Use strong authentication (e.g., user passwords). Avoid SMB1 (deprecated).
- **Rsync**: Configure read-only or read-write access based on requirements.
- **Firewalld**: Enable firewalld rules to restrict access to NAS services.
- **Secrets**: Use Ansible Vault for credentials (e.g., Samba passwords).

## NOTES
- **Dependencies**: This role is standalone but may require `common` for baseline system configuration.
- **Testing**: No formal testing framework (e.g., Molecule) detected. Use `--check --diff` for dry runs.
- **Documentation**: Expand role-specific docs in `docs/roles/nas/README.md`.