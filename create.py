# streamlit_app.py

import streamlit as st
import openai

# 🔑 OpenAI API Key 설정
openai.api_key = "your-openai-api-key"

# 🎯 기업 인재상 예시 데이터
company_values = {
    "삼성전자": ["도전정신", "창의성", "글로벌 역량"],
    "카카오": ["유연한 사고", "문제해결력", "소통 능력"],
    "LG화학": ["책임감", "협업", "전문성"]
}

# 🧠 GPT 활용 함수
import streamlit as st
from openai import OpenAI

# 최신 방식: OpenAI 인스턴스 생성
client = OpenAI(api_key="your-openai-api-key")

def generate_cover_letter(reason, background, experience, company):
    value_keywords = ", ".join(company_values.get(company, []))
    prompt = f"""
    아래 내용을 기반으로 지원 기업({company})의 인재상({value_keywords})을 반영한 자기소개서를 작성해줘.

    [지원동기]
    {reason}

    [성장과정]
    {background}

    [직무 관련 경험]
    {experience}

    형식은 항목별 문단 구성으로 해줘.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_interview_questions(reason, background, experience, company):
    prompt = f"""
    아래 정보를 바탕으로 지원자가 받을 수 있는 면접 예상 질문 5개를 생성해줘.

    지원 기업: {company}
    지원동기: {reason}
    성장과정: {background}
    직무 관련 경험: {experience}

    형식: 번호를 매겨서 간단하게 출력해줘.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# 🚀 Streamlit UI
st.title("AI 자소서 생성기 + 면접 질문 예측")

reason = st.text_area("1. 지원 동기")
background = st.text_area("2. 성장 과정")
experience = st.text_area("3. 직무 관련 경험")
company = st.selectbox("4. 지원 기업", ["삼성전자", "카카오", "LG화학"])

if st.button("자기소개서 및 면접 질문 생성"):
    with st.spinner("AI가 자소서를 작성 중입니다..."):
        cover_letter = generate_cover_letter(reason, background, experience, company)
        questions = generate_interview_questions(reason, background, experience, company)

    st.subheader("📄 생성된 자기소개서")
    st.write(cover_letter)

    st.subheader("🎤 예상 면접 질문")
    st.write(questions)
