# Getting Started with Claude

## Source
[Claude Documentation](https://docs.anthropic.com/claude/docs)

## Quick Start

### 1. API Access
- Sign up at [console.anthropic.com](https://console.anthropic.com/)
- Get your API key
- Add to `config/settings/.env`

### 2. Basic API Usage

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(response.content[0].text)
```

### 3. System Prompts

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful coding assistant focused on Python.",
    messages=[
        {"role": "user", "content": "How do I read a CSV file?"}
    ]
)
```

## Key Concepts

### Models
- **Claude 3.5 Sonnet** - Best balance of intelligence and speed
- **Claude 3 Opus** - Most capable, for complex tasks
- **Claude 3 Haiku** - Fastest, for simple tasks

### Token Limits
- Sonnet: 200K context window
- Max output tokens: configurable (typically 4096)

### Best Practices
1. Use system prompts to set behavior
2. Provide clear, specific instructions
3. Use XML tags for structure
4. Include examples when needed
5. Handle errors gracefully

## Common Patterns

### Multi-turn Conversation
```python
messages = [
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's its population?"}
]
```

### Structured Output
```python
prompt = """
Extract information from this text and output as JSON.

<text>
John Smith is a software engineer at Acme Corp in San Francisco.
</text>

<output_format>
{
  "name": "...",
  "role": "...",
  "company": "...",
  "location": "..."
}
</output_format>
"""
```

### Tool Use (Function Calling)
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in NYC?"}]
)
```

## Experiments to Try

- [ ] Basic prompt and response
- [ ] System prompt customization
- [ ] Multi-turn conversation
- [ ] Structured output with XML tags
- [ ] Tool use / function calling
- [ ] Long context handling
- [ ] Streaming responses

## My Notes

### What Works Well
- Clear, specific instructions
- XML tags for structuring complex inputs
- Few-shot examples for consistent output
- System prompts for role definition

### What to Avoid
- Vague or ambiguous prompts
- Overly complex single prompts
- Assuming context without providing it
- Not specifying output format

## Next Steps
- [ ] Read prompt engineering guide
- [ ] Experiment with different system prompts
- [ ] Try tool use for real use case
- [ ] Build first agent with skills

## Date
2026-01-16

## Tags
#claude #getting-started #api #basics
