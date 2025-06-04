import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="AI 자기소개서 작성기", layout="wide")

st.title("🤖 AI 자기소개서 & 면접질문 생성기")

# 1. OpenAI API 키 입력
api_key = st.text_input("🔑 OpenAI API 키 입력", type="password")
if not api_key:
    st.warning("API 키를 입력해주세요.")
    st.stop()
client = OpenAI(api_key=api_key.strip())

# 2. 기업별 인재상 데이터
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
    "배달의민족": ["자율", "유쾌함", "사용자 중심"],
    "삼성바이오로직스": ["정직", "혁신", "책임의식"]
}

# 3. PDF 업로드 (고용 24 자소서 가이드)
uploaded_file = st.file_uploader("📥 고용 24 자소서 가이드 PDF 업로드", type=["pdf"])

pdf_text = ""
if uploaded_file:
    with st.spinner("PDF 텍스트 추출 중..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pdf_text += page.get_text()
    st.success("PDF 텍스트 추출 완료!")
    st.markdown("### 📄 PDF 내용 일부 미리보기")
    st.text(pdf_text[:1000])

# 4. 지원 기업 선택
company = st.selectbox("📌 지원 기업을 선택하세요", list(company_values.keys()))

# 5. 인재상 표시
if company:
    st.markdown(f"### 🏢 {company} 인재상")
    for v in company_values[company]:
        st.markdown(f"- {v}")

# 6. 자기소개서 입력
st.header("✍️ 자기소개서 작성 정보 입력")
reason = st.text_area("1. 지원 동기", height=100)
background = st.text_area("2. 성장 과정", height=100)
experience = st.text_area("3. 직무 관련 경험", height=100)

def generate_cover_letter(api_client, company, reason, background, experience, guide_text, values):
    prompt = f"""
당신은 취업 자기소개서 작성 전문가입니다.
아래 고용 24 자소서 가이드 내용을 참고하여,
지원 기업 '{company}' 인재상 {values} 을 반영한
자연스럽고 진솔한 에세이 형식 자기소개서를 작성해 주세요.
각 항목을 하나의 문단으로 작성하고, 문단 간 연결 문장으로 부드럽게 이어주세요.

[고용 24 자소서 가이드 주요 내용]
{guide_text[:3000]}

[지원 동기]
{reason}

[성장 과정]
{background}

[직무 경험]
{experience}
"""
    response = api_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def generate_interview_questions(api_client, company):
    prompt = f"""
지원 기업 '{company}'와 관련된 자기소개서에 기초한 예상 면접 질문 5개를 작성해 주세요.
"""
    response = api_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def create_pdf(text, filename="자기소개서.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)  # 한글폰트 필요
    pdf.set_font('NanumGothic', '', 12)
    lines = text.split('\n')
    for line in lines:
        pdf.cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

if st.button("🚀 자기소개서 & 면접 질문 생성"):
    if not (company and reason and background and experience and pdf_text):
        st.error("모든 입력란과 PDF 업로드를 완료해 주세요.")
    else:
        with st.spinner("자기소개서 작성 중..."):
            cover_letter = generate_cover_letter(client, company, reason, background, experience, pdf_text, company_values[company])
        with st.spinner("면접 예상 질문 생성 중..."):
            interview_questions = generate_interview_questions(client, company)

        st.subheader("📄 생성된 자기소개서 (에세이 형식)")
        st.write(cover_letter)

        st.subheader("❓ 예상 면접 질문 5개")
        st.write(interview_questions)

        # PDF 다운로드 버튼
        pdf_file = create_pdf(cover_letter)
        st.download_button(
            label="📥 자기소개서 PDF 다운로드",
            data=pdf_file,
            file_name=f"{company}_자기소개서.pdf",
            mime="application/pdf"
        )
