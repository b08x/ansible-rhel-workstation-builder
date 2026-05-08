# Sway Systemd Cgroup Manager

> 23 nodes · cohesion 0.14

## Key Concepts

- **assign-cgroups.py** (8 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **CGroupHandler** (8 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **._on_new_window()** (6 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **assign_scope()** (5 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **.connect()** (5 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **get_cgroup()** (5 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **.cgroup_change_needed()** (4 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **.get_pid()** (4 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **create_x11_pid_getter()** (3 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **escape_app_id()** (3 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **get_pid_by_socket()** (3 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **get_x11_window_pid()** (3 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **main()** (3 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **.__init__()** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Create fallback X11 PID getter.      Sway 1.6.1/wlroots 0.14 can use XRes to get** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Main logic: handle i3/sway IPC events and start systemd transient units.** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **asynchronous initialization code** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Get PID from IPC response (sway), X-Resource or _NET_WM_PID (i3)** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Check criteria for assigning current app into an isolated cgroup** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **window:new IPC event handler** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Escape app_id for systemd APIs.      The "unit prefix" must consist of one or mo** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **Get cgroup identifier for the process specified by pid.     Assumes cgroups v2 u** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`
- **getsockopt (..., SO_PEERCRED, ...) returns the following structure     struct uc** (1 connections) — `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `roles/sway/files/usr/libexec/sway-systemd/assign-cgroups.py`

## Audit Trail

- EXTRACTED: 70 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*