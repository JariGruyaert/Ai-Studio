# AI Studio

A personal AI infrastructure for building with Claude, focused on prompt engineering, context engineering, agents, and skills.

## Philosophy

This infrastructure is designed to be:
- **Foundational** - Start simple, iterate continuously
- **Practical** - Focus on real implementations over theory
- **Knowledge-driven** - Learn by doing, document what works
- **Composable** - Build reusable components that combine

## Architecture Overview

```
Ai-Studio/
├── prompts/          # Prompt engineering workspace
├── agents/           # Agent development & orchestration
├── knowledge/        # Documentation & learnings (your second brain)
├── pipelines/        # Data extraction & knowledge creation
├── automation/       # Scripts, Raycast presets, terminal commands
└── config/           # Settings & configurations
```

## Quick Start

1. **Explore prompts/** - Start with prompt templates and system prompts
2. **Build agents/** - Create agents using configs, skills, and workflows
3. **Document in knowledge/** - Capture learnings from Claude docs
4. **Automate with automation/** - Use Raycast and terminal for daily workflows
5. **Create pipelines/** - Build text extraction → knowledge creation flows

## Directory Guide

### 📝 [prompts/](./prompts/README.md)
Your prompt engineering workspace. Contains system prompts, task-specific prompts, and reusable templates.

### 🤖 [agents/](./agents/README.md)
Agent development hub. Build custom agents with configurations, skills, and multi-step workflows.

### 📚 [knowledge/](./knowledge/README.md)
Your second brain. Document learnings from Claude docs, best practices, and reusable patterns.

### 🔄 [pipelines/](./pipelines/README.md)
Data pipelines for text extraction and knowledge creation. From raw sources to structured knowledge.

### ⚡ [automation/](./automation/README.md)
Daily workflow tools: Python/Bash scripts, Raycast AI presets, and terminal commands.

### ⚙️ [config/](./config/README.md)
Configuration management, environment settings, and security.

## Core Concepts

### Prompts → Agents → Skills → Workflows
- **Prompts** are your interface to Claude
- **Agents** orchestrate complex tasks
- **Skills** are reusable capabilities
- **Workflows** combine multiple steps

### Knowledge Extraction Pipeline
```
Sources → Extraction → Processing → Ingestion → Knowledge Base
```

## Getting Started

1. Read [prompts/README.md](./prompts/README.md) for prompt engineering basics
2. Explore [agents/skills/README.md](./agents/skills/README.md) for building custom skills
3. Set up your first pipeline in [pipelines/](./pipelines/README.md)
4. Automate common tasks with [automation/](./automation/README.md)

## References

- [Claude Documentation](https://docs.anthropic.com/claude/docs)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Agent SDK](https://github.com/anthropics/anthropic-sdk-python)

## Iteration Philosophy

Start with what you need today, expand as you discover new requirements. Each directory can grow organically based on your actual usage patterns.
