import streamlit as st
import fitz  # PyMuPDF for handling PDFs
import requests
import os

# Function to read PDF files
def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract skills using Gemini AI Studio API
def extract_skills_with_gemini_api(text, api_key):
    endpoint = "https://geminiapi.com/extract-skills"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        skills = response.json().get("skills", [])
        return skills
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to extract skills: {str(e)}")
        return []

# Function to recommend career paths using Gemini AI Studio API
def recommend_career_with_gemini_api(skills, api_key):
    endpoint = "https://geminiapi.com/recommend-careers"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "skills": skills
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        recommendations = response.json().get("recommendations", "")
        return recommendations
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to recommend career paths: {str(e)}")
        return ""

# Streamlit UI
st.set_page_config(
    page_title="AI Career Advisor with Gemini AI Studio",
    page_icon=":gemini:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles for the application
st.markdown(
    """
    <style>
    .full-width {
        width: 100%;
        margin: auto;
    }
    .highlight-text {
        color: #0066CC;
        font-weight: bold;
    }
    .button-primary {
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .button-primary:hover {
        background-color: #0052a3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content of the application
st.title("AI Career Advisor with Gemini AI Studio")
st.markdown(
    """
    Upload your resume to get personalized career recommendations using Gemini AI Studio.
    """
)

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'skills' not in st.session_state:
    st.session_state.skills = []

# File uploader and processing logic
uploaded_file = st.file_uploader("Choose a file (PDF format)", type=["pdf"], key="unique_file_uploader")

if uploaded_file is not None:
    resume_text = read_pdf(uploaded_file)
    st.session_state.resume_text = resume_text
    api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual environment variable name
    st.session_state.skills = extract_skills_with_gemini_api(resume_text, api_key)

# Display resume text and extracted skills
if st.session_state.resume_text:
    st.subheader("Resume Text:")
    st.write(st.session_state.resume_text)
    st.subheader("Extracted Skills:")
    st.write(", ".join(st.session_state.skills))

    # Button for generating recommendations
    button_col1, button_col2, button_col3 = st.columns(3)
    with button_col2:
        if st.button("Get Career Recommendations", key="unique_recommend_button"):
            with st.spinner('Analyzing skills and generating recommendations...'):
                api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual environment variable name
                recommendations = recommend_career_with_gemini_api(st.session_state.skills, api_key)
                st.subheader("Recommended Career Paths:")
                st.write(recommendations)

