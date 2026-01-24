# WORKSTATION ROLE KNOWLEDGE BASE

Application installation role - **PRIMARY TARGET** for GenAI tools integration and language environment management.

## WHERE TO LOOK
| Task                   | File                      | Notes                             |
|------------------------|---------------------------|-----------------------------------|
| **Browser Install**    | `tasks/google-chrome.yml` | Google Chrome (non-standard repo) |
| **IDE Setup**          | `tasks/ide.yml`           | Development environments          |
| **Rust Utilities**     | `tasks/rust_utils.yml`    | Cargo-based CLI tools             |
| **YADM Dotfiles**      | `tasks/yadm.yml`          | Yet Another Dotfiles Manager      |
| **Main Orchestration** | `tasks/main.yml`          | Includes component-specific tasks |
| **Package Variables**  | `vars/main.yml`           | Workstation-specific packages     |

## CONVENTIONS
- **Component-Specific Tasks**: Named after tools (google-chrome.yml, not install-browser.yml)
- **Include Pattern**: `main.yml` dynamically includes task files
- **Third-Party Repos**: Manages non-standard repos (Chrome, RPM Fusion)
- **User Applications**: System-wide installs (not user-local)
- **Application-Specific Task Files**: Tasks organized by application/tool
- **Jinja2 Templates**: Dynamic configurations for application setups

## CONSOLIDATION OBJECTIVES

### **GenAI Tools Integration** (PRIMARY)
Add the following tools to this role:

| Tool            | Type              | Installation Method  | Notes                                  |
|-----------------|-------------------|----------------------|----------------------------------------|
| **ollama**      | LLM runtime       | Official repo/script | Systemd service, model management      |
| **whisper.cpp** | Speech-to-text    | Manual build/tarball | CUDA support optional, model downloads |
| **gemini-cli**  | Google Gemini CLI | pip/manual           | API key management (secrets.yml)       |
| **claude-code** | Anthropic CLI     | npm/manual           | API key management, project config     |
| **opencode**    | Oh My OpenCode    | git clone/script     | Shell integration, plugin system       |

**Implementation Strategy:**
- Create `tasks/genai.yml` for unified GenAI tool installation
- Split into subtasks: `tasks/genai/ollama.yml`, `tasks/genai/whisper.yml`, etc.
- Add variables: `workstation_enable_genai`, `genai_tools_list`
- Manage API keys via Ansible Vault in `vars/secrets.yml`
- Consider systemd units for ollama service management

## ANTI-PATTERNS (THIS ROLE)
- **Minimal Package Consolidation**: Duplicates common packages from other roles
- **No GenAI Tool Support**: Currently missing planned tools
- **No Language Version Managers**: Ruby/Python installed system-wide only
- **Non-Standard Task Names**: Task files named after applications/tools (existing convention, not changing)

## UNIQUE STYLES
- **Application Focus**: Unlike infrastructure roles, focuses on end-user applications
- **Third-Party Repo Heavy**: Manages non-standard package sources
- **Future Expansion Hub**: Designated role for new tool categories
- **YADM Integration**: Manages dotfiles using YADM (Yet Another Dotfiles Manager)

## NOTES
- **13 Files**: Smaller than most roles (ready for expansion)
- **Non-Standard Repos**: Chrome repo added manually (google-chrome.yml)
- **Dependencies**: Requires `common` and `repos` roles first
- **Testing**: Verify app launches after install (no automated tests currently)
- **GenAI Tools**: Target for consolidation effort - high priority
- **Language Envs**: Consider asdf over rbenv+pyenv for unified management
- **Expansion Ready**: Minimal current footprint allows significant additions without complexity explosion
