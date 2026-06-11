import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="공부 계획 도우미 챗봇", page_icon="📅", layout="centered")

st.title("📅 AI 공부 계획 도우미")
st.caption("목표하는 시험이나 과목을 알려주시면 체계적인 공부 계획을 세워드려요!")

# 1. Streamlit Secrets에서 API 키 불러오기 및 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리자 설정을 확인해주세요.")
    st.stop()

# 2. 채팅 기록(Session State) 초기화
if "messages" not in st.session_state:
    # 챗봇에게 '공부 계획 플래너'라는 페르소나를 부여하는 시스템 지침(System Instruction) 설정
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 어떤 과목이나 시험을 준비하시나요? 목표 기간과 하루 공부 가능 시간을 알려주시면 맞춤형 계획을 세워드릴게요! ✍️"
        }
    ]

# 3. 기존 채팅 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. 사용자 입력 받기
if user_input := st.chat_input("예: 고1 수학 기말고사 3주 계획 짜줘"):
    
    # 사용자 메시지 화면 표시 및 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 응답 생성 과정에서의 예외 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("생각 중... 🤔"):
                # gemini-2.5-flash-lite 모델 호출
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction="당신은 학생들의 학습을 돕는 친절하고 체계적인 '공부 계획 설정 플래너'입니다. 학습 목표, 기간, 하루 공부 시간을 파악하여 구체적이고 실행 가능한 주간/일일 계획을 표나 불릿포인트로 정리해 주세요."
                )
                
                # 대화 맥락 유지를 위해 기존 기록을 대화 형태로 가공 (텍스트 기반)
                # (주석: 보다 완벽한 대화 관리를 위해 간단한 string format 구조를 채택했습니다)
                chat_history = ""
                for msg in st.session_state.messages[:-1]: # 현재 입력 제외한 이전 기록
                    prefix = "User: " if msg["role"] == "user" else "Assistant: "
                    chat_history += f"{prefix}{msg['content']}\n"
                chat_history += f"User: {user_input}\nAssistant: "

                # 모델 응답 생성
                response = model.generate_content(chat_history)
                ai_response = response.text
                
                # 화면에 부드럽게 출력 및 저장
                message_placeholder.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
        except genai.types.generation_types.BlockedPromptException:
            message_placeholder.error("🚫 안전 정책에 의해 차단된 요청입니다. 다른 질문을 입력해주세요.")
        except Exception as e:
            message_placeholder.error(f"❌ 오류가 발생했습니다: {str(e)}\n잠시 후 다시 시도해주세요.")
