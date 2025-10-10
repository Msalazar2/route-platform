import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import streamlit as st

# Load .env from repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(dotenv_path=os.path.join(REPO_ROOT, ".env"))

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000/api")
NOTES_URL = f"{API_BASE}/notes"
HEALTH_URL = f"{API_BASE}/health"

st.set_page_config(page_title="Route Proto (API)", page_icon="🔌", layout="centered")
st.title("🔌 Route Prototype (via FastAPI)")
st.caption("Streamlit → FastAPI → Postgres")

@st.cache_data(ttl=5.0)
def check_health():
    try:
        r = httpx.get(HEALTH_URL, timeout=5.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

@st.cache_data(ttl=0.5)
def fetch_notes():
    r = httpx.get(NOTES_URL, timeout=10.0)
    r.raise_for_status()
    return r.json()

def create_note(body: str, author: str | None):
    payload = {"body": body}
    if author:
        payload["author"] = author
    r = httpx.post(NOTES_URL, json=payload, timeout=10.0)
    r.raise_for_status()
    return r.json()

# --- UI ---
health = check_health()
st.info(f"API health: {health.get('ok')} · ts={health.get('ts', 'n/a')}")

with st.form("new_note", clear_on_submit=True):
    st.subheader("Add a note (via API)")
    col1, col2 = st.columns([2,1])
    with col1:
        body = st.text_input("Note", placeholder="hello from Streamlit → FastAPI")
    with col2:
        author = st.text_input("Author (optional)")
    submitted = st.form_submit_button("Create")
    if submitted:
        if body.strip():
            try:
                create_note(body.strip(), author.strip() or None)
                st.success("Created.")
                # bust caches so list refreshes immediately
                fetch_notes.clear()
                st.rerun()
            except httpx.HTTPError as e:
                st.error(f"Create failed: {e}")
        else:
            st.warning("Please enter a note.")

st.divider()
st.subheader("Recent notes (latest 100)")

try:
    rows = fetch_notes()
    if rows:
        for r in rows:
            created = r["created_at"]
            # coerce to readable if string:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created_disp = dt.strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                created_disp = created
            st.write(f"**#{r['id']}** · {created_disp} — {r['body']}  _(by {r.get('author') or 'anon'})_")
    else:
        st.info("No rows yet.")
except httpx.HTTPError as e:
    st.error(f"Fetch failed: {e}")
