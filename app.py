import streamlit as st
import random

# 게임 목록
games = [
    "마인크래프트",
    "리그 오브 레전드",
    "발로란트",
    "로블록스",
    "오버워치 2",
    "스타듀밸리",
    "피파 온라인",
    "배틀그라운드",
    "젤다의 전설",
    "에이펙스 레전드"
]

# 제목
st.title("🎮 게임 추천 프로그램")

st.write("버튼을 누르면 게임 하나를 추천해줌 ㅋㅋ")

# 버튼
if st.button("게임 추천받기"):
    game = random.choice(games)
    st.success(f"오늘 할 게임: {game}")
