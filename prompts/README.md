# Prompts

Your prompt engineering workspace for building effective interactions with Claude.

## Overview

This directory contains three types of prompts:
- **system/** - System prompts that set Claude's behavior and context
- **tasks/** - Task-specific prompts for common operations
- **templates/** - Reusable prompt templates with variables

## Directory Structure

```
prompts/
├── system/       # System prompts (roles, behaviors, constraints)
├── tasks/        # Task-specific prompts (code review, summarization, etc.)
└── templates/    # Reusable templates with placeholders
```

## Prompt Engineering Principles

### 1. Be Clear and Direct
```markdown
❌ "Can you help with this code?"
✅ "Review this Python function for security vulnerabilities, focusing on input validation."
```

### 2. Provide Context
```markdown
❌ "Fix this bug"
✅ "This authentication function is returning 401 for valid users. Expected behavior: return 200 with JWT token."
```

### 3. Use XML Tags for Structure
```xml
<task>
  Review the following code for performance issues
</task>

<code>
def process_items(items):
    result = []
    for item in items:
        result.append(expensive_operation(item))
    return result
</code>

<focus>
- Look for unnecessary loops
- Check for potential caching opportunities
- Suggest batch processing where applicable
</focus>
```

### 4. Few-Shot Examples When Needed
```markdown
Convert the following data to JSON format.

Example:
Input: Name: John, Age: 30, City: NYC
Output: {"name": "John", "age": 30, "city": "NYC"}

Now convert:
Input: Name: Sarah, Age: 25, City: LA
```

## System Prompts

System prompts define Claude's role and behavior. Store these in `system/`.

### Example: Code Review Assistant
```markdown
You are an expert code reviewer focused on:
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- Code maintainability and readability
- Best practices for the given language/framework

When reviewing code:
1. Identify issues by severity (critical, high, medium, low)
2. Explain WHY each issue matters
3. Provide specific code examples for fixes
4. Suggest alternative approaches when applicable

Format your response with clear sections and prioritize critical issues first.
```

### Example: Data Extraction Specialist
```markdown
You are a data extraction specialist. Your role is to:
- Extract structured information from unstructured text
- Maintain accuracy and cite sources
- Handle missing or ambiguous data gracefully
- Output data in specified formats (JSON, CSV, XML)

Guidelines:
- If information is uncertain, mark it with "confidence: low"
- Never fabricate data - use null for missing fields
- Preserve original terminology when extracting technical terms
```

## Task Prompts

Task-specific prompts for repeatable operations. Store in `tasks/`.

### Example: Summarization
```markdown
Summarize the following document:

<document>
{{CONTENT}}
</document>

Requirements:
- 3-5 bullet points
- Focus on key decisions and action items
- Include relevant dates and deadlines
- Highlight any blockers or risks
```

### Example: Code Documentation
```markdown
Generate documentation for this code:

<code>
{{CODE}}
</code>

Include:
- High-level purpose
- Parameters and return values
- Usage examples
- Edge cases and error handling
- Dependencies
```

## Templates

Reusable templates with placeholders. Store in `templates/`.

### Template Structure
```markdown
# Template: {{TEMPLATE_NAME}}

## Purpose
{{DESCRIPTION}}

## Variables
- {{VAR_1}}: Description
- {{VAR_2}}: Description

## Prompt
{{ACTUAL_PROMPT_CONTENT}}

## Example Usage
Input: ...
Output: ...
```

### Example: API Response Parser
```markdown
# Template: API Response Parser

## Purpose
Extract and structure data from API responses

## Variables
- {{API_RESPONSE}}: Raw API response (JSON/XML)
- {{FIELDS}}: Fields to extract
- {{OUTPUT_FORMAT}}: Desired output format

## Prompt
Parse the following API response and extract these fields: {{FIELDS}}

<response>
{{API_RESPONSE}}
</response>

Output format: {{OUTPUT_FORMAT}}

Requirements:
- Handle missing fields gracefully
- Validate data types
- Flag any anomalies
```

## Prompt Patterns

### Chain of Thought
For complex reasoning tasks:
```markdown
Analyze this problem step by step:

<problem>
{{PROBLEM}}
</problem>

Think through:
1. What are the key components?
2. What relationships exist between them?
3. What constraints apply?
4. What's the optimal solution?

Show your reasoning at each step.
```

### Structured Output
For consistent data formatting:
```xml
<output_format>
{
  "summary": "Brief summary",
  "details": ["point 1", "point 2"],
  "confidence": 0.95,
  "sources": ["source 1"]
}
</output_format>
```

## Best Practices

1. **Version your prompts** - Track what works and what doesn't
2. **Test iteratively** - Start simple, add complexity as needed
3. **Use examples** - Show Claude what good output looks like
4. **Be specific** - Vague prompts get vague results
5. **Provide constraints** - Length, format, style, tone
6. **Separate instructions from data** - Use XML tags or clear delimiters

## Anti-Patterns to Avoid

❌ Overly complex mega-prompts
❌ Ambiguous instructions
❌ Mixing multiple unrelated tasks
❌ Assuming context Claude doesn't have
❌ Not specifying output format

## References

- [Claude Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Using XML Tags](https://docs.anthropic.com/claude/docs/use-xml-tags)
- [Prompt Examples](https://docs.anthropic.com/claude/docs/examples)

## Next Steps

1. Create your first system prompt in `system/`
2. Build task-specific prompts for common operations
3. Extract reusable patterns into `templates/`
4. Document what works in `../knowledge/best-practices/`
