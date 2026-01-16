# Config

Configuration management, environment settings, and security.

## Overview

Central location for:
- Environment variables and API keys
- Application settings
- Environment-specific configurations
- Security best practices

## Directory Structure

```
config/
└── settings/        # Configuration files and environment variables
```

## Configuration Files

### Environment Variables

Store sensitive credentials in `.env` files (never commit these!).

```bash
# config/settings/.env
# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Application Settings
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Pipeline Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=text-embedding-3-small

# Vector DB
CHROMA_DB_PATH=./data/chroma_db
COLLECTION_NAME=documents
```

### Environment Template

Provide a template for others (or yourself on new machines).

```bash
# config/settings/.env.example
# Copy this to .env and fill in your values

# API Keys (required)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Database (optional)
DATABASE_URL=

# Application Settings
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Pipeline Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=text-embedding-3-small

# Vector DB
CHROMA_DB_PATH=./data/chroma_db
COLLECTION_NAME=documents
```

### Application Config

```yaml
# config/settings/app.yaml
app:
  name: AI Studio
  version: 1.0.0
  debug: false

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: logs/app.log

agents:
  default_model: claude-3-5-sonnet-20241022
  max_tokens: 4000
  timeout: 300

pipelines:
  chunk_size: 1000
  chunk_overlap: 200
  batch_size: 100

storage:
  data_dir: ./data
  cache_dir: ./cache
  temp_dir: ./temp
```

### Environment-Specific Configs

```yaml
# config/settings/development.yaml
debug: true
verbose_logging: true
use_cache: false
api_timeout: 60

# config/settings/production.yaml
debug: false
verbose_logging: false
use_cache: true
api_timeout: 30
performance_monitoring: true
```

## Loading Configuration

### Python Example

```python
# config/settings/config_loader.py
import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

class Config:
    """Configuration manager"""

    def __init__(self, env: str = None):
        """
        Initialize configuration

        Args:
            env: Environment (development, production)
        """
        self.env = env or os.getenv('ENV', 'development')
        self.config_dir = Path(__file__).parent

        # Load environment variables
        self._load_env()

        # Load base config
        self.settings = self._load_yaml('app.yaml')

        # Load environment-specific config
        env_config = self._load_yaml(f'{self.env}.yaml')
        self.settings.update(env_config)

    def _load_env(self):
        """Load .env file"""
        env_file = self.config_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML config file"""
        file_path = self.config_dir / filename

        if not file_path.exists():
            return {}

        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default

    def get_env(self, key: str, default=None):
        """Get environment variable"""
        return os.getenv(key, default)

# Usage
config = Config()
api_key = config.get_env('ANTHROPIC_API_KEY')
model = config.get('agents.default_model')
debug = config.get('debug', False)
```

### Simple Loader

```python
# config/settings/simple_config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/settings/.env')

# Access configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Pipeline settings
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
```

## Security Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.*.local

# API Keys
**/api_keys.txt
**/secrets.yaml

# Credentials
credentials.json
service-account.json

# Database
*.db
*.sqlite

# Logs (may contain sensitive info)
logs/
*.log
```

### 2. Use Environment Variables

```python
# Good
api_key = os.getenv('ANTHROPIC_API_KEY')

# Bad
api_key = "sk-ant-..."  # Never hardcode!
```

### 3. Validate Configuration

```python
# config/settings/validator.py
import os

def validate_config():
    """Validate required configuration is present"""
    required_vars = [
        'ANTHROPIC_API_KEY',
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")

# Call at startup
validate_config()
```

### 4. Secure File Permissions

```bash
# Protect sensitive files
chmod 600 config/settings/.env
chmod 600 config/settings/secrets.yaml
```

### 5. Use Secrets Management (Production)

For production, consider:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Secret Manager

```python
# Example: AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
secrets = get_secret('ai-studio-prod')
api_key = secrets['ANTHROPIC_API_KEY']
```

## Configuration Patterns

### Pattern: Layered Configuration

```
Default Config → Environment Config → Runtime Config → Environment Variables
(lowest priority)                                      (highest priority)
```

### Pattern: Configuration Schema

```python
# config/settings/schema.py
from typing import Optional
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    """Agent configuration schema"""
    default_model: str = Field(default="claude-3-5-sonnet-20241022")
    max_tokens: int = Field(default=4000, ge=1, le=200000)
    timeout: int = Field(default=300, ge=1)

class PipelineConfig(BaseModel):
    """Pipeline configuration schema"""
    chunk_size: int = Field(default=1000, ge=100, le=10000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    batch_size: int = Field(default=100, ge=1, le=1000)

class AppConfig(BaseModel):
    """Main application configuration"""
    debug: bool = False
    log_level: str = "INFO"
    agents: AgentConfig = AgentConfig()
    pipelines: PipelineConfig = PipelineConfig()

# Validate configuration
config = AppConfig(**settings)
```

### Pattern: Feature Flags

```yaml
# config/settings/features.yaml
features:
  vector_search: true
  entity_extraction: true
  advanced_chunking: false
  experimental_embeddings: false
```

```python
# Check feature flags
def is_enabled(feature: str) -> bool:
    return config.get(f'features.{feature}', False)

if is_enabled('vector_search'):
    # Use vector search
    pass
```

## API Key Management

### Rotating Keys

```bash
# config/settings/rotate_keys.sh
#!/bin/bash
# Rotate API keys safely

backup_file=".env.backup.$(date +%Y%m%d_%H%M%S)"

# Backup current .env
cp .env "$backup_file"
echo "Backed up to $backup_file"

# Update keys
echo "Update your API keys in .env"
echo "Old backup saved to: $backup_file"
```

### Key Validation

```python
# config/settings/validate_keys.py
import os
from anthropic import Anthropic

def validate_anthropic_key():
    """Validate Anthropic API key"""
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        return False, "API key not found"

    try:
        client = Anthropic(api_key=api_key)
        # Make a minimal API call
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        return True, "API key is valid"
    except Exception as e:
        return False, f"API key validation failed: {e}"

# Usage
valid, message = validate_anthropic_key()
print(message)
```

## Configuration Documentation

Document your configuration:

```markdown
# Configuration Guide

## Required Environment Variables

### ANTHROPIC_API_KEY
- **Required**: Yes
- **Description**: Anthropic API key for Claude access
- **Format**: `sk-ant-...`
- **Get it**: https://console.anthropic.com/

### OPENAI_API_KEY
- **Required**: No (only if using OpenAI embeddings)
- **Description**: OpenAI API key for embeddings
- **Format**: `sk-...`

## Optional Settings

### CHUNK_SIZE
- **Default**: 1000
- **Description**: Text chunk size for processing
- **Range**: 100-10000

### LOG_LEVEL
- **Default**: INFO
- **Options**: DEBUG, INFO, WARNING, ERROR
- **Description**: Logging verbosity
```

## Initialization Script

```python
# config/settings/init_config.py
#!/usr/bin/env python3
"""Initialize configuration for new environment"""

import os
from pathlib import Path
import shutil

def init_config():
    """Initialize configuration files"""
    config_dir = Path(__file__).parent

    # Copy .env.example to .env if doesn't exist
    env_example = config_dir / '.env.example'
    env_file = config_dir / '.env'

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"Created {env_file}")
        print("Please edit .env and add your API keys")
    else:
        print(".env already exists")

    # Create necessary directories
    dirs = ['../../data', '../../cache', '../../temp', '../../logs']
    for dir_path in dirs:
        path = (config_dir / dir_path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created {path}")

    print("\nConfiguration initialized!")
    print("Next steps:")
    print("1. Edit config/settings/.env with your API keys")
    print("2. Review config/settings/app.yaml")
    print("3. Run validation: python validate_keys.py")

if __name__ == '__main__':
    init_config()
```

## Best Practices

1. **Separate Secrets from Config**
   - Secrets → `.env` (never commit)
   - Config → `.yaml` (can commit)

2. **Provide Templates**
   - Include `.env.example`
   - Document all variables

3. **Validate Early**
   - Check config on startup
   - Fail fast with clear errors

4. **Layer Your Config**
   - Defaults → Environment → Runtime
   - Higher layers override lower

5. **Document Everything**
   - What each setting does
   - Valid ranges/options
   - Where to get API keys

## Next Steps

1. Copy `.env.example` to `.env`
2. Add your API keys
3. Review and adjust `app.yaml`
4. Run configuration validation
5. Document any custom settings

## References

- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [12 Factor App Config](https://12factor.net/config)
- Parent: [../README.md](../README.md)
