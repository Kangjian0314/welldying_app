# pages/1_🏠_Life_Care_Home.py
import streamlit as st
from datetime import datetime, timedelta
from dateutil import tz

st.set_page_config(page_title="우리 아이 케어", page_icon="🏠", layout="centered")

if st.session_state.get("user") is None:
    st.switch_page("app.py")

bg = "#FAF6F1"; head = "#B68C66"; text = "#5A524B"; sub = "#8D857E"

st.markdown(f"<h3 style='color:{text}'>우리 아이 케어</h3>", unsafe_allow_html=True)

# --- 반려동물 카드 (간단 버전) ---
with st.container(border=True):
    cols = st.columns([1,4,1])
    cols[0].markdown("### 🐶")
    with cols[1]:
        st.markdown("**매생이**  \n미니어처 푸들 · 8살  \n2017.12.25 입양", unsafe_allow_html=True)
    cols[2].page_link("pages/4_⚙️_Pet_Settings.py", label="편집", icon="✏️")

st.divider()

# --- 이번 주 스트립 + 선택 날짜 일정 ---
now = st.session_state.start_date_anchor
kst = tz.gettz("Asia/Seoul")
today = datetime.now(tz=kst)
start = today - timedelta(days=today.weekday())   # 월요일
days = [start + timedelta(days=i) for i in range(7)]

selected_date = st.session_state.get("selected_date", today.date())

st.markdown("#### 이번 주 일정")
colw = st.columns(7)
ko = ["월","화","수","목","금","토","일"]
for i, d in enumerate(days):
    label = f"{ko[i]}<br><span style='font-size:20px;font-weight:700'>{d.day}</span>"
    is_sel = (selected_date == d.date())
    if colw[i].button(label, key=f"day_{i}", help=d.strftime("%Y.%m.%d"),
                      use_container_width=True):
        selected_date = d.date()
        st.session_state.selected_date = selected_date
    if is_sel:
        colw[i].markdown(f"<div style='text-align:center;color:white;background:{head};border-radius:12px;padding:4px 0'>선택</div>", unsafe_allow_html=True)

st.markdown(f"**선택일:** `{selected_date}`")

# 일정 리스트(선택일)
schedules = st.session_state.schedules
selected_list = [s for s in schedules if s["dt"].date() == selected_date]
selected_list.sort(key=lambda x: x["dt"])

with st.container(border=True):
    st.markdown("##### 📅 선택한 날짜의 일정")
    if not selected_list:
        st.info("이 날짜에는 등록된 일정이 없어요.")
    else:
        for s in selected_list:
            st.write(f"- {s['title']} ({s['dt'].strftime('%H:%M')})")

    with st.expander("＋ 일정 추가"):
        title = st.text_input("내용", key="add_title")
        dt = st.date_input("날짜", value=selected_date, key="add_date")
        tm = st.time_input("시간", value=datetime.now(tz=kst).time(), key="add_time")
        if st.button("추가", type="primary"):
            from datetime import datetime
            new_dt = datetime(dt.year, dt.month, dt.day, tm.hour, tm.minute, tzinfo=kst)
            st.session_state.schedules.append({"title": title.strip() or "새 일정", "dt": new_dt})
            st.success("일정이 추가되었습니다.")
            st.experimental_rerun()

st.divider()

# --- 오늘의 케어 체크 프리뷰 ---
st.markdown("#### 오늘의 케어 체크")
tasks = st.session_state.care_tasks
for i, t in enumerate(tasks):
    new_val = st.checkbox(t["title"], value=t["done"], key=f"home_task_{t['id']}")
    t["done"] = new_val
col = st.columns([1,1,1,1])
col[-1].page_link("pages/2_📝_Care_Checklist.py", label="전체보기 →")
