# Ansible Callback LLM Analyzer

> 31 nodes · cohesion 0.10

## Key Concepts

- **CallbackModule** (19 connections) — `plugins/callback/llm_analyzer.py`
- **.analyze_style()** (8 connections) — `plugins/callback/llm_analyzer.py`
- **.v2_playbook_on_task_start()** (6 connections) — `plugins/callback/llm_analyzer.py`
- **._violation_to_suggestion()** (6 connections) — `plugins/callback/llm_analyzer.py`
- **.generate_structured_suggestions()** (5 connections) — `plugins/callback/llm_analyzer.py`
- **._to_snake_case()** (5 connections) — `plugins/callback/llm_analyzer.py`
- **._check_task_structure()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **._check_variable_naming()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **._generate_tag_naming_fix()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **._generate_variable_naming_fix()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **._save_to_markdown()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **.v2_playbook_on_play_start()** (4 connections) — `plugins/callback/llm_analyzer.py`
- **._check_tag_conventions()** (3 connections) — `plugins/callback/llm_analyzer.py`
- **._generate_task_structure_fix()** (3 connections) — `plugins/callback/llm_analyzer.py`
- **._save_structured_suggestions()** (3 connections) — `plugins/callback/llm_analyzer.py`
- **._validate_task_attribute_order()** (3 connections) — `plugins/callback/llm_analyzer.py`
- **.__init__()** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Save analysis to a markdown file.** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Save structured suggestions for LLM processing.** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Analyze YAML content for Ansible style guide violations.          Args:** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Generate structured suggestions for LLM processing in DSPy format.          Args** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Convert a style violation to an actionable suggestion.** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Generate fix for variable naming violations.** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Generate fix for tag naming violations.** (1 connections) — `plugins/callback/llm_analyzer.py`
- **Generate fix for task structure violations.** (1 connections) — `plugins/callback/llm_analyzer.py`
- *... and 6 more nodes in this community*

## Relationships

- [[AI Provider Integrations]] (4 shared connections)

## Source Files

- `plugins/callback/llm_analyzer.py`

## Audit Trail

- EXTRACTED: 100 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*