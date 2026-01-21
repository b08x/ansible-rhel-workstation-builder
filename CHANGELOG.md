## [unreleased]

### 🚀 Features

- *(rpm-dev)* Add RPM development environment role with complete setup for Fedora 42
- *(common)* Added common system configuration and GRUB setup with new defaults and handlers
- *(repos)* Add initial repository role with configuration, handlers, and tasks for Fedora and RHEL repo setup
- *(playbooks)* Add rpm-dev playbook for RPM development environment setup
- *(rpm-dev)* Update mock configuration and add custom template for Fedora 43
- Add Ansible roles for Docker, Libvirt, Workstation, and RPM development, new playbooks, and relocate inventory.
- *(audio)* Add comprehensive audio production role
- *(sway)* Add initial sway window manager role
- *(kiwi)* Add new role and playbook for Fedora ISO generation with KIWI NG
- *(osbuild)* Overhaul role with modular tasks and Fedora 43 support
- *(sway)* Enhance distribution support and refine configuration
- Document the new audio role and enhance the project knowledge base with updated playbooks, anti-patterns, and unique style descriptions.

### 🐛 Bug Fixes

- *(nas)* Add missing firewall.nfs.ports variable structure

### 🚜 Refactor

- *(repos)* Consolidate repository priority configuration

### 📚 Documentation

- *(knowledge-base)* Init hierarchical AGENTS.md files
- Rewrite README + add Claude agents for RHEL workflows
- Add workstation collection architect agent definition
- Enhance README readability by adjusting table formatting, adding a KIWI documentation link, and specifying shell for a code block.

### ⚙️ Miscellaneous Tasks

- *(agents)* Consolidate architect agents and workflows
