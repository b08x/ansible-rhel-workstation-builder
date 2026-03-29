---
name: add-new-ansible-role
description: Workflow command scaffold for add-new-ansible-role in ansible-rhel-workstation-builder.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-new-ansible-role

Use this workflow when working on **add-new-ansible-role** in `ansible-rhel-workstation-builder`.

## Goal

Adds a new Ansible role to the project, including its default variables, handlers, meta, tasks, templates/files, tests, and README documentation.

## Common Files

- `roles/<role-name>/README.md`
- `roles/<role-name>/defaults/main.yml`
- `roles/<role-name>/handlers/main.yml`
- `roles/<role-name>/meta/main.yml`
- `roles/<role-name>/tasks/main.yml`
- `roles/<role-name>/vars/main.yml`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create role directory under roles/<role-name>/
- Add README.md and AGENTS.md for documentation/context
- Add defaults/main.yml, handlers/main.yml, meta/main.yml, tasks/main.yml, and (optionally) vars/main.yml
- Add templates/ and/or files/ as needed for configuration/scripts
- Add tests/inventory and tests/test.yml for role testing

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.