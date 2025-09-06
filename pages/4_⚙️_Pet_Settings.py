# pages/4_⚙️_Pet_Settings.py
import streamlit as st

st.set_page_config(page_title="펫 설정(데모)", page_icon="⚙️", layout="centered")
if st.session_state.get("user") is None:
    st.switch_page("app.py")

st.markdown("### 펫 설정 (데모)")
with st.form("pet_form"):
    name = st.text_input("이름", value="매생이")
    breed = st.text_input("품종", value="미니어처 푸들")
    age = st.text_input("나이", value="8살")
    submitted = st.form_submit_button("저장", type="primary")
    if submitted:
        st.success("저장되었습니다. (데모: 홈 UI에 직접 반영은 생략)")
