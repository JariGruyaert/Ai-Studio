# Agents

Agent development hub for building autonomous AI systems with Claude.

## Overview

Agents are autonomous systems that can:
- Execute multi-step workflows
- Use tools and skills
- Make decisions based on context
- Handle complex tasks end-to-end

## Architecture

```
agents/
├── configs/      # Agent configuration files (behavior, tools, constraints)
├── skills/       # Custom skills agents can use (see skills/README.md)
└── workflows/    # Multi-step workflow definitions
```

## Agent Components

### 1. Configs (What the agent is)
Define the agent's identity, capabilities, and constraints.

```yaml
# configs/code-reviewer.yaml
name: code-reviewer
description: Expert code reviewer for security and performance

system_prompt: |
  You are a code review specialist focusing on:
  - Security vulnerabilities
  - Performance optimization
  - Best practices

tools:
  - file_reader
  - code_analyzer
  - security_scanner

skills:
  - syntax_validation
  - dependency_check
  - test_coverage_analysis

constraints:
  max_file_size: 10000
  timeout: 300
  output_format: json
```

### 2. Skills (What the agent can do)
Reusable capabilities that agents can leverage. See [skills/README.md](./skills/README.md)

### 3. Workflows (How the agent works)
Multi-step processes the agent follows.

```yaml
# workflows/document-processor.yaml
name: document-processor
steps:
  - name: extract
    skill: text_extraction
    input: source_file

  - name: structure
    skill: data_structuring
    input: extract.output

  - name: validate
    skill: schema_validation
    input: structure.output

  - name: store
    skill: knowledge_ingestion
    input: validate.output
```

## Agent Patterns

### Simple Task Agent
Single-purpose agent for specific tasks.

```python
# Example: Summary Agent
{
  "name": "summarizer",
  "task": "Summarize documents",
  "skills": ["text_extraction", "summarization"],
  "output": "markdown"
}
```

### Pipeline Agent
Processes data through multiple stages.

```python
# Example: Data Pipeline Agent
{
  "name": "data-pipeline",
  "workflow": [
    "extract → transform → validate → load"
  ],
  "error_handling": "retry_with_backoff"
}
```

### Research Agent
Gathers and synthesizes information.

```python
# Example: Research Agent
{
  "name": "researcher",
  "capabilities": [
    "web_search",
    "document_analysis",
    "citation_extraction",
    "synthesis"
  ],
  "output_format": "structured_report"
}
```

## Building Your First Agent

### Step 1: Define the Config
```yaml
# configs/my-first-agent.yaml
name: my-first-agent
purpose: Process text documents and extract key information

system_prompt: |
  You are a document processing agent.
  Extract key information and structure it clearly.

skills:
  - text_extraction
  - entity_recognition
  - summarization
```

### Step 2: Create Required Skills
See [skills/README.md](./skills/README.md) for creating custom skills.

### Step 3: Define Workflow (if multi-step)
```yaml
# workflows/my-first-workflow.yaml
name: document-analysis
agent: my-first-agent

steps:
  - extract_text
  - identify_entities
  - generate_summary
  - format_output
```

### Step 4: Test and Iterate
- Start with simple tasks
- Add complexity gradually
- Document what works in `../knowledge/patterns/`

## Agent Design Principles

### 1. Single Responsibility
Each agent should have a clear, focused purpose.

❌ "General purpose AI helper"
✅ "Code review agent for Python security"

### 2. Composability
Agents should work together via standard interfaces.

```
Agent A output → Agent B input → Agent C input
```

### 3. Error Handling
Define how agents handle failures:
- Retry strategies
- Fallback behaviors
- Error reporting

### 4. Observability
Track agent behavior:
- Input/output logging
- Decision points
- Performance metrics

## Multi-Agent Workflows

### Sequential
```
Agent 1 → Agent 2 → Agent 3 → Result
```

### Parallel
```
        → Agent 1 →
Input                  → Merge → Result
        → Agent 2 →
```

### Hierarchical
```
Orchestrator Agent
    ├── Specialist Agent 1
    ├── Specialist Agent 2
    └── Specialist Agent 3
```

## Configuration Best Practices

### Environment-Specific Configs
```yaml
# configs/agent.dev.yaml
debug: true
verbose_logging: true

# configs/agent.prod.yaml
debug: false
performance_monitoring: true
```

### Secret Management
Never hardcode secrets in configs. Use environment variables:

```yaml
api_keys:
  anthropic: ${ANTHROPIC_API_KEY}
  openai: ${OPENAI_API_KEY}
```

Store actual values in `../config/settings/.env`

## Testing Agents

### Unit Test Individual Skills
Test each skill independently before integration.

### Integration Test Workflows
Test complete workflows end-to-end.

### Validation Checklist
- [ ] Handles expected inputs correctly
- [ ] Gracefully handles errors
- [ ] Respects rate limits and timeouts
- [ ] Produces consistent output format
- [ ] Logs sufficient information for debugging

## Common Patterns

### Retry with Backoff
```python
max_retries: 3
backoff_factor: 2  # 2s, 4s, 8s
```

### Conditional Branching
```yaml
- if: validation_failed
  then: manual_review
  else: auto_approve
```

### Parallel Processing
```yaml
parallel:
  - skill: process_chunk_1
  - skill: process_chunk_2
  - skill: process_chunk_3
merge: combine_results
```

## Agent State Management

### Stateless Agents
Each invocation is independent. Good for:
- Simple transformations
- Idempotent operations

### Stateful Agents
Maintain context across invocations. Good for:
- Conversations
- Multi-session workflows
- Learning from feedback

## Monitoring and Debugging

### Key Metrics
- Task completion rate
- Average execution time
- Error frequency
- Resource usage

### Debug Logging
```yaml
logging:
  level: debug
  include:
    - inputs
    - outputs
    - decision_points
    - errors
```

## Examples

### Document Processor Agent
```yaml
name: doc-processor
skills: [extract, structure, validate]
workflow: extract → structure → validate → store
error_handling: retry_failed_steps
```

### Code Analysis Agent
```yaml
name: code-analyzer
skills: [parse, analyze, report]
tools: [ast_parser, linter, security_scanner]
output: detailed_report.json
```

### Knowledge Graph Builder
```yaml
name: kg-builder
skills: [entity_extraction, relationship_mapping, graph_construction]
workflow: parallel_extraction → relationship_discovery → graph_assembly
```

## Next Steps

1. Read [skills/README.md](./skills/README.md) to understand skill development
2. Create your first agent config in `configs/`
3. Build supporting skills in `skills/`
4. Define workflows in `workflows/`
5. Document patterns in `../knowledge/patterns/`

## References

- [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Building Agents with Claude](https://docs.anthropic.com/claude/docs/agents)
- [Tool Use Guide](https://docs.anthropic.com/claude/docs/tool-use)
