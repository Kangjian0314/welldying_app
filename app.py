# app.py
import streamlit as st
from datetime import datetime
from dateutil import tz

st.set_page_config(page_title="Welldying", page_icon="🐶", layout="centered")

# ------- 세션 초기화 -------
def init_state():
    ss = st.session_state
    if "user" not in ss:
        ss.user = None   # {"id": "...", "remember": True/False}
    if "care_tasks" not in ss:
        # Flutter CareTask.simple(...)에 해당
        ss.care_tasks = [
            {"id": "t1", "title": "아침 산책", "done": False},
            {"id": "t2", "title": "사료 급여", "done": False},
            {"id": "t3", "title": "관절 영양제", "done": False},
            {"id": "t4", "title": "저녁 산책", "done": False},
        ]
    if "schedules" not in ss:
        # [{"title": "...", "dt": datetime}]
        now = datetime.now(tz=tz.gettz("Asia/Seoul"))
        ss.schedules = [
            {"title": "관절 영양제", "dt": now.replace(hour=14, minute=0, second=0, microsecond=0)},
            {"title": "내일 정기검진 예약 확인", "dt": (now.replace(hour=9, minute=0, second=0, microsecond=0)).replace(day=now.day + 1)},
        ]
    if "posts" not in ss:
        # 커뮤니티 초기 더미 데이터
        ss.posts = [
            {
                "id": "p1",
                "nick": "냥집사", "emoji": "🐱",
                "content": "15살 노묘 식욕부진, 이렇게 해결했어요! 수의사 상담+식이요법으로 많이 좋아졌어요🥰",
                "likes": 24, "comments": ["도움돼요!", "공유 감사해요"],
                "minutes_ago": 120, "tags": ["노묘케어","식욕부진","영양제"],
                "image_path": None
            },
            {
                "id": "p2",
                "nick": "멍멍이네", "emoji": "🐶",
                "content": "노견 관절 관리 꿀팁! 매달 하는 루틴 공유합니다.",
                "likes": 18, "comments": ["좋은 정보네요"], 
                "minutes_ago": 240, "tags": ["노견","관절"], 
                "image_path": None
            },
        ]
    if "liked" not in ss:
        ss.liked = set()   # 사용자가 좋아요 누른 post id
    if "start_date_anchor" not in ss:
        ss.start_date_anchor = datetime.now(tz=tz.gettz("Asia/Seoul"))

init_state()

# ------- 로그인 화면 -------
def login_view():
    st.markdown("### Welldying\n“마지막까지 존엄하게, 기억은 따뜻하게”\n반려동물 AI 장례 서비스", help="데모 로그인 화면")
    st.divider()
    with st.form("login_form"):
        col1, col2 = st.columns([1,1])
        with col1:
            user_id = st.text_input("아이디", value=st.session_state.get("saved_id",""))
        with col2:
            pw = st.text_input("비밀번호", type="password")
        col3, col4 = st.columns([1,1])
        with col3:
            remember = st.checkbox("아이디 저장", value=bool(st.session_state.get("saved_id")))
        with col4:
            st.caption("아직 회원이 아니세요? 👉 *데모에선 즉시 로그인만 제공*")
        submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)
        if submitted:
            # 데모: 비번 검증 없이 로그인
            st.session_state.user = {"id": user_id.strip() or "guest", "remember": remember}
            if remember:
                st.session_state.saved_id = user_id.strip()
            else:
                st.session_state.saved_id = ""
            st.success("로그인 완료!")
            st.switch_page("pages/1_🏠_Life_Care_Home.py")

# ------- 라우팅 -------
if st.session_state.user is None:
    login_view()
else:
    st.markdown(f"👋 **{st.session_state.user['id']}**님, 상단 좌측의 *Pages*에서 화면을 선택하세요.")
    st.page_link("pages/1_🏠_Life_Care_Home.py", label="🏠 우리 아이 케어 홈", icon="🏠")
    st.page_link("pages/2_📝_Care_Checklist.py", label="📝 오늘의 케어 체크", icon="📝")
    st.page_link("pages/3_👥_Community.py", label="👥 커뮤니티", icon="👥")
    st.page_link("pages/4_⚙️_Pet_Settings.py", label="⚙️ 펫 설정(데모)", icon="⚙️")
    st.divider()
    if st.button("로그아웃"):
        st.session_state.user = None
        st.rerun()
