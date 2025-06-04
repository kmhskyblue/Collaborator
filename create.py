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
    company = st.selectbox("4. 지원 기업", ["삼성전자", "LG전자", "SK하이닉스","현대자동차","기아","카카오","네이버","롯데","포스코","CJ"])

    # 인재상 샘플
    company_values = {
    "삼성전자": ["도전정신", "창의성", "글로벌 역량"],
    "LG전자": ["고객지향", "자율과 책임", "지속적 혁신"],
    "SK하이닉스": ["패기", "협력", "지속가능한 성장"],
    "현대자동차": ["도전", "소통과 협업", "고객 최우선"],
    "기아": ["혁신", "열정", "소통"],
    "카카오": ["유연한 사고", "문제 해결력", "소통 능력"],
    "네이버": ["기술 중심", "자율성", "글로벌 확장"],
    "롯데": ["도전", "창의", "책임감"],
    "포스코": ["고객 중심", "창의와 혁신", "신뢰와 협력"],
    "CJ": ["ONLYONE 정신", "창의성", "열정"],
    "한화": ["신뢰", "도전", "헌신"],
    "대한항공": ["책임감", "정직", "글로벌 역량"],
    "KT": ["도전", "혁신", "고객가치 중심"],
    "LG화학": ["책임감", "협업", "전문성"],
    "NHN": ["협업", "기술 성장", "유연성"],
    "쿠팡": ["고객 집착", "속도", "소유 의식"],
    "토스": ["문제 해결 중심", "책임", "신속한 실행"],
    "배달의민족(우아한형제들)": ["자율", "유쾌함", "사용자 중심"],
    "삼성바이오로직스": ["정직", "혁신", "책임의식"]
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


# ✅ 1. 기업 선택
company = st.selectbox("📌 지원할 기업을 선택하세요", list(company_values.keys()))

# ✅ 2. 해당 기업의 인재상 출력
if company:
    st.markdown(f"### 🏢 {company}의 인재상")
    for v in company_values[company]:
        st.markdown(f"- {v}")
