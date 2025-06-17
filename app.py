import streamlit as st
import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------
# 🧠 Subject Plan (14 Days)
# -------------------------------
subject_plan = {
    1: ("Operating Systems", ["Processes", "Scheduling", "Deadlock", "Memory Mgmt", "File Systems"]),
    2: ("Operating Systems", ["Virtual Memory", "I/O Systems", "Revision", "PYQs"]),
    3: ("Computer Architecture", ["Number Systems", "Gates", "Boolean Algebra", "Flip Flops", "PYQs"]),
    4: ("COA + DBMS", ["Pipelining", "Cache", "DBMS Intro", "Keys", "ER Model"]),
    5: ("DBMS", ["Normalization", "SQL", "Transactions", "Indexing"]),
    6: ("Algorithms + CN", ["Greedy", "Divide & Conquer", "Graphs", "Basics of CN"]),
    7: ("Computer Networks", ["TCP/IP", "OSI Model", "Routing", "Congestion"]),
    8: ("Data Structures + DM", ["Arrays", "Linked List", "Trees", "Hashing", "Combinatorics"]),
    9: ("DM + TOC", ["Set Theory", "Logic", "Graphs", "DFA/NFA", "CFG"]),
    10: ("TOC + Compiler Design", ["Turing Machines", "Parsing", "Code Generation"]),
    11: ("Compiler Design + EM", ["Lexical Analysis", "Intermediate Code", "Probability", "Matrices"]),
    12: ("Engineering Mathematics", ["Linear Algebra", "DE", "Statistics", "Quick Rev"]),
    13: ("Full Revision", ["PYQs", "Mistake Review", "Flashcards", "Summaries"]),
    14: ("Mock Test Day", ["Full-Length Test", "Time Mgmt", "Post-Test Analysis"]),
}

# -------------------------------
# 🌟 App Configuration
# -------------------------------
st.set_page_config(page_title="DTU AI Scheduler", layout="centered")
st.markdown("<h1 style='text-align:center;'>📘 DTU MTech Prep Scheduler</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:gray;'>Plan • Track • Succeed</h4>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# 📆 Determine Study Day
# -------------------------------
today = datetime.date.today()
start_date = today - datetime.timedelta(days=(today.day - 1))
day_num = (today - start_date).days + 1
day_num = min(day_num, 14)

subject, tasks = subject_plan.get(day_num, ("Done!", []))

st.markdown(f"### 📅 **Day {day_num}/14**")
st.markdown(f"#### 🎯 **Focus Area:** `{subject}`")
st.progress(day_num / 14)

# -------------------------------
# ✅ Task Checklist
# -------------------------------
st.markdown("### 📌 Today's Task Breakdown")
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

for idx, task in enumerate(tasks):
    key = f"day{day_num}_task{idx}"
    if key not in st.session_state.completed_tasks:
        st.session_state.completed_tasks[key] = False
    st.session_state.completed_tasks[key] = st.checkbox(f"📝 {task}", value=st.session_state.completed_tasks[key], key=key)

# -------------------------------
# 🔁 Productivity Sidebar
# -------------------------------
with st.sidebar:
    st.title("📊 Productivity Tracker")
    st.markdown("Log your daily input ⏳")
    hours = st.slider("Hours Studied", 0, 16, 4)
    pomodoros = st.slider("Pomodoros Completed", 0, 12, 5)
    rating = st.slider("Your Energy Today", 1, 10, 7)
    
    st.markdown("---")
    st.metric(label="⏰ Hours", value=f"{hours} hrs")
    st.metric(label="🍅 Pomodoros", value=pomodoros)
    st.metric(label="🔋 Focus Score", value=f"{rating}/10")

# -------------------------------
# 🔥 GROQ API Motivation
# -------------------------------
st.markdown("### 💡 Need a Boost?")
if st.button("⚡ Get AI Motivation"):
    with st.spinner("Talking to your AI mentor..."):
        prompt = f"""Motivate me for Day {day_num} of my DTU MTech prep. 
        Today's subject is {subject}. Give me a 2-3 sentence daily plan and motivation."""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            ai_message = response.json()["choices"][0]["message"]["content"]
            st.success("🧠 AI Guidance:")
            st.markdown(ai_message)
        else:
            st.error("❌ Error fetching motivation. Check GROQ API key or connection.")

# -------------------------------
# 🌈 Footer
# -------------------------------
st.markdown("---")
st.markdown("<small>Made with ❤️ by your AI Engineer | Stay consistent, succeed massively!</small>", unsafe_allow_html=True)
