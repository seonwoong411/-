import streamlit as st
import random

st.title("🎯 숫자 맞추기 게임")

# 정답 저장
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 10)

guess = st.number_input("1~10 숫자 입력", 1, 10)

if st.button("확인"):
    if guess == st.session_state.answer:
        st.success("정답이다 ㅋㅋ")
    elif guess < st.session_state.answer:
        st.warning("더 큰 숫자임")
    else:
        st.warning("더 작은 숫자임")
