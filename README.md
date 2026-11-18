# Autonomous AI Agent

An autonomous AI agent built using Python and Google's Gemini API. The agent can understand user objectives, create execution plans, select tools dynamically, execute tasks, observe results, and maintain persistent memory.

## Features

- AI-powered task planning
- Dynamic decision-making using Gemini
- Tool registry and execution system
- Web search
- Calculator
- File reading and writing
- SQLite-based persistent memory
- Autonomous multi-step execution
- Fallback model support

## Tech Stack

- Python
- Google Gemini API
- Pydantic
- SQLite
- Web Search
- Streamlit (planned)

## Project Structure

```text
autonomous-ai-agent/
├── agent/
├── config/
├── tools/
├── output/
├── tests/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

1. Clone this repository.
2. Create a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file and add your Gemini API key.
5. Run `python main.py`.

## Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## How It Works

1. User provides an objective.
2. Planner generates an execution plan.
3. Brain selects the next appropriate action.
4. Executor runs the selected tool.
5. Observer records execution results.
6. Memory stores relevant information.
7. Agent continues until the objective is completed.

## Author

Harshita kanwar 