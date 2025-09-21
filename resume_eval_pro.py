import streamlit as st
import pdfplumber
import docx2txt
from sentence_transformers import SentenceTransformer
import numpy as np

# ---- Predefined list of important skills ----
important_skills = [
    "python", "java", "c++", "c#", "sql", "nosql", "javascript", "html", "css",
    "react", "angular", "node.js", "django", "flask", "spring", "aws", "azure",
    "docker", "kubernetes", "machine learning", "deep learning", "nlp", "pandas",
    "numpy", "tensorflow", "pytorch", "git", "github", "excel", "tableau", "power bi"
]

# ---- Page Config ----
st.set_page_config(page_title="Resume Relevance Checker", layout="wide")
st.title("📄 Resume Relevance Checker")
st.write("Upload a **Resume** and provide a **Job Description (Text/PDF)** to check relevance.")

# ---- Sidebar ----
st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=120)
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark", "Colorful"])

# ---- Load Sentence Transformer Model ----
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ---- Text Extraction ----
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

# ---- Semantic Similarity ----
def compute_similarity(resume_text, jd_text):
    resume_emb = model.encode([resume_text])[0]
    jd_emb = model.encode([jd_text])[0]
    similarity = np.dot(resume_emb, jd_emb) / (np.linalg.norm(resume_emb) * np.linalg.norm(jd_emb))
    return round(similarity * 100, 2)

# ---- Missing Skills (based only on predefined skills list) ----
def get_missing_skills(resume_text, jd_text):
    resume_text_lower = resume_text.lower()
    jd_text_lower = jd_text.lower()
    jd_skills = [skill for skill in important_skills if skill in jd_text_lower]
    missing_skills = [skill for skill in jd_skills if skill not in resume_text_lower]
    return missing_skills

# ---- Streamlit UI ----
resume_file = st.file_uploader("📑 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

st.write("### 📝 Job Description")
jd_file = st.file_uploader("Upload Job Description (TXT/PDF)", type=["txt", "pdf"])
jd_text_input = st.text_area("Or paste Job Description text here:")

if st.button("🚀 Evaluate Relevance"):
    if resume_file and (jd_file or jd_text_input.strip()):
        # Extract resume text
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        # Extract JD text
        jd_text = ""
        if jd_file:
            if jd_file.type == "application/pdf":
                jd_text = extract_text_from_pdf(jd_file)
            elif jd_file.type == "text/plain":
                jd_text = jd_file.read().decode("utf-8")
        elif jd_text_input.strip():
            jd_text = jd_text_input.strip()

        # Compute similarity score
        score = compute_similarity(resume_text, jd_text)

        # Verdict
        if score >= 75:
            verdict = "High"
        elif score >= 50:
            verdict = "Medium"
        else:
            verdict = "Low"

        # Missing skills
        missing_skills = get_missing_skills(resume_text, jd_text)

        # ---- Final Structured Output ----
        st.subheader("📊 Result")

        # Score with progress bar
        st.write("**Relevance Score (0–100):**")
        st.progress(int(score))
        st.markdown(f"<h3 style='color:#2E86C1;'>🎯 {score}%</h3>", unsafe_allow_html=True)

        # Verdict with colors
        if verdict == "High":
            st.markdown(f"<h4 style='color:green;'>✅ Verdict: {verdict} Suitability</h4>", unsafe_allow_html=True)
        elif verdict == "Medium":
            st.markdown(f"<h4 style='color:orange;'>⚠️ Verdict: {verdict} Suitability</h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4 style='color:red;'>❌ Verdict: {verdict} Suitability</h4>", unsafe_allow_html=True)

        # Missing Skills
        st.write("**Missing Skills/Projects/Certifications:**")
        if missing_skills:
            st.error(", ".join(missing_skills))
        else:
            st.success("None – your resume covers most required skills!")

        # Suggestions with improvements
        if missing_skills:
            suggestions = f"💡 Improve your skills in: {', '.join(missing_skills)}.\n\n"
            suggestions += "📌 Additional tips to boost your profile:\n"
            suggestions += "- Work on real-world projects and upload them to GitHub.\n"
            suggestions += "- Earn certifications (AWS, Azure, Tableau, etc.).\n"
            suggestions += "- Practice coding challenges on platforms like LeetCode/HackerRank.\n"
            suggestions += "- Build a strong LinkedIn profile highlighting your skills.\n"
            suggestions += "- Stay updated with latest technologies and frameworks."
        else:
            suggestions = "✅ Your resume already covers most of the required skills. Keep learning and building projects!"

        st.info(suggestions)

    else:
        st.warning("⚠️ Please upload both Resume and Job Description (file or text).")
