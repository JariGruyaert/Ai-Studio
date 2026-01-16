# Knowledge

Your second brain for AI development. Document learnings, patterns, and best practices as you build.

## Overview

This directory is your knowledge repository:
- **claude-docs/** - Notes and learnings from Claude documentation
- **best-practices/** - What works, what doesn't, and why
- **patterns/** - Reusable patterns and strategies

## Philosophy

### Learn by Doing
- Build something → Document what worked → Refine
- Theory is useful, but practical experience is invaluable
- Keep notes concise and actionable

### Knowledge Compounds
- Small learnings accumulate over time
- Cross-reference related concepts
- Revisit and update as you learn more

### Make it Searchable
- Use clear titles and tags
- Include examples and code snippets
- Link to source material

## Directory Structure

```
knowledge/
├── claude-docs/        # Learnings from Claude documentation
├── best-practices/     # Proven patterns and approaches
└── patterns/           # Reusable design patterns
```

## Document Template

```markdown
# [Topic Name]

## Context
What problem does this solve? When is it useful?

## Key Concepts
- Concept 1: Explanation
- Concept 2: Explanation

## Implementation
How to apply this in practice.

\`\`\`python
# Code example
\`\`\`

## Examples
Real-world usage examples.

## Gotchas
Common mistakes and edge cases.

## References
- [Link to docs]
- [Related notes]

## Date
YYYY-MM-DD
```

## Categories to Track

### Prompt Engineering
- Effective prompt patterns
- XML tag usage
- Chain-of-thought strategies
- Few-shot examples that work

### Context Engineering
- Context window management
- Retrieval strategies
- Caching techniques
- Context optimization

### Agent Development
- Agent architectures
- Multi-agent coordination
- Error handling patterns
- State management

### Skills & Tools
- Custom skill patterns
- Tool integration approaches
- API usage patterns
- Performance optimization

## Note-Taking Strategy

### 1. Quick Capture
When you discover something useful:

```markdown
# Quick Note: [Topic]
Date: 2026-01-16

## What I learned
[Quick summary]

## Example
[Code or prompt]

## Next
[What to try next]
```

### 2. Structured Documentation
For more complete understanding:

```markdown
# [Topic]: Deep Dive

## Overview
Comprehensive explanation

## Use Cases
When to use this approach

## Implementation Guide
Step-by-step instructions

## Code Examples
Working code samples

## Trade-offs
Pros and cons

## Related
Links to related notes
```

### 3. Reference Material
Quick lookup information:

```markdown
# [Topic]: Reference

## Syntax
\`\`\`
Quick syntax reference
\`\`\`

## Parameters
- param1: Description
- param2: Description

## Examples
Common usage patterns
```

## Organizing Claude Docs Learnings

### File Naming Convention
```
claude-docs/
├── prompt-engineering-basics.md
├── xml-tags-usage.md
├── tool-use-patterns.md
├── context-management.md
└── agent-architecture.md
```

### Template for Claude Docs Notes

```markdown
# [Claude Docs Topic]

## Source
[Link to Claude docs]

## Summary
TL;DR of the key points

## Key Takeaways
1. Point 1
2. Point 2
3. Point 3

## My Experiments
What I tried based on this documentation

### Experiment 1
- **Tried**: Description
- **Result**: What happened
- **Learned**: Key insight

## Code Snippets
\`\`\`python
# Practical implementation
\`\`\`

## Questions to Explore
- [ ] Question 1
- [ ] Question 2

## Date
YYYY-MM-DD

## Tags
#prompt-engineering #tool-use #agents
```

## Best Practices Documentation

### What to Document
- ✅ Patterns that consistently work
- ✅ Common mistakes and how to avoid them
- ✅ Performance optimizations
- ✅ Security considerations
- ❌ One-off solutions (unless they teach a principle)
- ❌ Obvious or well-documented practices

### Template

```markdown
# Best Practice: [Name]

## Problem
What issue does this solve?

## Solution
The recommended approach

## Why It Works
Explanation of the underlying principle

## Example
\`\`\`python
# Good
good_example()

# Bad
bad_example()
\`\`\`

## When to Apply
Specific scenarios where this applies

## When NOT to Apply
Edge cases or exceptions

## Related Patterns
- [Pattern 1]
- [Pattern 2]
```

## Pattern Library

### Pattern Template

```markdown
# Pattern: [Name]

## Intent
What does this pattern accomplish?

## Motivation
Why would you use this pattern?

## Structure
\`\`\`
Component relationships and flow
\`\`\`

## Implementation
\`\`\`python
class PatternExample:
    # Implementation
\`\`\`

## Applicability
When to use this pattern:
- Scenario 1
- Scenario 2

## Consequences
Trade-offs and considerations

## Examples
Real-world usage in your projects

## Related Patterns
Similar or complementary patterns
```

## Cross-Referencing

Link related concepts together:

```markdown
# Prompt Engineering

See also:
- [Context Management](./context-management.md)
- [XML Tags Best Practice](../best-practices/xml-tags.md)
- [Agent System Prompts](../../agents/configs/examples.md)
```

## Version Control

Track how your understanding evolves:

```markdown
## Version History

### v2 - 2026-01-16
- Added section on async patterns
- Updated examples with error handling

### v1 - 2026-01-10
- Initial documentation
```

## Tagging System

Use consistent tags for easy searching:

```markdown
## Tags
#prompt-engineering #xml-tags #advanced #tested

## Difficulty
Beginner | Intermediate | Advanced

## Status
Draft | Tested | Production-Ready
```

## Knowledge Review Process

### Weekly Review
- Review new notes
- Consolidate related concepts
- Update existing notes with new learnings

### Monthly Review
- Archive outdated information
- Identify knowledge gaps
- Plan learning priorities

## Example: Complete Note

```markdown
# Effective XML Tag Usage in Prompts

## Context
XML tags help structure prompts and improve Claude's understanding of different sections.

## Source
https://docs.anthropic.com/claude/docs/use-xml-tags

## Key Concepts
- Use tags to separate instructions from data
- Nested tags for hierarchical structure
- Consistent naming improves reliability

## Implementation
\`\`\`xml
<task>
Analyze the following code for security issues
</task>

<code>
def process_user_input(data):
    return eval(data)  # Dangerous!
</code>

<requirements>
- Check for injection vulnerabilities
- Verify input validation
- Suggest safer alternatives
</requirements>
\`\`\`

## My Experiments

### Experiment 1: Structured Data Extraction
- **Tried**: Using XML tags to specify output format
- **Result**: 95% consistent structured output
- **Learned**: Tags work better than JSON examples for structure

### Experiment 2: Multi-Document Analysis
- **Tried**: Separate documents with `<document id="1">` tags
- **Result**: Claude correctly attributed findings to specific docs
- **Learned**: IDs help with cross-referencing

## Best Practices
1. Keep tag names semantic and consistent
2. Use nesting for complex structures
3. Always close tags properly
4. Combine with clear instructions

## Gotchas
- Don't over-complicate with too many nested levels
- Claude understands the content, not just the structure
- Tags complement good prompts, they don't replace them

## Related
- [Prompt Engineering Basics](./prompt-engineering-basics.md)
- [Context Management](./context-management.md)

## Date
2026-01-16

## Tags
#prompt-engineering #xml-tags #tested #best-practice

## Status
Production-Ready
\`\`\`

## Next Steps

1. Start documenting learnings from Claude docs
2. Capture patterns as you discover them
3. Review and consolidate weekly
4. Build your knowledge base iteratively

Remember: The goal is **useful knowledge you'll actually reference**, not comprehensive documentation.
