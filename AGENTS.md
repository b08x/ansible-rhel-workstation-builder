# ANSIBLE KNOWLEDGE BASE

**Generated:** May 8, 2026
**Commit:** ab94fcf (development branch)

---

## OVERVIEW
Ansible collection for RHEL-family workstation provisioning, NAS configuration, and custom ISO generation (OSBuild). Supports Fedora 43, Rocky Linux 9/10, RHEL 9+ with NVIDIA drivers, Intel oneAPI, and hybrid desktop environments.

## STRUCTURE
```
./playbooks/     # 12 playbooks (use-case-specific naming)
./roles/        # 21 modular roles
./vars/         # Global variables (unencrypted secrets)
./plugins/      # Custom Ansible plugins
./inventory/    # Inventory files
./docs/         # PLAYBOOKS.md, VARIABLES.md
./ansible.cfg   # Fact caching, SSH optimization
```

## ROLES (21 TOTAL)
| Role | Purpose |
|------|---------|
| `osbuild/` | **Primary:** ISO building (replaced KIWI) |
| `workstation/` | Desktop apps, GenAI tools (ollama, etc.) |
| `audio/` | PipeWire/JACK, realtime tuning |
| `sway/` | Wayland compositor |
| `video/` | Intel/NVIDIA GPU setup |
| `nas/` | NFS/Samba/Rsync |
| `podman/` | Container runtime |
| `docker/` | Docker daemon |
| `libvirt/` | VM management |
| `rpm-dev/` | Mock templates |
| `zsh/` | Oh-My-Zsh |
| `asdf/` | Version manager |
| `base/` | Repository + common setup |
| `repos/` | DNF/YUM management |
| `common/` | GRUB, timezone, locale |
| `systemd-networkd/` | Network config |
| `display-manager/` | Login managers |
| `networking/` | Network setup |
| `ramalama/` | RAG tooling |
| `ruby/` | Ruby environment |
| `tools/` | Development tools |
| `user/` | User configuration |
| `xdg/` | XDG base dirs |

## COMMANDS
```bash
# ISO builds (primary use case)
ansible-playbook playbooks/build-workstation-image.yml  # OSBuild

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
```

## SECURITY ANTI-PATTERNS
- **`vars/secrets.yml`:** Unencrypted secrets (Gmail passwords, credentials)
- **`roles/nas/`:** SMB1/NTLMv1 enabled (deprecated protocols)
- **Empty passwords:** `roles/osbuild/` live ISO defaults

## CONVENTIONS
- **YAML:** 2-space indent, no line limits, `document-start: error`
- **Task naming:** Non-standard, tool-specific (e.g., `jacktrip-pi.yml`)
- **Variable files:** `roles/*/vars/{{ ansible_distribution }}.yml`
- **Build patterns:** `async`/`poll: 0` for long operations (OSBuild)

## CRITICAL NOTES
- **NVIDIA First Boot:** Black screen 2-5min normal (akmods compiling)
- **Secure Boot:** Disable or enroll MOK for NVIDIA akmods
- **DNF5 Instability:** Fedora 43+ retry logic (3 attempts)
- **Disk Space:** OSBuild requires 50GB minimum
- **No Molecule:** Custom test playbooks in `roles/*/tests/`

## WHAT TO AVOID
- Don't expect KIWI role (removed in commit bd14050)
- Don't use `site.yml` - know exact playbook names
- Don't assume standard role structure - many have non-standard layouts