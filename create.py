import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
from pptx import Presentation
import re

st.set_page_config(
    page_title="CoverCraft | AI Cover Letter Generator",
    page_icon="🧑\u200d💼",
    layout="wide"
)

st.title("🧑\u200d💼 CoverCraft | AI Cover Letter Generator")

# OpenAI API Key
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()
client = OpenAI(api_key=api_key)

# Company values
company_values = {
    "Samsung Electronics": ["Challenge Spirit", "Creativity", "Global Competence"],
    "LG Electronics": ["Customer Orientation", "Responsibility", "Continuous Innovation"],
    "SK Hynix": ["Passion", "Cooperation", "Sustainable Growth"],
    # Add others as needed
}

company = st.selectbox("📊 Select Your Target Company", list(company_values.keys()))
if company:
    st.markdown(f"#### 🏢 {company} Core Values")
    st.markdown("".join([f"- {v}\n" for v in company_values[company]]))

st.divider()

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload your resume or reference (PDF or PPTX)", type=["pdf", "pptx"])
with col2:
    user_extra_text = st.text_area("Optional: Additional details to consider", height=150)

pdf_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                pdf_text += page.get_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        prs = Presentation(uploaded_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    pdf_text += shape.text + "\n"

st.divider()

st.subheader("📋 Cover Letter Inputs")
reason = st.text_area("1. Why do you want to join this company?", height=100)
background = st.text_area("2. Tell us about your personal growth story.", height=100)
experience = st.text_area("3. Share a relevant experience for this role.", height=100)

# Cover letter generator
def generate_cover_letter(reason, background, experience, company, pdf_text="", user_text=""):
    traits = ", ".join(company_values[company])
    prompt = f"""
Write a sincere and natural essay-style cover letter based on the following inputs.
Each point should be a paragraph, and the transitions should flow naturally.
Avoid robotic or overly formal language; include emotion and personal stories.

[Target Company]: {company}
[Company Core Values]: {traits}

[Motivation to Apply]
{reason}

[Personal Growth]
{background}

[Relevant Experience]
{experience}
"""
    if pdf_text.strip():
        prompt += f"\n[Resume Excerpt]\n{pdf_text.strip()}"
    if user_text.strip():
        prompt += f"\n[User Additional Notes]\n{user_text.strip()}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# Interview Q&A generator
def generate_questions_and_answers(cover_letter_text, company):
    prompt = f"""
Based on the following cover letter for {company}, generate 5 possible interview questions and model answers.
Format:
Q1. ...
A1. ...

Q2. ...
A2. ...

[Cover Letter]
{cover_letter_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# QA parser
def parse_questions_and_answers(text):
    qa_pairs = []
    pattern = re.compile(r"Q\d+\.\s*(.*?)\nA\d+\.\s*(.*?)(?=\nQ\d+\.|\Z)", re.DOTALL)
    matches = pattern.findall(text)
    for q, a in matches:
        qa_pairs.append((q.strip(), a.strip()))
    return qa_pairs

# Generate button
if st.button("🚀 Generate Cover Letter & Interview Questions"):
    if not (reason and background and experience):
        st.error("Please fill in all cover letter input fields.")
    else:
        with st.spinner("Creating your cover letter..."):
            cover_letter = generate_cover_letter(reason, background, experience, company, pdf_text, user_extra_text)
        st.subheader("🔔 Generated Cover Letter")
        st.write(cover_letter)
        st.download_button("📄 Download Cover Letter", cover_letter, file_name="cover_letter.txt")

        with st.spinner("Generating interview questions and answers..."):
            raw_qna = generate_questions_and_answers(cover_letter, company)
            qa_pairs = parse_questions_and_answers(raw_qna)

        st.subheader("💬 Interview Practice: Questions & Model Answers")
        for i, (q, a) in enumerate(qa_pairs):
            st.markdown(f"**Q{i+1}. {q}**")
            st.markdown(f":green[A{i+1}. {a}]")
            st.markdown("---")
