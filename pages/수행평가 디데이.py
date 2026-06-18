import streamlit as st
from datetime import date

st.set_page_config(
    page_title="수행평가 D-Day 관리기",
    page_icon="📚",
    layout="centered"
)

st.title("📚 수행평가 D-Day 관리기")
st.markdown("수행평가 날짜를 입력하면 남은 기간을 알려줍니다.")

today = date.today()

# 수행평가 개수
count = st.number_input(
    "수행평가 개수",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)

tasks = []

st.divider()

for i in range(count):
    st.subheader(f"수행평가 {i+1}")

    name = st.text_input(
        f"과목 또는 수행평가 이름",
        key=f"name_{i}"
    )

    due_date = st.date_input(
        f"제출 날짜",
        value=today,
        key=f"date_{i}"
    )

    diff = (due_date - today).days

    if diff > 0:
        status = f"⏳ D-{diff}"
    elif diff == 0:
        status = "🔥 오늘 제출!"
    else:
        status = f"✅ 종료 ({abs(diff)}일 지남)"

    st.info(status)

    if name.strip():
        tasks.append({
            "수행평가": name,
            "날짜": due_date.strftime("%Y-%m-%d"),
            "남은일수": diff
        })

st.divider()

if tasks:
    future_tasks = [t for t in tasks if t["남은일수"] >= 0]

    if future_tasks:
        nearest = min(future_tasks, key=lambda x: x["남은일수"])

        st.success(
            f"가장 가까운 수행평가: "
            f"**{nearest['수행평가']}** "
            f"(D-{nearest['남은일수']})"
        )
    else:
        st.warning("예정된 수행평가가 없습니다.")

    st.subheader("📋 전체 일정")

    table_data = []

    for t in sorted(tasks, key=lambda x: x["남은일수"]):
        if t["남은일수"] > 0:
            state = f"D-{t['남은일수']}"
        elif t["남은일수"] == 0:
            state = "오늘"
        else:
            state = f"{abs(t['남은일수'])}일 지남"

        table_data.append({
            "수행평가": t["수행평가"],
            "날짜": t["날짜"],
            "상태": state
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("수행평가 이름을 입력하면 일정이 표시됩니다.")
