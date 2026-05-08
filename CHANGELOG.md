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
- *(osbuild)* Update Fedora 43 package sources and manifest
- *(kiwi)* Update image build configuration and package lists
- *(kiwi)* Update build configuration and dependencies
- *(workstation)* Expand functionality with IDE and browser improvements
- *(roles)* Add asdf version manager role
- *(video)* Add new role for Intel and NVIDIA GPU configuration
- *(podman)* Add podman role and update nvidia gpu configuration
- Add Claude AI settings, update ASDF installation and ownership, adjust package defaults, and refine Fedora-specific configurations.
- Enhance workstation roles with flatpaks, asdf updates, and AI tools
- Add ramalama role and selinux playbook
- *(osbuild)* Update Fedora 43 sources and workstation blueprint
- *(base)* Add git-cliff to cargo packages
- *(osbuild)* Update fedora 43 nvidia blueprint packages and repo config
- *(osbuild)* Update Fedora 43 workstation NVIDIA blueprint
- *(base)* Enhance system configuration with dnf and cpupower settings
- *(workstation)* Configure ydotool service and socket permissions
- *(workstation,base,audio)* Add OS verification and enhance system configurations
- *(osbuild)* Update workstation config and add refactor todo
- *(systemd-networkd)* Add role for systemd-networkd and resolved configuration

### 🐛 Bug Fixes

- *(nas)* Add missing firewall.nfs.ports variable structure

### 🚜 Refactor

- *(repos)* Consolidate repository priority configuration
- *(kiwi)* Update schema to 8.3 and refine config
- *(video)* Wrap nvidia tasks in detection block
- *(base)* Consolidate repos and common roles into base role
- Move user vars to inventory and migrate rust utils to base role
- *(audio)* Switch NoiseTorch install to binary release
- *(base)* Reorganize tasks and update package/repo configuration
- *(workstation)* Improve NVIDIA detection and update repository settings
- *(docker)* Migrate playbook to role and add storage configuration

### 📚 Documentation

- *(knowledge-base)* Init hierarchical AGENTS.md files
- Rewrite README + add Claude agents for RHEL workflows
- Add workstation collection architect agent definition
- Enhance README readability by adjusting table formatting, adding a KIWI documentation link, and specifying shell for a code block.
- Add changelog and significantly update READMEs
- *(agents)* Expand agent documentation and context files
- *(changelog)* Update CHANGELOG.md with recent changes
- Add AGENTS.md context files to roles

### ⚙️ Miscellaneous Tasks

- *(agents)* Consolidate architect agents and workflows
- *(asdf)* Update plugin selection and dependency installation
- Added ide config to gitignore and updated the changelog
- Added gum package to role vars and base image template
