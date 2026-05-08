# Graph Report - ansible-collection-rhel-workstation-builder  (2026-05-08)

## Corpus Check
- 26 files · ~38,090 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 187 nodes · 200 edges · 49 communities (25 shown, 24 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ba6692b5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Ansible Callback LLM Analyzer|Ansible Callback LLM Analyzer]]
- [[_COMMUNITY_Sway Systemd Cgroup Manager|Sway Systemd Cgroup Manager]]
- [[_COMMUNITY_AI Provider Integrations|AI Provider Integrations]]
- [[_COMMUNITY_SBDP Keybinding Documentation|SBDP Keybinding Documentation]]
- [[_COMMUNITY_OS Image Building Strategy|OS Image Building Strategy]]
- [[_COMMUNITY_Audio Normalization Tools|Audio Normalization Tools]]
- [[_COMMUNITY_NAS Storage Configuration|NAS Storage Configuration]]
- [[_COMMUNITY_Waybar & Notification Scripts|Waybar & Notification Scripts]]
- [[_COMMUNITY_Workstation Task Orchestration|Workstation Task Orchestration]]
- [[_COMMUNITY_Video & Graphics Acceleration|Video & Graphics Acceleration]]
- [[_COMMUNITY_Audio Stack & Distribution|Audio Stack & Distribution]]
- [[_COMMUNITY_Display & Network Management|Display & Network Management]]
- [[_COMMUNITY_Cgroup Resource Management|Cgroup Resource Management]]
- [[_COMMUNITY_Configuration Layering|Configuration Layering]]
- [[_COMMUNITY_Shell & Version Management|Shell & Version Management]]
- [[_COMMUNITY_Pro Audio Configuration|Pro Audio Configuration]]
- [[_COMMUNITY_Unified Networking Strategy|Unified Networking Strategy]]
- [[_COMMUNITY_Noise Cancellation Tools|Noise Cancellation Tools]]
- [[_COMMUNITY_VSCode Configuration|VSCode Configuration]]
- [[_COMMUNITY_AI Pattern Automation|AI Pattern Automation]]
- [[_COMMUNITY_Security Hardening (SELinux)|Security Hardening (SELinux)]]
- [[_COMMUNITY_Workstation Playbook|Workstation Playbook]]
- [[_COMMUNITY_X11 PID Handling|X11 PID Handling]]
- [[_COMMUNITY_Systemd Slice Management|Systemd Slice Management]]
- [[_COMMUNITY_Component 25|Component 25]]
- [[_COMMUNITY_Component 29|Component 29]]
- [[_COMMUNITY_Component 30|Component 30]]
- [[_COMMUNITY_Component 41|Component 41]]
- [[_COMMUNITY_Component 42|Component 42]]
- [[_COMMUNITY_Component 43|Component 43]]
- [[_COMMUNITY_Component 44|Component 44]]
- [[_COMMUNITY_Component 45|Component 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]

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
- `RamaLama Tasks` --conceptually_related_to--> `AI Code Analysis`  [INFERRED]
  roles/ramalama/tasks/main.yml → plugins/callback/llm_analyzer.py
- `Execution Environment` --conceptually_related_to--> `AI Code Analysis`  [INFERRED]
  meta/execution-environment.yml → plugins/callback/llm_analyzer.py
- `oneAPI Playbook` --conceptually_related_to--> `Video Tasks Main`  [INFERRED]
  playbooks/oneAPI.yml → roles/video/tasks/main.yml
- `JackTrip Pi Playbook` --conceptually_related_to--> `Audio Defaults`  [INFERRED]
  playbooks/jacktrip-pi.yml → roles/audio/defaults/main.yml
- `Build Workstation Image Playbook` --calls--> `OSBuild Tasks Main`  [EXTRACTED]
  playbooks/build-workstation-image.yml → roles/osbuild/tasks/main.yml

## Communities (49 total, 24 thin omitted)

### Community 0 - "Ansible Callback LLM Analyzer"
Cohesion: 0.1
Nodes (15): CallbackModule, Save analysis to a markdown file., Save structured suggestions for LLM processing., Analyze YAML content for Ansible style guide violations.          Args:, Generate structured suggestions for LLM processing in DSPy format.          Args, Convert a style violation to an actionable suggestion., Generate fix for variable naming violations., Generate fix for tag naming violations. (+7 more)

### Community 1 - "Sway Systemd Cgroup Manager"
Cohesion: 0.12
Nodes (16): assign_scope(), CGroupHandler, get_x11_window_pid(), window:new IPC event handler, Main logic: handle i3/sway IPC events and start systemd transient units., asynchronous initialization code, Get PID from IPC response (sway), X-Resource or _NET_WM_PID (i3), Check criteria for assigning current app into an isolated cgroup (+8 more)

### Community 2 - "AI Provider Integrations"
Cohesion: 0.13
Nodes (18): assign_scope(), CGroupHandler, create_x11_pid_getter(), escape_app_id(), get_cgroup(), get_pid_by_socket(), get_x11_window_pid(), main() (+10 more)

### Community 4 - "OS Image Building Strategy"
Cohesion: 0.36
Nodes (8): DocsConfig, findKeybindingForLine(), getDocsConfig(), getDocsList(), getSymbolDict(), replaceBindingFromMap(), sanitize(), translate()

### Community 5 - "Audio Normalization Tools"
Cohesion: 0.33
Nodes (6): Build Workstation Image Playbook, Image Building, KIWI Tasks Main, OSBuild Tasks Main, KIWI Deprecation Rationale, OSBuild Migration Rationale

### Community 7 - "Waybar & Notification Scripts"
Cohesion: 0.4
Nodes (5): NAS Tasks Main, NAS NFS Tasks, NAS Rsync Tasks, NAS Samba Tasks, Hybrid Firewall Approach

### Community 9 - "Workstation Task Orchestration"
Cohesion: 0.5
Nodes (4): Workstation Antigravity Tasks, Workstation Browser Tasks, Workstation Tasks Main, Workstation VSCode Tasks

### Community 10 - "Video & Graphics Acceleration"
Cohesion: 0.5
Nodes (3): AI Code Analysis, Execution Environment, RamaLama Tasks

### Community 11 - "Audio Stack & Distribution"
Cohesion: 0.67
Nodes (3): OSBuild Defaults, oneAPI Playbook, Video Tasks Main

### Community 12 - "Display & Network Management"
Cohesion: 0.67
Nodes (3): Audio Defaults, Audio Modernization (Pipewire), JackTrip Pi Playbook

### Community 13 - "Cgroup Resource Management"
Cohesion: 0.67
Nodes (3): Display Manager Tasks, Sway Tasks Main, Systemd-Networkd Tasks

## Knowledge Gaps
- **78 isolated node(s):** `Get cgroup identifier for the process specified by pid.     Assumes cgroups v2 u`, `getsockopt (..., SO_PEERCRED, ...) returns the following structure     struct uc`, `Escape app_id for systemd APIs.      The "unit prefix" must consist of one or mo`, `Create fallback X11 PID getter.      Sway 1.6.1/wlroots 0.14 can use XRes to get`, `Main logic: handle i3/sway IPC events and start systemd transient units.` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CallbackModule` connect `Ansible Callback LLM Analyzer` to `SBDP Keybinding Documentation`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `main_async()` connect `AI Provider Integrations` to `Sway Systemd Cgroup Manager`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Get cgroup identifier for the process specified by pid.     Assumes cgroups v2 u`, `getsockopt (..., SO_PEERCRED, ...) returns the following structure     struct uc`, `Escape app_id for systemd APIs.      The "unit prefix" must consist of one or mo` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ansible Callback LLM Analyzer` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Sway Systemd Cgroup Manager` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `AI Provider Integrations` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._