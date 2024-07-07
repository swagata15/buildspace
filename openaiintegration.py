import streamlit as st
import fitz  # PyMuPDF for handling PDFs
import spacy
from openai import OpenAI
import tiktoken 
import time

# Initialize SpaCy model
nlp = spacy.load('en_core_web_sm')

# Set your OpenAI API key
#openai.api_key = 'your-key-here'


# Function to read PDF files
def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

    # Function to count tokens using tiktoken
def count_tokens(text, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return len(tokens)



# Function to extract skills using OpenAI
def extract_skills_with_openai(text):
    token_count = count_tokens(text)
    st.write(f"Token count for resume text: {token_count}")
    
    if token_count > 4096:  # Token limit for gpt-3.5-turbo
        st.error("The resume text is too long for the model to process. Please shorten the resume.")
        return []

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts skills from resumes."},
            {"role": "user", "content": f"Extract the skills from the following resume text:\n{text}"}
        ]
    )
    
    skills = completion.choices[0].message.content.strip().split('\n')
    return skills

# Function to recommend career paths using OpenAI
def recommend_career_with_openai(skills):
    skills_str = ', '.join(skills)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a career advisor."},
            {"role": "user", "content": f"Given the following skills: {skills_str}, recommend some suitable career paths and explain why."}
        ]
    )
    recommendations = completion.choices[0].message.content.strip()
    return recommendations

# Streamlit UI
st.title("AI Career Advisor")
st.write("Upload your resume to get personalized career recommendations.")

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'skills' not in st.session_state:
    st.session_state.skills = []

uploaded_file = st.file_uploader("Choose a file", type=["pdf"], key="unique_file_uploader")

if uploaded_file is not None:
    resume_text = read_pdf(uploaded_file)
    st.session_state.resume_text = resume_text
    st.session_state.skills = extract_skills_with_openai(resume_text)

if st.session_state.resume_text:
    st.write("Resume Text:", st.session_state.resume_text)
    st.write("Extracted Skills:", st.session_state.skills)

    if st.button("Get Career Recommendations", key="unique_recommend_button"):
        recommendations = recommend_career_with_openai(st.session_state.skills)
        st.write("Recommended Career Paths:", recommendations)
