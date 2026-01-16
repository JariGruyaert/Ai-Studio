# Template: Code Review

## Purpose
Review code for security, performance, and best practices

## Variables
- `{{CODE}}`: The code to review
- `{{LANGUAGE}}`: Programming language (optional)
- `{{FOCUS}}`: Specific areas to focus on (optional)

## Prompt

```xml
<task>
Review the following {{LANGUAGE}} code for:
- Security vulnerabilities (OWASP Top 10)
- Performance issues
- Best practices
- Potential bugs
{{#if FOCUS}}
- {{FOCUS}}
{{/if}}
</task>

<code>
{{CODE}}
</code>

<requirements>
1. Identify issues by severity (critical, high, medium, low)
2. Explain WHY each issue matters
3. Provide specific code examples for fixes
4. Suggest alternative approaches where applicable
</requirements>

<output_format>
For each issue found:
- Severity: [critical|high|medium|low]
- Issue: [description]
- Location: [line numbers or function names]
- Why it matters: [explanation]
- Suggested fix: [code example]
</output_format>
```

## Example Usage

### Input
```
CODE:
def process_user_input(data):
    return eval(data)

LANGUAGE: Python
FOCUS: Input validation
```

### Expected Output
```
Severity: critical
Issue: Arbitrary code execution vulnerability
Location: line 2
Why it matters: eval() executes arbitrary Python code, allowing attackers to run malicious commands
Suggested fix:
```python
import json

def process_user_input(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input")
```
```

## Notes
- This template works well for most programming languages
- Adjust the focus areas based on your needs
- Can be used with Claude Code or API directly
