# -*- coding: utf-8 -*-
# Copyright (c) 2023 Sagi Shnaidman <sshnaidm@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.plugins.callback import CallbackBase
from ansible.module_utils._text import to_text
import yaml
from typing import Any, Optional, List, Dict
from pathlib import Path
import os
import json
import datetime
import re

__metaclass__ = type

DOCUMENTATION = """
    name: llm_analyzer
    type: notification
    short_description: Analyzes Ansible tasks and playbooks with various AI models
    description:
      - Analyzes Ansible tasks and playbooks using different AI providers
      - Validates API keys before playbook execution
      - Prints analysis for the tasks and playbooks
      - Saves analysis to markdown files in llm_analysis directory
      - Automatically disables if API key validation fails
    requirements:
      - enable in configuration - see examples section below for details
      - install required provider libraries (openai, google.generativeai, etc.)

    options:
      provider:
        description: AI provider to use
        choices: ['openai', 'gemini', 'groq', 'openrouter', 'cohere', 'anthropic']
        default: openai
        env:
          - name: AI_PROVIDER
        ini:
          - section: callback_llm_analyzer
            key: provider
      api_key:
        description: |
          API key for the chosen provider. Can be provided directly or via environment variables:
          - For OpenAI: OPENAI_API_KEY
          - For Gemini: GEMINI_API_KEY or GOOGLE_API_KEY
          - For Groq: GROQ_API_KEY
          - For OpenRouter: OPENROUTER_API_KEY
          - For Cohere: COHERE_API_KEY
          - For Anthropic: ANTHROPIC_API_KEY
          The API key must be set either through this option or the corresponding environment variable.
        env:
          - name: OPENAI_API_KEY
          - name: GEMINI_API_KEY
          - name: GROQ_API_KEY
          - name: OPENROUTER_API_KEY
          - name: COHERE_API_KEY
          - name: ANTHROPIC_API_KEY
        ini:
          - section: callback_llm_analyzer
            key: api_key
      model:
        description: Model to use for the chosen provider
        default: gpt-4
        env:
          - name: AI_MODEL
        ini:
          - section: callback_llm_analyzer
            key: model
      temperature:
        description: Temperature for AI response
        default: 0.4
        env:
          - name: AI_TEMPERATURE
        ini:
          - section: callback_llm_analyzer
            key: temperature
      max_tokens:
        description: Maximum tokens for AI response
        env:
          - name: AI_MAX_TOKENS
        ini:
          - section: callback_llm_analyzer
            key: max_tokens

    examples: |
      # Enable the callback plugin in ansible.cfg
      [defaults]
      callbacks_enabled = llm_analyzer

      # Configure the plugin in ansible.cfg
      [callback_llm_analyzer]
      provider = openai
      api_key = sk-xxx  # Or set via OPENAI_API_KEY environment variable
      model = gpt-4
      temperature = 0.4
      max_tokens = 1000

      # Example using environment variables with Gemini
      export AI_PROVIDER=gemini
      export GEMINI_API_KEY=your-key
      export AI_MODEL=gemini-1.5-pro
      ansible-playbook playbook.yml

      # Example using Groq
      [callback_llm_analyzer]
      provider = groq
      api_key = gsk-xxx  # Or set via GROQ_API_KEY environment variable
      model = llama-3.3-70b-versatile

      # Example using Cohere
      [callback_llm_analyzer]
      provider = cohere
      api_key = xxx  # Or set via COHERE_API_KEY environment variable
      model = command-r-plus-08-2024

      # Example using OpenRouter
      [callback_llm_analyzer]
      provider = openrouter
      api_key = sk-xxx  # Or set via OPENROUTER_API_KEY environment variable
      model = anthropic/claude-3-opus
"""


# Provider-specific imports
AVAILABLE_PROVIDERS = {}
PROVIDER_CLASSES = {}

# Mapping of providers to their required packages for better error messages
PROVIDER_REQUIREMENTS = {
    "openai": "openai",
    "openrouter": "openai",
    "gemini": "google-generativeai",
    "groq": "groq",
    "cohere": "cohere",
    "anthropic": "anthropic",
}

try:
    import openai
    from openai import OpenAI

    AVAILABLE_PROVIDERS["openai"] = True
    PROVIDER_CLASSES["openai"] = {"client": OpenAI, "module": openai}
except ImportError:
    AVAILABLE_PROVIDERS["openai"] = False
    PROVIDER_CLASSES["openai"] = {"client": None, "module": None}

try:
    import google.generativeai as genai

    AVAILABLE_PROVIDERS["gemini"] = True
    PROVIDER_CLASSES["gemini"] = {"client": genai.GenerativeModel, "module": genai}
except ImportError:
    AVAILABLE_PROVIDERS["gemini"] = False
    PROVIDER_CLASSES["gemini"] = {"client": None, "module": None}

try:
    import groq

    AVAILABLE_PROVIDERS["groq"] = True
    PROVIDER_CLASSES["groq"] = {"client": groq.Groq, "module": groq}
except ImportError:
    AVAILABLE_PROVIDERS["groq"] = False
    PROVIDER_CLASSES["groq"] = {"client": None, "module": None}

try:
    import cohere

    AVAILABLE_PROVIDERS["cohere"] = True
    PROVIDER_CLASSES["cohere"] = {"client": cohere.ClientV2, "module": cohere}
except ImportError:
    AVAILABLE_PROVIDERS["cohere"] = False
    PROVIDER_CLASSES["cohere"] = {"client": None, "module": None}

try:
    import anthropic

    AVAILABLE_PROVIDERS["anthropic"] = True
    PROVIDER_CLASSES["anthropic"] = {"client": anthropic.Anthropic, "module": anthropic}
except ImportError:
    AVAILABLE_PROVIDERS["anthropic"] = False
    PROVIDER_CLASSES["anthropic"] = {"client": None, "module": None}

# OpenRouter uses OpenAI's client
AVAILABLE_PROVIDERS["openrouter"] = AVAILABLE_PROVIDERS["openai"]
PROVIDER_CLASSES["openrouter"] = PROVIDER_CLASSES["openai"]


class AIProvider:
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        self.api_callers = {}  # Initialize api_callers here
        self._setup_client()

    def validate_api_key(self) -> bool:
        """Validate the API key for the chosen provider."""
        if not self.api_key:
            print(f"No API key provided for {self.provider}")
            return False

        if not AVAILABLE_PROVIDERS.get(self.provider):
            required_package = PROVIDER_REQUIREMENTS.get(self.provider, "unknown")
            print(
                f"Provider {self.provider} is not available. Please install required library: pip install {required_package}"
            )
            return False

        # Check if provider classes are available
        provider_classes = PROVIDER_CLASSES.get(self.provider, {})
        client_class = provider_classes.get("client")
        provider_module = provider_classes.get("module")

        if not client_class or not provider_module:
            required_package = PROVIDER_REQUIREMENTS.get(self.provider, "unknown")
            print(
                f"Provider {self.provider} classes are not available. Please install the required library: pip install {required_package}"
            )
            return False

        try:
            if self.provider in ["openai", "openrouter"]:
                # Test API key with a minimal request
                if self.provider == "openrouter":
                    client = client_class(base_url="https://openrouter.ai/api/v1")
                else:
                    client = client_class()
                client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5,
                )
            elif self.provider == "gemini":
                provider_module.configure(api_key=self.api_key)
                model = client_class(self.model)
                model.generate_content("test")
            elif self.provider == "groq":
                client = client_class(api_key=self.api_key)
                client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5,
                )
            elif self.provider == "cohere":
                client = client_class(api_key=self.api_key)
                client.generate(prompt="test", model=self.model, max_tokens=5)
            elif self.provider == "anthropic":
                client = client_class(api_key=self.api_key)
                client.messages.create(
                    model=self.model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "test"}],
                )
            return True
        except Exception as e:
            print(f"API key validation failed for {self.provider}: {str(e)}")
            return False

    def _setup_client(self):
        if not self.api_key:
            raise ValueError(f"API key not provided for {self.provider}")

        # Check if provider classes are available
        provider_classes = PROVIDER_CLASSES.get(self.provider, {})
        client_class = provider_classes.get("client")
        provider_module = provider_classes.get("module")

        if not client_class or not provider_module:
            required_package = PROVIDER_REQUIREMENTS.get(self.provider, "unknown")
            raise ValueError(
                f"Provider {self.provider} is not available. Please install the required library: pip install {required_package}"
            )

        if self.provider in ["openai", "openrouter"]:
            os.environ["OPENAI_API_KEY"] = self.api_key
            if self.provider == "openrouter":
                self.client = client_class(base_url="https://openrouter.ai/api/v1")
            elif self.provider == "openai":
                self.client = client_class()
            self.api_callers["openai"] = self._call_openai_api
            self.api_callers["openrouter"] = self._call_openai_api
        elif self.provider == "gemini":
            os.environ["GOOGLE_API_KEY"] = self.api_key
            provider_module.configure(api_key=self.api_key)
            self.client = client_class(self.model)
            self.api_callers["gemini"] = self._call_gemini_api
        elif self.provider == "groq":
            os.environ["GROQ_API_KEY"] = self.api_key
            self.client = client_class(api_key=self.api_key)
            self.api_callers["groq"] = self._call_groq_api
        elif self.provider == "cohere":
            os.environ["COHERE_API_KEY"] = self.api_key
            self.client = client_class(api_key=self.api_key)
            self.api_callers["cohere"] = self._call_cohere_api
        elif self.provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
            self.client = client_class(api_key=self.api_key)
            self.api_callers["anthropic"] = self._call_anthropic_api

    def _create_prompt(
        self, task_text: Optional[str] = None, play_text: Optional[str] = None
    ) -> str:
        prompt_template_str = None
        prompt_name = None
        context_text = None

        if task_text:
            prompt_name = "ansible_task_prompt"
            context_text = task_text
        elif play_text:
            prompt_name = "ansible_play_prompt"
            context_text = play_text
        else:
            return ""  # No context, no prompt

        # If Langfuse fetching failed or was skipped, use local generation
        if prompt_template_str is None:
            if task_text:
                # Analysis-focused prompt for tasks
                prompt_template_str = (
                    "Review the following Ansible task code:\n"
                    "\n```yaml\n{{task_text}}\n```\n"
                    "Provide a technical analysis of this task. Focus on understanding and explaining:\n"
                    "- What this task accomplishes and its role in the playbook\n"
                    "- The Ansible modules and parameters being used\n"
                    "- How idempotency is handled in this implementation\n"
                    "- The error handling and conditional logic present\n"
                    "- The technical approach and methodology used\n\n"
                    "IMPORTANT: Provide only factual analysis and explanation of what the code does. "
                    "Do NOT provide recommendations, suggestions, improvements, or advice on how to change the code. "
                    "Focus purely on understanding and documenting the current implementation."
                )
            elif play_text:
                # Analysis-focused prompt for playbooks
                prompt_template_str = (
                    "Review the following Ansible playbook code:\n"
                    "\n```yaml\n{{play_text}}\n```\n"
                    "Provide a technical analysis of this playbook. Focus on understanding and explaining:\n"
                    "- The overall purpose and scope of this playbook\n"
                    "- The play structure, hosts targeting, and execution flow\n"
                    "- Variable definitions, role assignments, and task organization\n"
                    "- Error handling mechanisms and conditional logic in use\n"
                    "- The technical architecture and design patterns employed\n\n"
                    "IMPORTANT: Provide only factual analysis and explanation of what the code does. "
                    "Do NOT provide recommendations, suggestions, improvements, or advice on how to change the code. "
                    "Focus purely on understanding and documenting the current implementation."
                )
            else:
                return ""

        # Substitute the context into the prompt string
        final_prompt = prompt_template_str
        if task_text and "{{task_text}}" in final_prompt:
            final_prompt = final_prompt.replace("{{task_text}}", task_text)
        elif play_text and "{{play_text}}" in final_prompt:
            final_prompt = final_prompt.replace("{{play_text}}", play_text)

        return final_prompt

    def _call_openai_api(self, prompt):
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant and Ansible expert.",
                },
                {"role": "user", "content": prompt},
            ],
        }
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        # Add OpenRouter specific headers if using OpenRouter
        if self.provider == "openrouter":
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://github.com/ansible/ansible",  # Identifies your application
                "X-Title": "Ansible LLM Analyzer",  # Name of your application
            }

        response = self.client.chat.completions.create(**kwargs)
        return to_text(response.choices[0].message.content.strip())

    def _call_gemini_api(self, prompt):
        response = self.client.generate_content(prompt)
        return to_text(response.text.strip())

    def _call_groq_api(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant and Ansible expert.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature if self.temperature is not None else 0.4,
            max_tokens=self.max_tokens if self.max_tokens else None,
        )
        return to_text(completion.choices[0].message.content.strip())

    def _call_cohere_api(self, prompt):
        response = self.client.generate(
            prompt=prompt,
            model=self.model,
            temperature=self.temperature if self.temperature is not None else 0.4,
            max_tokens=self.max_tokens if self.max_tokens else None,
        )
        return to_text(response.generations[0].text.strip())

    def _call_anthropic_api(self, prompt):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens if self.max_tokens else 1024,
            temperature=self.temperature if self.temperature is not None else 0.4,
            system="You are a helpful assistant and Ansible expert.",
            messages=[{"role": "user", "content": prompt}],
        )
        return to_text(message.content[0].text.strip())

    def get_description(
        self, task_text: Optional[str] = None, play_text: Optional[str] = None
    ) -> str:
        if not AVAILABLE_PROVIDERS.get(self.provider):
            return to_text(f"Please install the required library for {self.provider}")

        if not self.api_key:
            return to_text(f"Please set the API key for {self.provider}")

        prompt = self._create_prompt(task_text, play_text)

        try:
            api_caller = self.api_callers.get(self.provider)
            if api_caller:
                return api_caller(prompt)
            else:
                return to_text("Unsupported provider")

        except Exception as e:
            return to_text(f"Error with {self.provider}: {str(e)}")


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 1.1
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "llm_analyzer"
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.ai_provider = None
        self.analysis_dir = Path("llm_analysis")
        self.analysis_dir.mkdir(exist_ok=True)
        self.task_count = 0
        self.play_count = 0

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(
            task_keys=task_keys, var_options=var_options, direct=direct
        )

        provider = self.get_option("provider")
        # Try to get provider-specific API key from environment first
        api_key = os.getenv(f"{provider.upper()}_API_KEY")

        # If not found in environment, try the generic api_key from ansible.cfg
        if not api_key:
            api_key = self.get_option("api_key")

        # Now, initialize and validate AI provider
        try:
            self.ai_provider = AIProvider(
                provider=provider,
                api_key=api_key,
                model=self.get_option("model"),
                temperature=float(self.get_option("temperature")),
                max_tokens=self.get_option("max_tokens"),
            )
            # Validate AI provider API key only if instantiation was successful
            if not self.ai_provider.validate_api_key():
                self.disabled = True  # Disables LLM-based analysis if key is bad
                print(
                    f"\nLLM Analyzer disabled: Invalid API key for {provider}. LLM analysis will be skipped."
                )
        except Exception as e:
            self.disabled = True  # Disables LLM-based analysis if provider init fails
            print(
                f"\nLLM Analyzer disabled: Failed to initialize AI provider '{provider}': {str(e)}. LLM analysis will be skipped."
            )
            # No return here, the plugin object itself is still valid, just analysis is disabled.

    def _save_to_markdown(self, content: str, analysis_type: str, name: str = None):
        """Save analysis to a markdown file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        count = self.task_count if analysis_type == "task" else self.play_count
        filename = f"{timestamp}_{analysis_type}_{count}"
        if name:
            # Replace spaces and special characters with underscores
            safe_name = "".join(c if c.isalnum() else "_" for c in name)
            filename = f"{filename}_{safe_name}"
        filename = f"{filename}.md"

        filepath = self.analysis_dir / filename
        with open(filepath, "w") as f:
            f.write(f"# {analysis_type.title()} Analysis\n\n")
            if name:
                f.write(f"**Name:** {name}\n\n")
            f.write(
                f"**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## Analysis\n\n")
            f.write(content)

    def _save_structured_suggestions(self, suggestions: str, analysis_type: str, name: str = None):
        """Save structured suggestions for LLM processing."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        count = self.task_count if analysis_type == "task" else self.play_count
        filename = f"{timestamp}_{analysis_type}_{count}"
        if name:
            safe_name = "".join(c if c.isalnum() else "_" for c in name)
            filename = f"{filename}_{safe_name}"
        filename = f"{filename}_suggestions.dspy"

        filepath = self.analysis_dir / filename
        with open(filepath, "w") as f:
            f.write(suggestions)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.task_count += 1

        # Safely get task data using public API with error handling
        try:
            # Use public get_ds() method instead of private _ds attribute
            task_data = task.get_ds()
            task_text = yaml.dump([json.loads(json.dumps(task_data))])
        except (AttributeError, TypeError) as e:
            # Fallback: create task representation from available public attributes
            print(f"Warning: Could not access task data structure: {e}")
            task_dict = {
                'name': str(getattr(task, 'name', 'Unknown Task')),
                'action': str(getattr(task, 'action', 'Unknown Action')),
            }
            # Add args if available and serializable
            try:
                if hasattr(task, 'args') and task.args:
                    # Only add args if they're serializable (not mock objects)
                    args_data = dict(task.args) if hasattr(task.args, 'items') else task.args
                    # Test if serializable
                    json.dumps(args_data)
                    task_dict.update(args_data)
            except (TypeError, ValueError, AttributeError):
                # Args not serializable, skip them
                task_dict['args'] = 'Unable to serialize task arguments'

            task_text = yaml.dump([task_dict])

        # Perform AI-powered explanation
        explanation = self.ai_provider.get_description(task_text=task_text)

        # Perform style analysis
        style_violations = self.analyze_style(task_text)

        # Print AI explanation to console
        print(f"Explanation: \n{explanation}")

        # Print style analysis if violations found
        if style_violations:
            print(f"\n⚠️  Style Guide Violations Found:")
            for violation in style_violations:
                print(f"  • Line {violation['line']}: {violation['message']}")

        # Save full analysis to markdown (includes both AI explanation and style analysis)
        full_analysis = explanation
        if style_violations:
            full_analysis += "\n\n## Style Analysis\n\n"
            for violation in style_violations:
                full_analysis += f"- **Line {violation['line']}** ({violation['type']}): {violation['message']}\n"

            # Also save structured suggestions for LLM processing
            structured_suggestions = self.generate_structured_suggestions(
                task_text, f"task_{self.task_count}_{task.get_name()}.yml"
            )
            self._save_structured_suggestions(structured_suggestions, "task", task.get_name())

        self._save_to_markdown(full_analysis, "task", task.get_name())

    def v2_playbook_on_play_start(self, play):
        self.play_count += 1

        # Safely get play data using public API with error handling
        try:
            # Use public get_ds() method
            play_data = play.get_ds()
            play_text = yaml.dump(json.loads(json.dumps(play_data)))
        except (AttributeError, TypeError) as e:
            # Fallback: create play representation from available public attributes
            print(f"Warning: Could not access play data structure: {e}")
            play_dict = {
                'name': str(getattr(play, 'name', 'Unknown Play')),
                'hosts': list(getattr(play, 'hosts', [])) if hasattr(getattr(play, 'hosts', []), '__iter__') else ['Unknown'],
                'gather_facts': bool(getattr(play, 'gather_facts', True)),
            }
            play_text = yaml.dump(play_dict)

        # Perform AI-powered explanation
        explanation = self.ai_provider.get_description(play_text=play_text)

        # Perform style analysis
        style_violations = self.analyze_style(play_text)

        # Print AI explanation to console
        print(f"Explanation: \n{explanation}")

        # Print style analysis if violations found
        if style_violations:
            print(f"\n⚠️  Style Guide Violations Found:")
            for violation in style_violations:
                print(f"  • Line {violation['line']}: {violation['message']}")

        # Save full analysis to markdown (includes both AI explanation and style analysis)
        full_analysis = explanation
        if style_violations:
            full_analysis += "\n\n## Style Analysis\n\n"
            for violation in style_violations:
                full_analysis += f"- **Line {violation['line']}** ({violation['type']}): {violation['message']}\n"

        self._save_to_markdown(full_analysis, "play", play.get_name())

    def analyze_style(self, yaml_content: str) -> List[Dict[str, Any]]:
        """Analyze YAML content for Ansible style guide violations.

        Args:
            yaml_content: The YAML content to analyze

        Returns:
            List of violation dictionaries with type, message, and line info
        """
        violations = []
        lines = yaml_content.split('\n')

        violations.extend(self._check_variable_naming(lines))
        violations.extend(self._check_task_structure(lines))
        violations.extend(self._check_tag_conventions(lines))

        return violations

    def generate_structured_suggestions(self, yaml_content: str, file_path: str = "ansible_file.yml") -> str:
        """Generate structured suggestions for LLM processing in DSPy format.

        Args:
            yaml_content: The YAML content to analyze
            file_path: Path to the file being analyzed

        Returns:
            Structured output with DSPy field markers and JSON suggestions
        """
        violations = self.analyze_style(yaml_content)
        suggestions = []

        for violation in violations:
            suggestion = self._violation_to_suggestion(violation, yaml_content)
            if suggestion:
                suggestions.append(suggestion)

        # Format in DSPy structured output format
        output_parts = [
            "[[ ## file_path ## ]]",
            file_path,
            "",
            "[[ ## suggestions ## ]]",
            json.dumps(suggestions, indent=2),
            "",
            "[[ ## completed ## ]]"
        ]

        return "\n".join(output_parts)

    def _violation_to_suggestion(self, violation: Dict[str, Any], yaml_content: str) -> Optional[Dict[str, Any]]:
        """Convert a style violation to an actionable suggestion."""
        lines = yaml_content.split('\n')
        if violation['line'] <= 0 or violation['line'] > len(lines):
            return None

        line_content = lines[violation['line'] - 1]

        suggestion = {
            "type": "replace",
            "line_number": violation['line'],
            "violation_type": violation['type'],
            "reason": violation['message']
        }

        # Generate specific fixes based on violation type
        if violation['type'] == 'variable_naming':
            suggestion.update(self._generate_variable_naming_fix(line_content, violation))
        elif violation['type'] == 'tag_naming':
            suggestion.update(self._generate_tag_naming_fix(line_content, violation))
        elif violation['type'] == 'task_structure':
            suggestion.update(self._generate_task_structure_fix(line_content, violation))

        return suggestion

    def _generate_variable_naming_fix(self, line_content: str, violation: Dict[str, Any]) -> Dict[str, str]:
        """Generate fix for variable naming violations."""
        old_text = line_content.strip()
        new_text = old_text

        # Fix camelCase variables in Jinja templates
        if 'snake_case' in violation['message']:
            import re
            camel_pattern = r'{{\s*([a-z][a-zA-Z]*[A-Z][a-zA-Z]*)\s*}}'
            match = re.search(camel_pattern, old_text)
            if match:
                camel_var = match.group(1)
                snake_var = self._to_snake_case(camel_var)
                new_text = old_text.replace(f"{{{{ {camel_var} }}}}", f"{{{{ {snake_var} }}}}")

        # Fix variables in vars sections
        elif 'role prefix' in violation['message']:
            var_pattern = r'^(\s*)([A-Z][a-zA-Z]*)\s*:'
            match = re.match(var_pattern, old_text)
            if match:
                indent, var_name = match.groups()
                snake_var = self._to_snake_case(var_name)
                new_text = f"{indent}role_{snake_var}:"

        return {
            "old_text": old_text,
            "new_text": new_text
        }

    def _generate_tag_naming_fix(self, line_content: str, violation: Dict[str, Any]) -> Dict[str, str]:
        """Generate fix for tag naming violations."""
        old_text = line_content.strip()
        new_text = old_text

        # Fix single string/unquoted tags to array format
        if 'array format' in violation['message']:
            if 'tags:' in old_text:
                # Extract tag value
                tag_match = re.search(r'tags:\s*([^\s#]+)', old_text)
                if tag_match:
                    tag_value = tag_match.group(1).strip('"\'')
                    # Convert to snake_case if needed
                    if re.match(r'[A-Z][a-zA-Z]*[A-Z][a-zA-Z]*', tag_value):
                        tag_value = self._to_snake_case(tag_value)
                    new_text = re.sub(r'tags:\s*[^\s#]+', f'tags: ["{tag_value}"]', old_text)

        # Fix camelCase tags in arrays
        elif 'snake_case' in violation['message']:
            camel_tags = re.findall(r'([A-Z][a-zA-Z]*[A-Z][a-zA-Z]*)', old_text)
            for camel_tag in camel_tags:
                snake_tag = self._to_snake_case(camel_tag)
                new_text = new_text.replace(camel_tag, f'"{snake_tag}"')

        return {
            "old_text": old_text,
            "new_text": new_text
        }

    def _generate_task_structure_fix(self, line_content: str, violation: Dict[str, Any]) -> Dict[str, str]:
        """Generate fix for task structure violations."""
        return {
            "old_text": line_content.strip(),
            "new_text": "# TODO: Reorder task attributes - name, module, become, loop, when, tags, notify",
            "note": "Task attribute reordering requires multi-line changes. Manual intervention recommended."
        }

    def _check_variable_naming(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Check for variable naming convention violations."""
        violations = []

        # Pattern for camelCase variables in Jinja templates
        camel_case_pattern = r'{{\s*([a-z][a-zA-Z]*[A-Z][a-zA-Z]*)\s*}}'

        # Pattern for variables in vars sections that start with capital letters
        vars_pattern = r'^\s*([A-Z][a-zA-Z]*)\s*:'

        for line_num, line in enumerate(lines, 1):
            # Check for camelCase in Jinja templates
            camel_matches = re.findall(camel_case_pattern, line)
            for match in camel_matches:
                violations.append({
                    'type': 'variable_naming',
                    'message': f'Variable "{match}" should use snake_case: "{self._to_snake_case(match)}"',
                    'line': line_num
                })

            # Check for variables starting with capital letters
            vars_match = re.match(vars_pattern, line)
            if vars_match:
                var_name = vars_match.group(1)
                violations.append({
                    'type': 'variable_naming',
                    'message': f'Variable "{var_name}" should use snake_case with role prefix',
                    'line': line_num
                })

        return violations

    def _check_task_structure(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Check for task structure violations according to style guide.

        Expected order: name, module, become, loop, when, tags, notify
        """
        violations = []
        in_task = False
        task_start_line = 0
        task_attributes = []

        for line_num, line in enumerate(lines, 1):
            # Detect start of a task (starts with "- ")
            if re.match(r'^\s*-\s+\w+:', line):
                if in_task and task_attributes:
                    # Check previous task structure
                    violations.extend(self._validate_task_attribute_order(task_attributes, task_start_line))

                in_task = True
                task_start_line = line_num
                task_attributes = []

                # Extract first attribute
                match = re.match(r'^\s*-\s+(\w+):', line)
                if match:
                    task_attributes.append(match.group(1))

            # Collect other task attributes
            elif in_task and re.match(r'^\s+(\w+):', line):
                match = re.match(r'^\s+(\w+):', line)
                if match:
                    attr = match.group(1)
                    # Skip ansible module attributes (they're not task-level attributes)
                    if not line.strip().startswith('ansible.builtin.'):
                        task_attributes.append(attr)

            # End of task detection (empty line or new task/block)
            elif in_task and (line.strip() == '' or re.match(r'^\s*-|^\w+:', line)):
                if task_attributes:
                    violations.extend(self._validate_task_attribute_order(task_attributes, task_start_line))
                in_task = False
                task_attributes = []

        # Check last task if file ends while in task
        if in_task and task_attributes:
            violations.extend(self._validate_task_attribute_order(task_attributes, task_start_line))

        return violations

    def _validate_task_attribute_order(self, attributes: List[str], start_line: int) -> List[Dict[str, Any]]:
        """Validate the order of task attributes against the style guide."""
        violations = []
        expected_order = ['name', 'become', 'loop', 'when', 'tags', 'notify']

        # Filter attributes to only those in expected order
        relevant_attrs = [attr for attr in attributes if attr in expected_order]

        if len(relevant_attrs) > 1:
            # Check if they're in the expected order
            sorted_attrs = sorted(relevant_attrs, key=lambda x: expected_order.index(x))
            if relevant_attrs != sorted_attrs:
                violations.append({
                    'type': 'task_structure',
                    'message': 'Task attributes not in recommended order. Should be: name, module, become, loop, when, tags, notify',
                    'line': start_line
                })

        return violations

    def _check_tag_conventions(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Check for tag naming convention violations."""
        violations = []

        for line_num, line in enumerate(lines, 1):
            # Check for string format tags (should be array)
            if re.search(r'tags:\s*"[^"]*"', line):
                violations.append({
                    'type': 'tag_naming',
                    'message': 'Tags should use square bracket array format',
                    'line': line_num
                })

            # Check for single unquoted tags (should be array)
            single_tag_match = re.search(r'tags:\s*([A-Za-z][A-Za-z0-9_]*)\s*(?:#|$)', line)
            if single_tag_match:
                tag_name = single_tag_match.group(1)
                violations.append({
                    'type': 'tag_naming',
                    'message': f'Tags should use square bracket array format',
                    'line': line_num
                })
                # Also check if the tag is camelCase
                if re.match(r'[A-Z][a-zA-Z]*[A-Z][a-zA-Z]*', tag_name):
                    violations.append({
                        'type': 'tag_naming',
                        'message': f'Tag "{tag_name}" should use snake_case',
                        'line': line_num
                    })

            # Check for camelCase tags in arrays
            tag_array_match = re.search(r'tags:\s*\[(.*)\]', line)
            if tag_array_match:
                tags_content = tag_array_match.group(1)
                # Find unquoted camelCase tags
                camel_tags = re.findall(r'([A-Z][a-zA-Z]*[A-Z][a-zA-Z]*)', tags_content)
                for tag in camel_tags:
                    violations.append({
                        'type': 'tag_naming',
                        'message': f'Tag "{tag}" should use snake_case',
                        'line': line_num
                    })

        return violations

    def _to_snake_case(self, camel_str: str) -> str:
        """Convert camelCase to snake_case.

        Args:
            camel_str: String in camelCase format

        Returns:
            String in snake_case format
        """
        # Insert underscore before capital letters that follow lowercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        # Insert underscore before capital letters that follow lowercase letters or digits
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
