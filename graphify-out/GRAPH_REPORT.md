# Graph Report - .  (2026-05-08)

## Corpus Check
- Corpus is ~34,292 words - fits in a single context window. You may not need a graph.

## Summary
- 187 nodes · 200 edges · 49 communities (25 shown, 24 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Ansible LLM Callback Analyzer|Ansible LLM Callback Analyzer]]
- [[_COMMUNITY_Sway Systemd Manager Core|Sway Systemd Manager Core]]
- [[_COMMUNITY_Sway Systemd Cgroup Assignment|Sway Systemd Cgroup Assignment]]
- [[_COMMUNITY_AI Provider Integration|AI Provider Integration]]
- [[_COMMUNITY_Sway Keybinding Documentation|Sway Keybinding Documentation]]
- [[_COMMUNITY_OS Image Building|OS Image Building]]
- [[_COMMUNITY_Audio Normalization Utilities|Audio Normalization Utilities]]
- [[_COMMUNITY_NAS Storage Services|NAS Storage Services]]
- [[_COMMUNITY_Workstation Task Orchestration|Workstation Task Orchestration]]
- [[_COMMUNITY_AI Pattern Automation|AI Pattern Automation]]
- [[_COMMUNITY_Video & oneAPI Configuration|Video & oneAPI Configuration]]
- [[_COMMUNITY_Pro Audio & JackTrip|Pro Audio & JackTrip]]
- [[_COMMUNITY_Display & Network Management|Display & Network Management]]
- [[_COMMUNITY_Cgroup Resource Management|Cgroup Resource Management]]
- [[_COMMUNITY_Configuration Layering|Configuration Layering]]
- [[_COMMUNITY_Shell & Tool Management|Shell & Tool Management]]
- [[_COMMUNITY_Pipewire Pro Audio|Pipewire Pro Audio]]
- [[_COMMUNITY_Unified Networking Strategy|Unified Networking Strategy]]
- [[_COMMUNITY_Noise Cancellation|Noise Cancellation]]
- [[_COMMUNITY_AI Pattern Framework|AI Pattern Framework]]
- [[_COMMUNITY_VSCode Configuration|VSCode Configuration]]
- [[_COMMUNITY_Workstation Playbook|Workstation Playbook]]
- [[_COMMUNITY_Security Hardening (SELinux)|Security Hardening (SELinux)]]
- [[_COMMUNITY_Sway Systemd Manager Rationale|Sway Systemd Manager Rationale]]
- [[_COMMUNITY_Sway Systemd Manager Rationale|Sway Systemd Manager Rationale]]
- [[_COMMUNITY_Sway Cgroup Assignment Rationale|Sway Cgroup Assignment Rationale]]
- [[_COMMUNITY_Sway Cgroup Assignment Rationale|Sway Cgroup Assignment Rationale]]
- [[_COMMUNITY_Workstation Defaults|Workstation Defaults]]
- [[_COMMUNITY_Workstation Flatpaks|Workstation Flatpaks]]
- [[_COMMUNITY_NAS Defaults|NAS Defaults]]
- [[_COMMUNITY_NAS Handlers|NAS Handlers]]
- [[_COMMUNITY_Kiwi Defaults|Kiwi Defaults]]
- [[_COMMUNITY_Wireless Configuration|Wireless Configuration]]
- [[_COMMUNITY_KVM over IP Concept|KVM over IP Concept]]
- [[_COMMUNITY_Fedora Specific Variables|Fedora Specific Variables]]

## God Nodes (most connected - your core abstractions)
1. `CallbackModule` - 19 edges
2. `AIProvider` - 12 edges
3. `CGroupHandler` - 8 edges
4. `CGroupHandler` - 8 edges
5. `get_cgroup()` - 5 edges
6. `assign_scope()` - 5 edges
7. `get_cgroup()` - 5 edges
8. `assign_scope()` - 5 edges
9. `main()` - 4 edges
10. `main_async()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `AI Code Analysis` --conceptually_related_to--> `RamaLama Tasks`  [INFERRED]
  plugins/callback/llm_analyzer.py → roles/ramalama/tasks/main.yml
- `AI Code Analysis` --conceptually_related_to--> `Execution Environment`  [INFERRED]
  plugins/callback/llm_analyzer.py → meta/execution-environment.yml
- `Video Tasks Main` --conceptually_related_to--> `oneAPI Playbook`  [INFERRED]
  roles/video/tasks/main.yml → playbooks/oneAPI.yml
- `Audio Defaults` --conceptually_related_to--> `JackTrip Pi Playbook`  [INFERRED]
  roles/audio/defaults/main.yml → playbooks/jacktrip-pi.yml
- `OSBuild Tasks Main` --calls--> `Build Workstation Image Playbook`  [EXTRACTED]
  roles/osbuild/tasks/main.yml → playbooks/build-workstation-image.yml

## Communities (49 total, 24 thin omitted)

### Community 0 - "Ansible LLM Callback Analyzer"
Cohesion: 0.1
Nodes (15): CallbackModule, Save analysis to a markdown file., Save structured suggestions for LLM processing., Analyze YAML content for Ansible style guide violations.          Args:, Generate structured suggestions for LLM processing in DSPy format.          Args, Convert a style violation to an actionable suggestion., Generate fix for variable naming violations., Generate fix for tag naming violations. (+7 more)

### Community 1 - "Sway Systemd Manager Core"
Cohesion: 0.12
Nodes (16): assign_scope(), CGroupHandler, get_x11_window_pid(), window:new IPC event handler, Main logic: handle i3/sway IPC events and start systemd transient units., asynchronous initialization code, Get PID from IPC response (sway), X-Resource or _NET_WM_PID (i3), Check criteria for assigning current app into an isolated cgroup (+8 more)

### Community 2 - "Sway Systemd Cgroup Assignment"
Cohesion: 0.13
Nodes (18): assign_scope(), CGroupHandler, create_x11_pid_getter(), escape_app_id(), get_cgroup(), get_pid_by_socket(), get_x11_window_pid(), main() (+10 more)

### Community 4 - "Sway Keybinding Documentation"
Cohesion: 0.36
Nodes (8): DocsConfig, findKeybindingForLine(), getDocsConfig(), getDocsList(), getSymbolDict(), replaceBindingFromMap(), sanitize(), translate()

### Community 5 - "OS Image Building"
Cohesion: 0.33
Nodes (6): Build Workstation Image Playbook, Image Building, KIWI Tasks Main, OSBuild Tasks Main, KIWI Deprecation Rationale, OSBuild Migration Rationale

### Community 7 - "NAS Storage Services"
Cohesion: 0.4
Nodes (5): NAS Tasks Main, NAS NFS Tasks, NAS Rsync Tasks, NAS Samba Tasks, Hybrid Firewall Approach

### Community 9 - "Workstation Task Orchestration"
Cohesion: 0.5
Nodes (4): Workstation Antigravity Tasks, Workstation Browser Tasks, Workstation Tasks Main, Workstation VSCode Tasks

### Community 10 - "AI Pattern Automation"
Cohesion: 0.5
Nodes (3): AI Code Analysis, Execution Environment, RamaLama Tasks

### Community 11 - "Video & oneAPI Configuration"
Cohesion: 0.67
Nodes (3): OSBuild Defaults, oneAPI Playbook, Video Tasks Main

### Community 12 - "Pro Audio & JackTrip"
Cohesion: 0.67
Nodes (3): Audio Defaults, Audio Modernization (Pipewire), JackTrip Pi Playbook

### Community 13 - "Display & Network Management"
Cohesion: 0.67
Nodes (3): Display Manager Tasks, Sway Tasks Main, Systemd-Networkd Tasks

## Knowledge Gaps
- **78 isolated node(s):** `Get cgroup identifier for the process specified by pid.     Assumes cgroups v2 u`, `getsockopt (..., SO_PEERCRED, ...) returns the following structure     struct uc`, `Escape app_id for systemd APIs.      The "unit prefix" must consist of one or mo`, `Create fallback X11 PID getter.      Sway 1.6.1/wlroots 0.14 can use XRes to get`, `Main logic: handle i3/sway IPC events and start systemd transient units.` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CallbackModule` connect `Ansible LLM Callback Analyzer` to `AI Provider Integration`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `main_async()` connect `Sway Systemd Cgroup Assignment` to `Sway Systemd Manager Core`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Get cgroup identifier for the process specified by pid.     Assumes cgroups v2 u`, `getsockopt (..., SO_PEERCRED, ...) returns the following structure     struct uc`, `Escape app_id for systemd APIs.      The "unit prefix" must consist of one or mo` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ansible LLM Callback Analyzer` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Sway Systemd Manager Core` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Sway Systemd Cgroup Assignment` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._