import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# 1. 페이지 기본 설정 (와이드 모드로 화면을 크게 사용)
st.set_page_config(
    page_title="수행평가 일정 캘린더",
    page_icon="📅",
    layout="wide",
)

# 2. 세션 상태(Session State) 초기화 - 일정 데이터를 저장할 공간
if "events" not in st.session_state:
    # 기본 예시 데이터 제공
    # FullCalendar는 end 날짜를 '미포함'하므로, 당일 일정이면 end를 다음 날로 지정해야 달력에 채워집니다.
    today_str = datetime.now().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    st.session_state["events"] = [
        {
            "title": "📑 수학 탐구 보고서 제출",
            "start": today_str,
            "end": tomorrow_str,
            "backgroundColor": "#FF6B6B",
            "borderColor": "#FF6B6B",
        },
        {
            "title": "🗣️ 영어 말하기 수행평가",
            "start": today_str,
            "end": tomorrow_str,
            "backgroundColor": "#4D96FF",
            "borderColor": "#4D96FF",
        }
    ]

# 3. 앱 타이틀 및 설명
st.title("📅 나의 수행평가 일정 기록 캘린더")
st.caption("수행평가 일정을 기록하고 한눈에 관리하세요. Streamlit Community Cloud 전용으로 설계되었습니다.")
st.markdown("---")

# 4. 레이아웃 분할 (왼쪽: 입력 및 관리 폼, 오른쪽: 대형 달력)
col_input, col_calendar = st.columns([1, 2])

# --- 왼쪽 사이드 입력 영역 ---
with col_input:
    st.subheader("📝 새로운 수행평가 등록")
    
    # 입력 폼 생성
    with st.form("event_form", clear_on_submit=True):
        subject = st.text_input("과목 및 평가 이름", placeholder="예: 국어 현대시 분석")
        
        # 시작일과 종료일 선택
        start_date = st.date_input("시작일", datetime.now())
        end_date = st.date_input("마감일(종료일)", datetime.now())
        
        # 과목별 구분을 위한 색상 선택
        color_todo = st.selectbox(
            "캘린더 표시 색상",
            ["빨간색 (급함)", "파란색 (여유)", "초록색 (제출완료)", "노란색 (준비중)"]
        )
        
        # 색상 매핑
        color_map = {
            "빨간색 (급함)": "#FF6B6B",
            "파란색 (여유)": "#4D96FF",
            "초록색 (제출완료)": "#6BCB77",
            "노란색 (준비중)": "#FFD93D"
        }
        chosen_color = color_map[color_todo]
        
        submit_btn = st.form_submit_button("캘린더에 추가하기")
        
        if submit_btn:
            # 예외 처리: 제목이 비어있거나 날짜가 역전된 경우
            if not subject.strip():
                st.error("과목 및 평가 이름을 입력해주세요!")
            elif start_date > end_date:
                st.error("마감일은 시작일보다 빠를 수 없습니다.")
            else:
                # 💡 FullCalendar 스펙 맞추기: 종료일 하루 더하기 (+1 day)
                # 이렇게 해야 사용자가 선택한 '마감일' 당일까지 달력 막대가 꽉 차게 보입니다.
                actual_end = end_date + timedelta(days=1)
                
                # 캘린더 라이브러리 형식에 맞게 데이터 추가
                new_event = {
                    "title": f"📝 {subject}",
                    "start": start_date.strftime("%Y-%m-%d"),
                    "end": actual_end.strftime("%Y-%m-%d"),
                    "backgroundColor": chosen_color,
                    "borderColor": chosen_color,
                }
                st.session_state["events"].append(new_event)
                st.success(f"'{subject}' 일정이 등록되었습니다!")
                st.rerun() # 화면 즉시 갱신

    st.markdown("---")
    
    # 등록된 일정 목록 확인 및 전체 삭제 기능
    st.subheader("🗑️ 일정 관리")
    if st.session_state["events"]:
        st.write(f"현재 등록된 총 일정: {len(st.session_state['events'])}개")
        if st.button("모든 일정 초기화", type="primary"):
            st.session_state["events"] = []
            st.success("모든 일정이 삭제되었습니다.")
            st.rerun()
    else:
        st.info("등록된 일정이 없습니다. 새로운 일정을 등록해 보세요!")

# --- 오른쪽 달력 영역 ---
with col_calendar:
    st.subheader("🗓️ 수행평가 달력")
    
    # 캘린더 커스텀 옵션 설정 (FullCalendar 기반 옵션)
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek,listMonth",
        },
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": True,
    }
    
    # 대형 달력 컴포넌트 렌더링
    calendar(
        events=st.session_state["events"],
        options=calendar_options,
        key="streamlit_calendar"
    )
