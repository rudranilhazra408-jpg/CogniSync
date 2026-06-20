import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2  # New import for reading PDFs

# 1. Initialize and Load API Keys
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("🔒 Environment Error: GEMINI_API_KEY not found in .env file.")

# 2. Configure the Web Layout
st.set_page_config(page_title="CogniSync AI", page_icon="🧠", layout="centered")

st.title("🧠 CogniSync Multi-Agent System")
st.markdown("##### *Autonomous Multi-Agent Architecture for Competitive Examination Mastery*")
st.divider()

# --- NEW: PDF Processing Function ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# 3. Sidebar Knowledge Base (Upgraded to File Uploader)
with st.sidebar:
    st.header("📂 Local Knowledge Base")
    st.write("Upload your PDF study materials or syllabus chapters below:")
    
    uploaded_file = st.file_uploader("Upload PDF Syllabus", type=['pdf'])
    
    # Store the extracted text in a variable
    syllabus_context = ""
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            syllabus_context = extract_text_from_pdf(uploaded_file)
            st.success(f"Successfully processed: {uploaded_file.name}")
            with st.expander("Preview Extracted Text"):
                st.caption(syllabus_context[:500] + "... [Text Truncated]")
    else:
        st.info("Awaiting file upload...")

# 4. Main Control Dashboard
st.write("### 🤖 Multi-Agent Orchestration Panel")
st.write("The Academic Supervisor is standing by. Choose an autonomous agent to deploy:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎓 Deploy Tutor Agent", use_container_width=True):
        if not syllabus_context:
            st.warning("Please upload a PDF document in the sidebar first.")
        else:
            with st.spinner("Tutor Agent formulating deep conceptual questions..."):
                try:
                    prompt = f"""
                    You are an elite academic tutor specializing in engineering competitive exams. 
                    Based on the following extracted PDF context, generate 1 advanced, highly conceptual practice problem followed by a fully detailed, step-by-step mathematical derivation solution.
                    
                    PDF Context:
                    {syllabus_context}
                    """
                    response = model.generate_content(prompt)
                    st.info("### 📝 Tutor Agent Analysis")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Execution failed: {e}")

with col2:
    if st.button("📅 Deploy Planner Agent", use_container_width=True):
        if not syllabus_context:
            st.warning("Please upload a PDF document in the sidebar first.")
        else:
            with st.spinner("Planner Agent calculating high-intensity countdown milestones..."):
                try:
                    prompt = f"""
                    You are an elite academic architect and time-management expert for high-stakes engineering exams. 
                    Based on the following extracted PDF context, design an optimized, high-intensity weekly revision countdown schedule, daily time allotment strategy, and specific mastery milestones.
                    
                    PDF Context:
                    {syllabus_context}
                    """
                    response = model.generate_content(prompt)
                    st.success("### 📅 Planner Agent Schedule")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Execution failed: {e}")