# AI Symposium 🎭

> A sophisticated multi-agent debate platform powered by OpenAI's Swarm framework, enabling structured intellectual discourse between AI agents.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Swarm-green.svg)

## Overview

AI Symposium revives the classical tradition of intellectual discourse for the AI age. Built on OpenAI's Swarm framework, it orchestrates sophisticated debates between AI agents, creating structured, meaningful discussions on complex topics.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-symposium.git
cd ai-symposium

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Clone Swarm framework
git clone https://github.com/openai/swarm.git

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API key
export OPENAI_API_KEY='your-api-key-here'  # Windows: set OPENAI_API_KEY=your-api-key-here
```

### Quick Start

```python
# main.py
from src.symposium.core import Symposium, DebateConfig

# Configure your debate
config = DebateConfig(
    topic="Should artificial intelligence be regulated?",
    pro_position="AI regulation ensures safety and ethical development",
    con_position="Regulation stifles innovation and progress",
    max_turns=10
)

# Initialize and run
symposium = Symposium()
symposium.setup_debate(config)
result = symposium.run_debate(
    "Welcome to today's debate on AI regulation. Let's begin with opening statements."
)
```

Run the debate:
```bash
python main.py
```

## Configuration Options

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `topic` | str | Main debate topic | Required |
| `pro_position` | str | Affirmative position | Required |
| `con_position` | str | Opposing position | Required |
| `max_turns` | int | Maximum debate turns | 10 |
| `style` | str | Debate format style | "structured" |
| `time_per_turn` | int | Seconds per turn | 300 |

## Project Structure

```
ai-symposium/
├── swarm/              # Cloned OpenAI Swarm repository
├── src/
│   └── symposium/
│       ├── __init__.py
│       ├── core.py     # Main orchestration logic
│       ├── agents/     # Agent definitions
│       │   ├── __init__.py
│       │   ├── moderator.py
│       │   └── debater.py
│       ├── config/     # Configuration
│       │   ├── __init__.py
│       │   └── debate_config.py
│       └── utils/      # Helper functions
│           ├── __init__.py
│           └── formatting.py
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## Requirements

The project requires the following dependencies:
- OpenAI's Swarm framework
- OpenAI API access
- python-dotenv
- Other dependencies listed in requirements.txt

## Known Limitations

- Speakers tend to be overly verbose and repetitive
- Debate phases don't transition smoothly
- Moderator can be rigid and templated
- Summary quality needs improvement
- No access to external information or fact-checking
- Limited to two speakers and text-only format
- Can produce formatting artifacts in responses
- Arguments may lack proper structure and flow

## Future Improvements 🚀

### Knowledge & Research 📚
- Real-time internet access and fact-checking
- Document reference and citation system
- Academic database integration

### Audio Features 🎙️
- Natural voice synthesis for all participants
- Real-time audio streaming
- Podcast-quality production

### Enhanced Interaction 🤝
- Live audience participation
- Multi-speaker debates
- Real-time voting and feedback
- Fact-check requests

*Note: Currently an experimental platform with bugs*
