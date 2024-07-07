import streamlit as st
import fitz  # PyMuPDF for handling PDFs
import spacy

# Initialize SpaCy model
nlp = spacy.load('en_core_web_sm')

# Function to read PDF files
def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


# Function to parse resume and extract skills
def parse_resume(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
    return skills

# Function to recommend career paths based on skills
def recommend_career(skills):
    career_paths = {
        "Data Scientist": ["Python", "Machine Learning", "Data Analysis"],
        "Software Engineer": ["Java", "System Design", "Algorithms"],
        "Project Manager": ["Leadership", "Communication", "Agile"]
    }
    recommendations = []
    for career, req_skills in career_paths.items():
        match = len(set(skills) & set(req_skills))
        if match > 0:
            recommendations.append((career, match))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [rec[0] for rec in recommendations]

# Streamlit UI
st.title("AI Career Advisor")
st.write("Upload your resume to get personalized career recommendations.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        resume_text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = read_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        resume_text = read_txt(uploaded_file)
    else:
        st.error("Unsupported file type.")
        resume_text = None

    if resume_text:
        st.write("Resume Text:", resume_text)

        skills = parse_resume(resume_text)
        st.write("Extracted Skills:", skills)

        if st.button("Get Career Recommendations"):
            recommendations = recommend_career(skills)
            st.write("Recommended Career Paths:", recommendations)
