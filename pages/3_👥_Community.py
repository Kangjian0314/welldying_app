# pages/3_👥_Community.py
import streamlit as st

st.set_page_config(page_title="커뮤니티", page_icon="👥", layout="centered")
if st.session_state.get("user") is None:
    st.switch_page("app.py")

head = "#B68C66"; text = "#5A524B"; sub = "#8D857E"
posts = st.session_state.posts
liked = st.session_state.liked

# 탭(정렬)
tab_pop, tab_new = st.tabs(["인기글", "최신글"])

def post_card(p):
    with st.container(border=True):
        top = st.columns([0.1, 0.7, 0.2])
        top[0].markdown(f"### {p['emoji']}")
        top[1].markdown(f"**{p['nick']}**  \n<small style='color:{sub}'>{p['minutes_ago']//60}시간 전</small>", unsafe_allow_html=True)
        top[2].write("")
        st.write(p["content"])
        if p.get("tags"):
            st.caption(" ".join([f"#{t}" for t in p["tags"]]))
        # 좋아요/댓글
        c1, c2, c3, c4 = st.columns([0.18,0.22,0.22,0.38])
        liked_now = p["id"] in liked
        if c1.button(("❤️" if liked_now else "🤍") + f" {p['likes']}", key=f"like_{p['id']}"):
            if liked_now:
                liked.remove(p["id"])
                p["likes"] = max(0, p["likes"] - 1)
            else:
                liked.add(p["id"])
                p["likes"] += 1
            st.experimental_rerun()
        c2.write("")  # spacer
        # 댓글 영역
        with c3:
            exp = st.toggle("댓글", key=f"exp_{p['id']}", value=False)
        if exp:
            for i, c in enumerate(p["comments"]):
                st.write(f"- {c}")
            new_c = st.text_input("댓글 입력", key=f"newc_{p['id']}")
            if st.button("등록", key=f"addc_{p['id']}") and (new_c or "").strip():
                p["comments"].append(new_c.strip())
                st.experimental_rerun()

with tab_pop:
    for p in sorted(posts, key=lambda x: x["likes"], reverse=True):
        post_card(p)

with tab_new:
    for p in sorted(posts, key=lambda x: x["minutes_ago"]):   # 최신(minutes_ago 작을수록 최신)
        post_card(p)

st.divider()
# 글쓰기(간단): 내용 + 태그
with st.expander("＋ 새 글쓰기"):
    colA, colB = st.columns([3,1])
    content = colA.text_area("내용", placeholder="반려동물 이야기를 공유해요!")
    tags = colB.text_input("태그(쉼표로 구분)", placeholder="노견, 관절")
    if st.button("게시"):
        import uuid
        st.session_state.posts.insert(0, {
            "id": str(uuid.uuid4()),
            "nick": st.session_state.user["id"] or "나",
            "emoji": "🙂",
            "content": content.strip() or "새 글",
            "likes": 0,
            "comments": [],
            "minutes_ago": 0,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "image_path": None
        })
        st.success("게시 완료!")
        st.experimental_rerun()
