import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="나만의 AI 비서", page_icon="📝", layout="wide")

# 사이드바 설정 (API 키 입력 및 가이드)
with st.sidebar:
    st.title("⚙️ 설정 및 안내")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.markdown("---")
    st.info("💡 **팁:** 폰으로 접속할 때도 이 키만 입력하면 어디서든 사용할 수 있어요.")

# 결과 저장을 위한 세션 상태 초기화
if 'result' not in st.session_state:
    st.session_state.result = ""

# 메인 UI
st.title("🕵️‍♂️ 지능형 정보 분석 & 작성 서비스")
st.write("주제와 일자를 정해주시면 자료 검색부터 분석, 스스로 검증까지 수행합니다.")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("무엇에 대해 알아볼까요? (주제 입력)", placeholder="예: 2026년 하반기 배터리 산업 전망")
    target_date = st.date_input("기준 일자", datetime.now())
    direction = st.text_area("방향 및 요청사항", placeholder="예: 유튜브 숏츠용으로 작성해줘, 혹은 베이킹 레시피 분석해줘", height=150)
    
    if st.button("🚀 분석 및 작성 시작", use_container_width=True):
        if not api_key:
            st.warning("API 키를 먼저 입력해주세요!")
        elif not topic:
            st.warning("주제를 입력해주세요!")
        else:
            with st.spinner("최신 자료를 검색하고 스스로 반론을 제기하며 검증 중..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro",
                        tools=[{"google_search_retrieval": {}}]
                    )
                    
                    # 사용자 맞춤형 지시사항 포함
                    prompt = f"""
                    날짜: {target_date}
                    주제: {topic}
                    요청: {direction}
                    
                    [필수 수행 지침]
                    1. Google Search를 통해 최신 정보를 검색하고 분석할 것.
                    2. 작성 시 다음의 규칙을 반드시 따를 것:
                       - 유튜브 관련 요청 시: 제목 후보, 요약 레시피/내용, 해시태그, 댓글용 문구 포함.
                       - 베이킹 관련 요청 시: 상세 공정, 실수 대응 팁, 베이커스 퍼센트, 정밀 수분율 포함.
                       - 정보성 글: 스스로의 논리에 반론을 제기하고 재검증하여 최선의 결과를 도출할 것.
                    3. 불필요한 직업 노출 용어(조종사 등)는 절대 사용 금지.
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.result = response.text
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

with col2:
    st.subheader("✅ 최종 분석 결과")
    if st.session_state.result:
        st.markdown(st.session_state.result)
        
        # 파일 저장 기능 (마크다운 형식)
        st.download_button(
            label="💾 분석 결과 파일로 저장",
            data=st.session_state.result,
            file_name=f"{topic}_{target_date}.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("분석이 완료되면 여기에 내용이 표시됩니다.")
