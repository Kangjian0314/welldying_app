# pages/2_📝_Care_Checklist.py
import streamlit as st
from uuid import uuid4

st.set_page_config(page_title="케어 체크리스트", page_icon="📝", layout="centered")
if st.session_state.get("user") is None:
    st.switch_page("app.py")

st.markdown("### 오늘의 케어 체크")

tasks = st.session_state.care_tasks

# 추가
with st.form("add_task_form", clear_on_submit=True):
    new_title = st.text_input("새 항목", placeholder="예: 아침 산책")
    c1, c2 = st.columns([1,3])
    submitted = c1.form_submit_button("추가", type="primary")
    if submitted:
        title = (new_title or "").strip()
        if title:
            tasks.append({"id": str(uuid4()), "title": title, "done": False})
            st.success("항목이 추가되었어요.")
            st.experimental_rerun()

st.divider()

# 목록
remove_ids = []
for t in tasks:
    cols = st.columns([0.1, 0.7, 0.2])
    with cols[0]:
        checked = st.checkbox("", value=t["done"], key=f"task_done_{t['id']}")
        t["done"] = checked
    cols[1].write(f"**{t['title']}**" if not t["done"] else f"~~{t['title']}~~")
    with cols[2]:
        if st.button("삭제", key=f"del_{t['id']}"):
            remove_ids.append(t["id"])

if remove_ids:
    st.session_state.care_tasks = [x for x in tasks if x["id"] not in remove_ids]
    st.experimental_rerun()
