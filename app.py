import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. 페이지 기본 설정 및 디자인 (Theme)
st.set_page_config(
    page_title="스마트 수행평가 플래너",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 깔끔한 디자인을 위한 커스텀 CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 초기화 (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if 'tasks' not in st.session_state:
    # 기본 예시 데이터 제공
    st.session_state.tasks = pd.DataFrame([
        {"과목": "수학", "수행평가명": "미적분 탐구 보고서", "마감일": date(2026, 7, 5), "중요도": "⭐⭐⭐", "상태": "진행 중"},
        {"과목": "영어", "수행평가명": "영작문 및 발표", "마감일": date(2026, 6, 25), "중요도": "⭐⭐", "상태": "대기 중"},
        {"과목": "과학", "수행평가명": "물리학 실험 결과 요약", "마감일": date(2026, 6, 20), "중요도": "⭐", "상태": "완료"}
    ])

# 페이지 이동 함수
def move_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ------------------------------------------------------------------
# 🏠 1. 메인 페이지
# ------------------------------------------------------------------
if st.session_state.page == 'main':
    st.markdown("<div class='main-title'>📅 스마트 수행평가 플래너</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>수행평가 일정 관리부터 맞춤형 전략 수립까지 한 번에!</div>", unsafe_allow_html=True)
    
    # 앱 기능 설명
    st.markdown("""
    <div class='card'>
        <h4>💡 주요 기능 안내</h4>
        <ul>
            <li><b>📆 수행평가 캘린더:</b> 마감일 순으로 정렬된 수행평가 일정을 확인하고 새 일정을 추가합니다.</li>
            <li><b>⏳ 실시간 디데이:</b> 남은 시간을 직관적으로 확인하고 마감 임박 과제를 놓치지 마세요.</li>
            <li><b>🎯 완벽 대비 전략:</b> 중요도와 난이도에 따른 우선순위 배치 및 과목별 공략 팁을 제공합니다.</li>
            <li><b>📖 수행평가 정보고:</b> 수행평가 고득점을 위한 기본 유의사항과 체크리스트를 확인합니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📍 원하는 페이지로 이동하세요")
    
    # 이동 버튼 배열 (2x2 레이아웃)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📆 수행평가 캘린더 바로가기", use_container_width=True):
            move_to('calendar')
        if st.button("🎯 완벽 대비 전략 바로가기", use_container_width=True):
            move_to('strategy')
            
    with col2:
        if st.button("⏳ 실시간 디데이 바로가기", use_container_width=True):
            move_to('dday')
        if st.button("📖 수행평가 정보고 바로가기", use_container_width=True):
            move_to('info')

# ------------------------------------------------------------------
# 📆 2. 캘린더 & 일정 관리 페이지
# ------------------------------------------------------------------
elif st.session_state.page == 'calendar':
    st.title("📆 수행평가 일정 관리")
    st.caption("새로운 수행평가를 등록하고 전체 일정을 확인하세요.")
    
    # 일정 추가 Form
    with st.expander("➕ 새 수행평가 등록하기", expanded=True):
        with st.form("task_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                subject = st.text_input("과목명 (예: 국어, 수학)", placeholder="과목 입력")
                task_name = st.text_input("수행평가명", placeholder="과제 내용 입력")
            with col2:
                due_date = st.date_input("마감일 선택", value=date.today())
                priority = st.selectbox("중요도", ["⭐", "⭐⭐", "⭐⭐⭐"])
            
            submit = st.form_submit_with_button("등록하기")
            
            if submit:
                if subject and task_name:
                    new_data = pd.DataFrame([{"과목": subject, "수행평가명": task_name, "마감일": due_date, "중요도": priority, "상태": "대기 중"}])
                    st.session_state.tasks = pd.concat([st.session_state.tasks, new_data], ignore_index=True)
                    st.success("🎉 새로운 수행평가가 등록되었습니다!")
                    st.rerun()
                else:
                    st.error("⚠️ 과목명과 수행평가명을 모두 입력해주세요.")

    # 일정 목록 출력 및 수정
    st.subheader("📋 나의 수행평가 리스트")
    if not st.session_state.tasks.empty:
        # 날짜순 정렬
        df_sorted = st.session_state.tasks.sort_values(by="마감일").reset_index(drop=True)
        
        # 데이터프레임 에디터 활용 (상태 변경 및 삭제 가능)
        edited_df = st.data_editor(
            df_sorted,
            column_config={
                "상태": st.column_config.SelectboxColumn("상태", options=["대기 중", "진행 중", "완료"], required=True),
                "마감일": st.column_config.DateColumn("마감일", format="YYYY-MM-DD")
            },
            use_container_width=True,
            num_rows="dynamic"
        )
        st.session_state.tasks = edited_df
        st.caption("💡 표 안의 내용을 더블클릭하여 수정하거나, 행을 선택 후 키보드 Delete 키로 삭제할 수 있습니다.")
    else:
        st.info("등록된 수행평가가 없습니다. 위 양식에서 새로 추가해보세요!")

    if st.button("🏠 메인 페이지로 돌아가기"):
        move_to('main')

# ------------------------------------------------------------------
# ⏳ 3. 디데이 페이지
# ------------------------------------------------------------------
elif st.session_state.page == 'dday':
    st.title("⏳ 실시간 디데이 현황")
    st.caption("마감이 임박한 과제를 확인하고 우선순위를 정해보세요.")
    
    if not st.session_state.tasks.empty:
        today = date.today()
        df = st.session_state.tasks
        
        # 완료된 과제 제외하고 보기 선택
        hide_completed = st.checkbox("완료된 수행평가 숨기기", value=True)
        
        for idx, row in df.iterrows():
            if hide_completed and row['상태'] == '완료':
                continue
                
            d_day = (row['마감일'] - today).days
            
            # 디자인 차별화 (D-Day 상태에 따른 색상 배치)
            if d_day < 0:
                d_day_str = f"❌ 만료 ({abs(d_day)}일 경과)"
                bg_color = "#FEE2E2" # 빨간색 톤
            elif d_day == 0:
                d_day_str = "🚨 D-DAY 바로 오늘!"
                bg_color = "#FEF3C7" # 노란색 톤
            elif d_day <= 3:
                d_day_str = f"🔥 D-{d_day} (마감 임박)"
                bg_color = "#FFEDD5" # 주황색 톤
            else:
                d_day_str = f"📅 D-{d_day}"
                bg_color = "#E0F2FE" # 파란색 톤
                
            st.markdown(f"""
            <div style='background-color: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem; border-left: 6px solid #1E3A8A;'>
                <span style='font-size: 1.2rem; font-weight: bold;'>[{row['과목']}] {row['수행평가명']}</span> 
                <span style='float: right; font-weight: 800; font-size: 1.1rem;'>{d_day_str}</span>
                <br><small>중요도: {row['중요도']} | 상태: {row['상태']} | 마감일: {row['마감일']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("등록된 수행평가 일정이 없습니다.")
        
    if st.button("🏠 메인 페이지로 돌아가기"):
        move_to('main')

# ------------------------------------------------------------------
# 🎯 4. 완벽 대비 전략 페이지
# ------------------------------------------------------------------
elif st.session_state.page == 'strategy':
    st.title("🎯 수행평가 완벽 대비 전략")
    st.caption("효율적인 시간 관리를 위한 맞춤형 전략 매트릭스입니다.")
    
    # 4분면 개념을 차용한 우선순위 추천 자동 기능 (차별화 포인트)
    st.subheader("🚀 시스템 추천 우선순위 가이드")
    st.markdown("> **'중요도가 높고 마감이 임박한 과제'**부터 정렬하여 보여줍니다.")
    
    if not st.session_state.tasks.empty:
        df = st.session_state.tasks.copy()
        today = date.today()
        # 남은 일수 계산
        df['남은일수'] = df['마감일'].apply(lambda x: (x - today).days)
        # 완료 제외
        df = df[df['상태'] != '완료']
        
        # 중요도를 숫자로 치환하여 정렬 우선순위로 사용
        p_map = {"⭐⭐⭐": 3, "⭐⭐": 2, "⭐": 1}
        df['중요도점수'] = df['중요도'].map(p_map)
        
        # 남은일수는 오름차순, 중요도는 내림차순
        df_strat = df.sort_values(by=['남은일수', '중요도점수'], ascending=[True, False])
        
        if not df_strat.empty:
            for idx, row in df_strat.head(3).iterrows():
                st.error(f"⚡ **우선 순위 {idx+1}** : [{row['과목']}] {row['수행평가명']} (남은 일수: {row['남은일수']}일 / 중요도: {row['중요도']})")
        else:
            st.success("👏 현재 마감 대기 중인 급한 과제가 없습니다! 아주 훌륭합니다.")
    else:
        st.info("데이터가 없습니다. 캘린더에서 수행평가를 먼저 등록하세요.")

    st.write("---")
    st.subheader("💡 과목별 유형별 공략 팁")
    
    with st.tabs(["📝 서술형/논술형", "📊 발표/PPT", "🔬 실험/탐구보고서"]):
        with st.tabs[0]:
            st.markdown("""
            * **핵심 키워드 선점:** 출제 의도와 교과서 단원 목표에 나오는 필수 핵심 용어를 반드시 포함하세요.
            * **개요 작성 필수:** 서론-본론-결론의 구조를 미리 짜두고 글을 쓰기 시작해야 논리가 꼬이지 않습니다.
            """)
        with st.tabs[1]:
            st.markdown("""
            * **가독성 중심 PPT:** 한 슬라이드에는 최대 3가지 핵심만 텍스트로 넣고 시각 자료를 활용하세요.
            * **대본 암기보다 흐름 파악:** 대본을 그대로 읽기보다는 슬라이드 키워드를 보고 설명하는 연습을 하세요.
            """)
        with st.tabs[2]:
            st.markdown("""
            * **동기 및 가설 명확화:** 왜 이 실험/탐구를 진행했는지 동기를 뚜렷하게 적어주면 좋은 평가를 받습니다.
            * **오차 분석:** 실험 결과가 실패했더라도 원인을 정확히 분석하고 피드백을 적으면 감점을 방지할 수 있습니다.
            """)

    if st.button("🏠 메인 페이지로 돌아가기"):
        move_to('main')

# ------------------------------------------------------------------
# 📖 5. 수행평가 정보고 (내용을 알려주는 페이지)
# ------------------------------------------------------------------
elif st.session_state.page == 'info':
    st.title("📖 수행평가 정보고")
    st.caption("수행평가에서 절대 놓쳐서는 안 될 기본 규칙들을 확인하세요.")
    
    st.markdown("""
    ### 📌 감점 방지 3대 체크리스트
    1. **⌛ 제출 기한 엄수:** 단 1분이라도 늦으면 학교 규정에 따라 대폭 감점되거나 0점 처리될 수 있으므로 무조건 하루 전 완성을 목표로 합니다.
    2. **📋 평가 기준표(루브릭) 확인:** 선생님이 나누어 주신 유인물의 '상/중/하' 기준표를 정독하고 '상' 조건에 내 과제가 부합하는지 체크하세요.
    3. **🛡️ 표절 및 출처 표기:** 인터넷 검색 내용을 그대로 복사-붙여넣기 하면 표절 검사기에서 적발됩니다. 반드시 본인의 문장으로 재구성하고 출처를 남기세요.
    """)
    
    st.write("---")
    
    # 초보자를 위한 격려 인터랙션 문구
    st.subheader("🍀 오늘의 한 줄 응원")
    quotes = [
        "“미루는 일은 시작을 가장 어렵게 만든다. 지금 바로 시작해봐요!”",
        "“수행평가는 완벽함보다 기한 내 완성이 먼저입니다.”",
        "“하나씩 차근차근 지워나가다 보면 어느새 끝이 보일 거예요.”"
    ]
    import random
    # 세션 내에서 응원 문구가 고정되도록 설정
    if 'quote' not in st.session_state:
        st.session_state.quote = random.choice(quotes)
    st.info(st.session_state.quote)
    
    if st.button("🏠 메인 페이지로 돌아가기"):
        # 돌아갈 때 응원 문구 초기화하여 다음 접속 시 바뀌도록 함
        if 'quote' in st.session_state:
            del st.session_state['quote']
        move_to('main')
