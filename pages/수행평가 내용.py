import streamlit as st

st.set_page_config(
    page_title="수행평가 안내서",
    page_icon="📚",
    layout="wide"
)

st.title("📚 수행평가 안내서")
st.caption("과목별 수행평가 내용을 한눈에 확인해보세요.")

# 데이터
subjects = [
    {
        "과목": "국어",
        "내용": "문학 작품 감상문 작성",
        "준비물": "교과서, 필기구",
        "난이도": "⭐⭐⭐",
        "팁": "작품의 주제와 자신의 생각을 연결하여 작성하면 좋습니다."
    },
    {
        "과목": "영어",
        "내용": "영어 발표 및 질의응답",
        "준비물": "발표 자료(PPT 가능)",
        "난이도": "⭐⭐⭐⭐",
        "팁": "짧은 문장으로 연습하고 여러 번 말해보세요."
    },
    {
        "과목": "수학",
        "내용": "수학 탐구 보고서 작성",
        "준비물": "계산기, 노트",
        "난이도": "⭐⭐⭐⭐⭐",
        "팁": "생활 속 사례를 활용하면 탐구 주제를 정하기 쉽습니다."
    },
    {
        "과목": "과학",
        "내용": "실험 보고서 작성",
        "준비물": "실험 기록지",
        "난이도": "⭐⭐⭐⭐",
        "팁": "실험 과정과 결과를 자세히 기록하세요."
    },
    {
        "과목": "사회",
        "내용": "시사 주제 조사 발표",
        "준비물": "인터넷 자료",
        "난이도": "⭐⭐⭐",
        "팁": "최근 뉴스 자료를 활용하면 좋습니다."
    }
]


# 검색
search = st.text_input(
    "🔍 과목 검색",
    placeholder="예: 수학"
)

filtered = []

if search:
    for s in subjects:
        if search in s["과목"]:
            filtered.append(s)
else:
    filtered = subjects


if not filtered:
    st.warning("검색 결과가 없습니다.")

else:

    cols = st.columns(2)

    for idx, sub in enumerate(filtered):

        with cols[idx % 2]:

            with st.container(border=True):

                st.subheader(f"📖 {sub['과목']}")

                st.write(f"**수행 내용**")
                st.write(sub["내용"])

                st.write(f"**준비물**")
                st.write(sub["준비물"])

                st.write(f"**난이도**")
                st.write(sub["난이도"])

                with st.expander("💡 공부 팁 보기"):
                    st.info(sub["팁"])


st.divider()

st.markdown("### 📌 수행평가 준비 체크리스트")

check1 = st.checkbox("평가 날짜 확인")
check2 = st.checkbox("준비물 챙기기")
check3 = st.checkbox("발표 또는 보고서 연습")
check4 = st.checkbox("제출 기한 확인")


if check1 and check2 and check3 and check4:
    st.success("🎉 수행평가 준비 완료!")
