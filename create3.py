import streamlit as st
from openai import OpenAI

st.title("🧠 AI 자기소개서 생성기")

# 1️⃣ API 키 입력 받기
api_key = st.text_input("🔑 OpenAI API 키를 입력하세요:", type="password")

# 키가 입력되어야 작동하도록 조건 처리
if api_key:
    client = OpenAI(api_key=api_key)

    # 자소서 입력 UI
    reason = st.text_area("1. 지원 동기")
    background = st.text_area("2. 성장 과정")
    experience = st.text_area("3. 직무 관련 경험")
    company = st.selectbox("4. 지원 기업", ["삼성전자", "카카오", "LG화학"])

    # 인재상 샘플
    company_values = {
        "삼성전자": ["도전정신", "창의성", "글로벌 역량"],
        "카카오": ["유연한 사고", "문제해결력", "소통 능력"],
        "LG화학": ["책임감", "협업", "전문성"]
    }

    def generate_cover_letter():
        value_keywords = ", ".join(company_values.get(company, []))
        prompt = f"""
        아래 내용을 기반으로 {company} 인재상({value_keywords})을 반영한 자기소개서를 작성해줘.

        [지원동기] {reason}
        [성장과정] {background}
        [직무경험] {experience}

        항목별 문단으로 구성해줘.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def generate_interview_questions():
        prompt = f"""
        다음 정보를 바탕으로 예상 면접 질문 5개를 생성해줘.

        [지원 기업]: {company}
        [지원 동기]: {reason}
        [성장 과정]: {background}
        [직무 경험]: {experience}
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()

    if st.button("🚀 자기소개서 및 질문 생성"):
        with st.spinner("AI가 자소서를 작성 중입니다..."):
            cover_letter = generate_cover_letter()
            questions = generate_interview_questions()

        st.subheader("📄 생성된 자기소개서")
        st.write(cover_letter)

        st.subheader("🎤 예상 면접 질문")
        st.write(questions)
else:
    st.warning("⚠️ OpenAI API 키를 입력해 주세요.")
