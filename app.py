import json
import time
import uuid
from pathlib import Path

import streamlit as st

from agent.planner import AgentPlanner
from agent.brain import AgentBrain
from agent.executor import AgentExecutor
from agent.observer import AgentObserver
from agent.memory import AgentMemory
from tools.registry import ToolRegistry
from config.settings import MAX_ITERATIONS

CHATS_FILE = Path(__file__).parent / "chats.json"

EXAMPLES = [
    ("📰 AI briefing", "Research the latest breakthroughs in AI agents this week, then write an executive briefing with sources to output/ai_briefing.md"),
    ("⚖️ Language comparison", "Compare the top 3 programming languages for AI development in 2026 by popularity and salary, and save a decision table to output/language_comparison.md"),
    ("✈️ Tokyo trip planner", "Plan a 3-day Tokyo trip for $1500: search current flight and hotel price ranges, calculate a daily budget, and save the itinerary to output/tokyo_trip.md"),
]

st.set_page_config(page_title="Autonomous AI Agent", page_icon="🤖", layout="centered", initial_sidebar_state="expanded")
st.markdown("""
<style>
#MainMenu, footer, [data-testid="stToolbarActions"], [data-testid="stDecoration"] {visibility: hidden;}
header {background: transparent;}
[data-testid="stStatusWidget"] {visibility: visible;}
.block-container {max-width: 820px; padding-top: 2rem; padding-bottom: 6rem;}
[data-testid="stSidebar"] .stButton button[kind="secondary"] {justify-content: flex-start; border-color: transparent; background: transparent;}
[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {background: rgba(128,128,128,.15);}
.hero {text-align: center; margin: 4rem 0 2rem;}
.hero h1 {font-size: 2.2rem; font-weight: 650;}
.hero p {opacity: .65;}
</style>
""", unsafe_allow_html=True)


def load_chats():
    try:
        return json.loads(CHATS_FILE.read_text())
    except Exception:
        return {}


def save_chats():
    CHATS_FILE.write_text(json.dumps(st.session_state.chats, indent=1, default=str))


if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
if "current" not in st.session_state:
    st.session_state.current = None


def render_steps(steps):
    for s in steps:
        with st.expander(f"🔧 Step {s['i']}: {s['tool']} — {s['why']}"):
            st.code(s["result"], language="json")


def run_agent(goal, chat):
    registry = ToolRegistry()
    tools = registry.get_available_tools()
    brain, executor, observer, memory = AgentBrain(), AgentExecutor(registry), AgentObserver(), AgentMemory()
    run_id = None
    steps, answer, ok = [], "", True
    try:
        with st.status("Planning…", expanded=True) as status:
            plan = AgentPlanner().create_plan(goal=goal, available_tools=tools)
            run_id = memory.start_run(goal, plan.model_dump())
            history = []
            for i in range(1, MAX_ITERATIONS + 1):
                status.update(label=f"Step {i}/{MAX_ITERATIONS}: thinking…")
                d = brain.think(goal=goal, plan=plan.model_dump(), history=history[-10:], available_tools=tools)
                if d.action in ("finish", "ask_user"):
                    answer = d.completion_summary or d.message
                    memory.update_status(run_id, "completed" if d.action == "finish" else "paused")
                    status.update(label="Done", state="complete", expanded=False)
                    break
                status.update(label=f"Step {i}: running {d.tool_name}…")
                result = executor.execute(d)
                step = {"i": i, "tool": d.tool_name, "why": d.reasoning_summary,
                        "result": json.dumps(result, indent=2, default=str)[:3000]}
                steps.append(step)
                st.markdown(f"**Step {i}:** `{d.tool_name}` — {d.reasoning_summary}")
                obs = observer.observe(i, d, result)
                memory.add_observation(run_id, i, obs)
                history.append(obs)
            else:
                memory.update_status(run_id, "max_iterations")
                answer, ok = "Reached the iteration limit before finishing.", False
                status.update(label="Iteration limit reached", state="error")
    except Exception as e:
        if run_id:
            memory.update_status(run_id, "failed")
        answer, ok = f"Error: {e}", False
    return {"role": "assistant", "content": answer, "steps": steps, "ok": ok}


# ---- Sidebar: history ----
with st.sidebar:
    st.markdown("### 🤖 Agent")
    if st.button("➕ New chat", use_container_width=True, type="primary"):
        st.session_state.current = None
    st.markdown("**History**")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda kv: -kv[1]["ts"]):
        if st.button(chat["title"][:38], key=f"c_{cid}"):
            st.session_state.current = cid
            st.rerun()
    if st.session_state.chats and st.button("🗑 Clear history"):
        st.session_state.chats, st.session_state.current = {}, None
        save_chats()
        st.rerun()

chat = st.session_state.chats.get(st.session_state.current)

# ---- Main area ----
def fill(text):
    st.session_state.draft = text


hero = st.empty()
start_prompt = None
if not chat:
    with hero.container():
        st.markdown('<div class="hero"><h1>What should the agent do?</h1>'
                    '<p>Pick an example to edit, or write your own objective.</p></div>',
                    unsafe_allow_html=True)
        cols = st.columns(len(EXAMPLES))
        for col, (label, text) in zip(cols, EXAMPLES):
            col.button(label, use_container_width=True, help=text, on_click=fill, args=(text,))
        st.text_area("Objective", key="draft", height=110, placeholder="Give the agent an objective…",
                     label_visibility="collapsed")
        if st.button("Send ➤", type="primary") and st.session_state.get("draft", "").strip():
            start_prompt = st.session_state.draft.strip()
else:
    for m in chat["messages"]:
        with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🤖"):
            if m["role"] == "assistant":
                render_steps(m.get("steps", []))
                (st.markdown if m.get("ok", True) else st.error)(m["content"])
            else:
                st.markdown(m["content"])

prompt = start_prompt or (st.chat_input("Give the agent an objective…", submit_mode="stop") if chat else None)

if prompt:
    hero.empty()
    if not chat:
        cid = uuid.uuid4().hex
        st.session_state.chats[cid] = chat = {"title": prompt, "ts": time.time(), "messages": []}
        st.session_state.current = cid
    chat["ts"] = time.time()
    chat["messages"].append({"role": "user", "content": prompt})
    save_chats()
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🤖"):
        reply = run_agent(prompt, chat)
        (st.markdown if reply["ok"] else st.error)(reply["content"])
    chat["messages"].append(reply)
    save_chats()
    st.rerun()
