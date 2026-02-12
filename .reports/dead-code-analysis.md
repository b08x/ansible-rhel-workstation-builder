# Dead Code Analysis Report
**Generated**: 2026-01-31 19:51:00 EST
**Project**: ansible-rhel-workstation-builder
**Scope**: Complete collection (focus on osbuild role)

---

## Executive Summary

Found **60+ items** of potentially dead code across 4 categories:
- 🟢 **SAFE** (26 items): Orphaned files, empty directories
- 🟡 **CAUTION** (13 items): Unused task files, nearly empty vars
- 🔴 **DANGER** (35+ items): TOML blueprints, handlers
- ⚠️ **IN DEVELOPMENT** (1 role): osbuild role not yet functional

**Recommendation**: Start with SAFE items, proceed cautiously with CAUTION items.

---

## 🔴 DANGER: OSBuild Role Status

### Critical Context
**The osbuild role does NOT function yet** - user is building ISOs manually using:
```bash
# Manual command (from todo.md)
sudo image-builder build minimal-installer --distro fedora-43 \
  --extra-repo "https://developer.download.nvidia.com/compute/cuda/repos/fedora42/x86_64" \
  --extra-repo "http://dl.google.com/linux/chrome/rpm/stable/x86_64" \
  --blueprint workstation/fedora-43-workstation-nvidia.toml
```

### Currently Used Files
✅ **KEEP THESE**:
- `/roles/osbuild/files/fedora/43/x86_64/workstation/fedora-43-workstation-nvidia.toml` (660 lines)
- Role infrastructure (tasks/, handlers/, defaults/, templates/)

### Potentially Dead TOML Files (35 files)

**Fedora 42 Blueprints** (4 files - 🔴 REVIEW):
```
roles/osbuild/files/fedora/42/x86_64/workstation/fedora-42-workstation-nvidia.toml
roles/osbuild/files/fedora/42/x86_64/workstation/fedora-42-workstation.toml
roles/osbuild/files/fedora/42/x86_64/workstation/fedora-42-vagrant-workstation-nvidia.toml
roles/osbuild/files/fedora/42/x86_64/workstation/fedora-42-vagrant-workstation.toml
```

**Fedora 42 Live ISOs** (2 files - 🔴 REVIEW):
```
roles/osbuild/files/fedora/42/x86_64/live/fedora-workstation-live-iso-nvidia.toml
roles/osbuild/files/fedora/42/x86_64/live/fedora-workstation-live-iso.toml
```

**Repository Source Definitions** (29 files - 🟡 NEEDED FOR AUTOMATION):
```
# Fedora 42 sources (13 files)
roles/osbuild/files/fedora/42/x86_64/sources/*.toml

# Fedora 43 sources (16 files)  
roles/osbuild/files/fedora/43/x86_64/sources/*.toml
```

**Decision**: 
- **DELETE** Fedora 42 blueprints/live ISOs if focusing on Fedora 43 only
- **KEEP** source definitions (needed for image-builder CLI migration per todo.md)
- **CONSOLIDATE** package lists (per todo.md line 6)

---

## 🟢 SAFE: Orphaned Files (26 items)

### Category 1: Mock Configuration Templates (14 files)
**Location**: `roles/rpm-dev/files/etc/mock/templates/`
**Issue**: Templates stored in `files/` instead of `templates/` directory

```
fedora-43-x86_64.cfg
fedora-43-x86_64-debug.cfg
fedora-43-x86_64-dev.cfg
fedora-43-x86_64-gcc13.cfg
fedora-43-x86_64-gcc14.cfg
fedora-43-x86_64-llvm-toolset-7.cfg
fedora-43-x86_64-llvm-toolset-7-clang.cfg
fedora-43-x86_64-mingw.cfg
fedora-43-x86_64-roselyn.cfg
fedora-43-x86_64-scl.cfg
fedora-43-x86_64-scl-dev.cfg
fedora-43-x86_64-scl-mingw.cfg
fedora-43-x86_64-swift.cfg
fedora-44-x86_64.cfg
fedora-44-x86_64-debug.cfg
```

**Status**: ❌ NEVER referenced in any task
**Recommendation**: 
1. Move to `roles/rpm-dev/templates/` if needed
2. Update tasks to use `ansible.builtin.template:` module
3. Or delete if rpm-dev role doesn't need these

### Category 2: ZSH Files (3 files)
**Location**: `roles/rpm-dev/files/oh-my-zsh/`

```
custom/plugins/ansible
custom/plugins/roles
custom/zshrc.symlink
before.remote
```

**Status**: ❌ NEVER referenced in any task
**Note**: Wrong role - should be in `roles/zsh/files/` if needed
**Recommendation**: DELETE (zsh role has its own file structure)

### Category 3: Empty Directories (11 directories)

```
roles/workstation/templates
roles/kiwi/vars
roles/kiwi/files/fedora/43/x86_64/scripts
roles/kiwi/files/fedora/43/x86_64/live
roles/asdf/files
roles/base/vars
roles/base/meta
roles/osbuild/files/fedora/43/x86_64/fedora-43-minimal-installer-x86_64
roles/video/vars
roles/video/meta
roles/ramalama/files
```

**Recommendation**: 
- **DELETE** if confirmed empty with: `find <dir> -type f | wc -l`
- Keep if placeholders are needed for future development

---

## 🟡 CAUTION: Unused Task Files (7 files)

### asdf role (3 files)
**Status**: Commented out in `main.yml` (lines 65-127)

```yaml
roles/asdf/tasks/node.yml    # Node.js plugin setup
roles/asdf/tasks/ruby.yml    # Ruby plugin setup  
roles/asdf/tasks/uv.yml      # UV package manager
```

**Root Cause**: TODO comments in main.yml indicate incomplete implementation
```yaml
# TODO: add .default-gems file
# TODO: add .default-python-packages file
# TODO: add .default-nodejs-packages file
```

**Recommendation**:
1. **KEEP** if planning to enable language version management
2. **DELETE** if using system-wide package managers instead

### audio role (3 files)

```yaml
roles/audio/tasks/applications.yml         # Audio production applications
roles/audio/tasks/configure_pipewire.yml   # User-specific PipeWire config
roles/audio/tasks/pipewire.yml             # Unified PipeWire stack
```

**Currently Used**: `tuning.yml`, `noisetorch.yml`, `packages.yml`

**Recommendation**:
- **REVIEW** if audio production features are planned
- **DELETE** if focusing on basic audio only

### workstation role (1 file)

```yaml
roles/workstation/tasks/flatpaks.yml
```

**Currently Used**: `browser.yml`, `ide.yml`

**Recommendation**:
- **KEEP** if planning Flatpak support
- **DELETE** if using RPM packages exclusively

---

## 🟡 CAUTION: Nearly Empty Vars Files (6 files)

Empty `vars/main.yml` files (1-3 lines, just comments/license):

```
roles/asdf/vars/main.yml         (3 lines)
roles/nas/vars/main.yml          (2 lines)
roles/osbuild/vars/main.yml      (3 lines) ✅ EXPECTED - everything in defaults/
roles/ramalama/vars/main.yml     (3 lines)
roles/workstation/vars/main.yml  (2 lines)
roles/zsh/vars/main.yml          (1 line)
```

**Recommendation**:
- **KEEP** if role uses only `defaults/main.yml` (normal pattern)
- **DELETE** if no variables exist in either location

---

## 🟢 SAFE: Unused Handlers

Handlers defined but NEVER notified in any task:

### audio role
```yaml
- Enable and restart rtirq service
- Enable and restart rtkit service  
- reload sysctl
```

### base role
```yaml
- Generate locales
- Rebuild grub
- Daemon reload
- Restart cpupower service
```

### kiwi role
```yaml
- restore_selinux
- cleanup_build_artifacts
```

### nas role
```yaml
- Reload firewalld
- Restart NFS server
- Restart NFS idmapd
- Reload NFS exports
- Restart rpcbind
- Restart Samba
- Restart Samba NetBIOS
- Reload Samba
- Restart rsync daemon
- Reload rsync daemon
```

### osbuild role
```yaml
- Reload systemd daemon
- Refresh composer sources
```

### rpm-dev role
```yaml
- "Reset mock configuration"
```

### sway role
```yaml
- Reload sway
```

**Note**: Only 3 handlers are actively used:
- "Clear mock cache" (3 notifications)
- "Restart Docker" (2 notifications)
- "Daemon reload" (2 notifications)

**Recommendation**:
- **REVIEW** each handler - may be needed for future functionality
- **DELETE** if confirmed unused after code review

---

## 🔵 INFO: TODOs Found (4 comments)

### asdf role (`tasks/main.yml` lines 61-63)
```yaml
# TODO: add .default-gems file
# TODO: add .default-python-packages file
# TODO: add .default-nodejs-packages file
```

### workstation role (`tasks/main.yml` line 46)
```yaml
# TODO: run ydotoold as a user service (systemctl --user enable ydotool.service), which creates the socket in your user's runtime directory (e.g., /run/user/1000/.ydotool_socket)
```

**Recommendation**: Track these as feature requests, not dead code

---

## 📋 Cleanup Recommendations

### Phase 1: SAFE Deletions (No Testing Required)

```bash
# 1. Remove orphaned ZSH files from wrong role
rm -rf roles/rpm-dev/files/oh-my-zsh/
rm -f roles/rpm-dev/files/before.remote

# 2. Remove empty directories (verify first!)
rmdir roles/workstation/templates
rmdir roles/kiwi/vars
rmdir roles/kiwi/files/fedora/43/x86_64/scripts
rmdir roles/kiwi/files/fedora/43/x86_64/live
rmdir roles/asdf/files
rmdir roles/base/vars
rmdir roles/base/meta
rmdir roles/osbuild/files/fedora/43/x86_64/fedora-43-minimal-installer-x86_64
rmdir roles/video/vars
rmdir roles/video/meta
rmdir roles/ramalama/files

# 3. Remove Fedora 42 blueprints (if focusing on Fedora 43)
rm -rf roles/osbuild/files/fedora/42/
```

### Phase 2: CAUTION - Delete After Review

```bash
# 1. Unused task files (verify not planning to use)
rm -f roles/asdf/tasks/{node,ruby,uv}.yml
rm -f roles/audio/tasks/{applications,configure_pipewire,pipewire}.yml
rm -f roles/workstation/tasks/flatpaks.yml

# 2. Mock templates (if not needed)
rm -rf roles/rpm-dev/files/etc/mock/templates/
```

### Phase 3: OSBuild Role Migration (Per todo.md)

```yaml
# From roles/osbuild/todo.md:
# 1. Refactor to use image-builder CLI instead of composer-cli
# 2. Create Jinja2 template(s) for blueprint file(s)
# 3. Consolidate all package lists to single source

# Action: Complete role migration before cleaning up TOML files
```

---

## ⚠️ Important Notes

1. **No Testing Framework Detected**: Project lacks Molecule or test playbooks
   - Cannot verify deletions are safe via automated tests
   - Manual verification required

2. **OSBuild Role**: Currently non-functional
   - Do NOT delete files until role migration complete
   - User building manually with fedora-43-workstation-nvidia.toml

3. **Handlers**: May be needed for future functionality
   - Review each handler before deletion
   - Some may be triggered conditionally

4. **TOML Files**: Source definitions likely needed
   - Keep for image-builder CLI migration
   - Only delete Fedora 42 blueprints if not needed

---

## Next Steps

1. ✅ Review this report
2. 🔍 Verify empty directories are truly empty
3. 🗑️ Execute Phase 1 deletions (safe)
4. 📝 Decide on Phase 2 items (task files, handlers)
5. 🚀 Complete osbuild role migration before cleaning TOML files
6. ✅ Run `ansible-lint` and `yamllint` after cleanup

---

**Generated by**: Sisyphus (OhMyClaude Code)
**Analysis Tools**: 4 parallel explore agents + direct grep/ast-grep
**Duration**: ~5 minutes
