```markdown
# ansible-rhel-workstation-builder Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches you how to contribute to the `ansible-rhel-workstation-builder` repository, which automates the configuration and provisioning of RHEL-based workstations using Ansible roles and playbooks. You'll learn the project's coding conventions, how to add or refactor roles, expand OS support, update documentation, and manage playbooks following established workflows and commit practices.

---

## Coding Conventions

- **Language:** Python (for any supporting scripts)
- **Framework:** None detected (Ansible-based project)
- **File Naming:** Uses camelCase for file names.
  - Example: `myRoleName.py`, `mainTasks.yml`
- **Import Style:** Relative imports in Python scripts.
  - Example:
    ```python
    from .utils import helper_function
    ```
- **Export Style:** Named exports (functions/classes are explicitly exported).
  - Example:
    ```python
    def my_function():
        pass
    ```
- **Commit Messages:** Conventional commits with prefixes like `feat`, `docs`, `refactor`.
  - Example: `feat(audio): add support for PipeWire configuration`

---

## Workflows

### Add New Ansible Role
**Trigger:** When introducing a new functional area (e.g., audio, podman, video) as a reusable Ansible role.  
**Command:** `/new-role`

1. Create a new directory under `roles/<role-name>/`.
2. Add documentation files: `README.md` and `AGENTS.md` for context.
3. Add Ansible role structure:
    - `defaults/main.yml`
    - `handlers/main.yml`
    - `meta/main.yml`
    - `tasks/main.yml`
    - (Optionally) `vars/main.yml`
4. Add `templates/` and/or `files/` for configuration or scripts as needed.
5. Add tests:
    - `tests/inventory`
    - `tests/test.yml`
6. Update `playbooks/<playbook>.yml` to include the new role if required.

**Example Directory Structure:**
```
roles/
  myrole/
    README.md
    AGENTS.md
    defaults/
      main.yml
    handlers/
      main.yml
    meta/
      main.yml
    tasks/
      main.yml
    vars/
      main.yml
    templates/
    files/
    tests/
      inventory
      test.yml
```

---

### Expand Role with New Feature or OS Support
**Trigger:** When adding new functionality (e.g., Flatpak, browser) or OS-specific logic (e.g., Fedora, Rocky) to an existing role.  
**Command:** `/role-feature`

1. Add or update `tasks/<feature>.yml` or `tasks/<os>.yml` in the role.
2. Add or update `vars/<OS>.yml` or `defaults/main.yml` for new variables.
3. Update `tasks/main.yml` to include the new task file.
4. Update `README.md` or `AGENTS.md` for documentation.
5. Optionally update the playbook to include the new task/role.

**Example Task Inclusion:**
```yaml
# roles/myrole/tasks/main.yml
- include_tasks: flatpak.yml
  when: ansible_os_family == "Fedora"
```

---

### Refactor or Consolidate Roles
**Trigger:** When merging, splitting, or reorganizing roles to improve maintainability or remove duplication.  
**Command:** `/refactor-role`

1. Move or merge tasks, handlers, defaults, templates, and vars between roles as needed.
2. Update playbooks to reference new role names or paths.
3. Remove deprecated or redundant files.
4. Update `README.md` and `AGENTS.md` to reflect changes.

**Example Refactor:**
- Move common handlers from `roles/audio/handlers/main.yml` to `roles/common/handlers/main.yml`.
- Update playbooks to use `common` role instead of `audio` for those handlers.

---

### Add or Update Documentation and Agents
**Trigger:** When documenting new features, updating usage instructions, or adding agent/workflow context.  
**Command:** `/doc-update`

1. Add or update `README.md` in roles or the project root.
2. Add or update `AGENTS.md` in relevant directories.
3. Update or create `CHANGELOG.md`.
4. Optionally update files in `docs/` or other meta directories.

**Example:**
- Add a new section to `roles/podman/README.md` describing Fedora support.
- Update `CHANGELOG.md` with the new feature.

---

### Add or Update Playbook
**Trigger:** When automating a new workflow or integrating new/existing roles into a deployment scenario.  
**Command:** `/new-playbook`

1. Create or update `playbooks/<playbook>.yml`.
2. Add or update `inventory/inventory.ini` as needed.
3. Reference new or updated roles in the playbook.
4. Optionally update `AGENTS.md` or other documentation.

**Example Playbook:**
```yaml
# playbooks/dev-workstation.yml
- hosts: all
  roles:
    - audio
    - podman
    - video
```

---

## Testing Patterns

- **Testing Framework:** Unknown (Ansible role testing is typically done via `ansible-playbook` or Molecule, but not detected here).
- **Test File Pattern:** `*.test.ts` (suggests some TypeScript test files, possibly for supporting scripts).
- **Role Testing:** Each role has a `tests/` directory with:
    - `inventory` file
    - `test.yml` playbook

**Example:**
```
roles/myrole/tests/
  inventory
  test.yml
```
Run with:
```bash
ansible-playbook -i roles/myrole/tests/inventory roles/myrole/tests/test.yml
```

---

## Commands

| Command        | Purpose                                                                 |
|----------------|------------------------------------------------------------------------|
| /new-role      | Scaffold a new Ansible role with all required files and documentation   |
| /role-feature  | Add a new feature or OS support to an existing role                    |
| /refactor-role | Refactor, merge, or reorganize existing roles                          |
| /doc-update    | Add or update documentation and agent context                           |
| /new-playbook  | Create or update a playbook to automate new workflows                  |
```
