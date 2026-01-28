# Installation

Install TestAgent with pip:

```bash
pip install testagent
```

## Requirements

- Python 3.9+
- praisonaiagents (for AI evaluation)

## Optional Dependencies

```bash
# For development
pip install testagent[dev]

# For all features
pip install testagent[all]
```

## Verify Installation

```bash
testagent version
```

## Environment Setup

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Or use a `.env` file:

```
OPENAI_API_KEY=your-api-key
```

## Next Steps

- [Quick Start](quickstart.md) - Your first AI test
- [CLI Usage](cli.md) - Command line interface
