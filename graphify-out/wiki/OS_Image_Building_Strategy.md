# OS Image Building Strategy

> 6 nodes · cohesion 0.33

## Key Concepts

- **OSBuild Tasks Main** (3 connections) — `roles/osbuild/tasks/main.yml`
- **Build Workstation Image Playbook** (2 connections) — `playbooks/build-workstation-image.yml`
- **KIWI Tasks Main** (2 connections) — `roles/kiwi/tasks/main.yml`
- **Image Building** (1 connections) — `roles/osbuild/tasks/main.yml`
- **KIWI Deprecation Rationale** (1 connections) — `roles/kiwi/tasks/main.yml`
- **OSBuild Migration Rationale** (1 connections) — `playbooks/build-workstation-image.yml`

## Relationships

- No strong cross-community connections detected

## Source Files

- `playbooks/build-workstation-image.yml`
- `roles/kiwi/tasks/main.yml`
- `roles/osbuild/tasks/main.yml`

## Audit Trail

- EXTRACTED: 8 (80%)
- INFERRED: 2 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*