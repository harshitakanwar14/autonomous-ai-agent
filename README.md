# Autonomous AI Agent

An autonomous agent built with Python and Google's Gemini API. Give it an objective and it plans the work, picks tools, executes them, observes the results and repeats until the task is done. It comes with a ChatGPT-style web UI (Streamlit) and a CLI.

## Features

- AI-generated execution plans
- Dynamic tool selection: web search, calculator, file read and file write
- Observe-and-continue loop (up to `MAX_ITERATIONS` steps)
- SQLite memory of every run (`agent_memory.db`)
- Gemini model fallback on errors
- Web UI with chat history, collapsible tool steps and one-click example prompts

## Quick start

```bash
git clone https://github.com/harshitakanwar14/autonomous-ai-agent
cd autonomous-ai-agent
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Create a `.env` file with your key (get one at https://aistudio.google.com):

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Run the web UI:

```bash
.venv/bin/streamlit run app.py
```

Or the CLI:

```bash
.venv/bin/python main.py
```

## Example prompts

- Research the latest breakthroughs in AI agents this week, then write an executive briefing with sources to `output/ai_briefing.md`
- Compare the top 3 programming languages for AI development in 2026 by popularity and salary, and save a decision table to `output/language_comparison.md`
- Plan a 3-day Tokyo trip for $1500: search current flight and hotel price ranges, calculate a daily budget, and save the itinerary to `output/tokyo_trip.md`

## How it works

1. **Planner** turns the objective into an execution plan.
2. **Brain** (Gemini) decides the next action: call a tool, ask the user, or finish.
3. **Executor** runs the chosen tool from the tool registry.
4. **Observer** records the result, which is fed back to the Brain.
5. **Memory** stores each run and its observations in SQLite.
6. The loop ends when the Brain finishes or the iteration limit is reached.

## Project structure

```text
app.py        Streamlit web UI (chat history saved to chats.json)
main.py       CLI entry point
agent/        planner, brain, executor, observer, memory
tools/        registry, calculator, web_search, file_reader, file_writer
config/       settings and Gemini client with fallback
output/       files written by the agent
tests/        tests
```

## Notes

- Each chat message is an independent run; the agent doesn't see earlier messages in the same chat.
- `.env`, `agent_memory.db` and `chats.json` are git-ignored.

## Author

Harshita Kanwar
