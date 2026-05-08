# NAS Storage Configuration

> 5 nodes · cohesion 0.40

## Key Concepts

- **NAS Tasks Main** (3 connections) — `roles/nas/tasks/main.yml`
- **NAS NFS Tasks** (2 connections) — `roles/nas/tasks/nfs/main.yml`
- **NAS Rsync Tasks** (1 connections) — `roles/nas/tasks/rsync/main.yml`
- **NAS Samba Tasks** (1 connections) — `roles/nas/tasks/samba/main.yml`
- **Hybrid Firewall Approach** (1 connections) — `roles/nas/tasks/nfs/firewall.yml`

## Relationships

- No strong cross-community connections detected

## Source Files

- `roles/nas/tasks/main.yml`
- `roles/nas/tasks/nfs/firewall.yml`
- `roles/nas/tasks/nfs/main.yml`
- `roles/nas/tasks/rsync/main.yml`
- `roles/nas/tasks/samba/main.yml`

## Audit Trail

- EXTRACTED: 6 (75%)
- INFERRED: 2 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*