import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

st.title("📄 고용 24 자소서 가이드 기반 AI 자기소개서 작성기")

# 1. OpenAI API 키 입력
api_key = st.text_input("🔑 OpenAI API 키 입력", type="password")
if not api_key:
    st.warning("API 키를 입력해주세요.")
    st.stop()
client = OpenAI(api_key=api_key.strip())

# 2. PDF 업로드 (고용 24 자소서 가이드)
uploaded_file = st.file_uploader("📥 고용 24 자소서 가이드 PDF 업로드", type=["pdf"])

pdf_text = ""
if uploaded_file:
    with st.spinner("PDF 텍스트를 추출하는 중..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pdf_text += page.get_text()
    st.success("PDF 텍스트 추출 완료!")
    st.write("📄 PDF 내용 미리보기:")
    st.text(pdf_text[:1000])  # 앞부분 1000자 미리보기

# 3. 사용자 자기소개서 입력
st.header("✍️ 자기소개서 작성 정보 입력")
company = st.text_input("지원하는 기업명")
reason = st.text_area("1. 지원 동기", height=100)
background = st.text_area("2. 성장 과정", height=100)
experience = st.text_area("3. 직무 관련 경험", height=100)

def generate_cover_letter(api_client, company, reason, background, experience, guide_text):
    # 프롬프트에 고용 24 가이드 내용을 요약해 반영, 자연스러운 에세이 스타일 요청
    prompt = f"""
당신은 취업 자기소개서 작성 전문가입니다.
아래 고용 24 자소서 가이드 내용을 참고하여,
지원 기업 '{company}'에 맞는 자연스럽고 진솔한 에세이 형식 자기소개서를 작성해 주세요.
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

if st.button("🚀 자기소개서 생성"):
    if not (company and reason and background and experience and pdf_text):
        st.error("모든 입력란과 PDF 업로드를 완료해 주세요.")
    else:
        with st.spinner("자기소개서를 작성 중입니다..."):
            cover_letter = generate_cover_letter(client, company, reason, background, experience, pdf_text)
        st.subheader("📄 생성된 자기소개서 (에세이 형식)")
        st.write(cover_letter)
