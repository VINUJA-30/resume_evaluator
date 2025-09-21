[Resume Relevance Checker.pdf](https://github.com/user-attachments/files/22450187/Resume.Relevance.Checker.pdf)


problem Statement

Students and job seekers often struggle to align their resumes with job descriptions. Recruiters spend only a few seconds reviewing each resume, making it crucial for candidates to showcase the right skills.

This project helps:

Evaluate the relevance of a resume against a job description.

Identify missing skills, projects, or certifications.

Provide actionable suggestions to improve the resume for better job fit.

Approach

Text Extraction

Resume: PDF or DOCX format.

Job Description: PDF, TXT, or direct text input.

Extracts text using pdfplumber and docx2txt.

Semantic Similarity

Uses SentenceTransformer (all-MiniLM-L6-v2) to convert text into embeddings.

Computes similarity between resume and job description.

Missing Skills Detection

Compares resume text with a predefined list of important skills (Python, Java, SQL, AWS, Machine Learning, etc.).

Highlights skills present in the JD but missing in the resume.

Suggestions Generation

Provides personalized improvement suggestions based on missing skills.

Tips include working on projects, certifications, coding challenges, and LinkedIn profile updates.

Frontend UI

Built with Streamlit.

Interactive dashboard with color-coded results, progress bar, and badges.

Allows JD to be uploaded or entered directly.

Installation Steps

Clone the repository

git clone https://github.com/<your-username>/resume-relevance-checker.git
cd resume-relevance-checker


Create a virtual environment (optional but recommended)

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install required packages

pip install -r requirements.txt


Run the Streamlit app

streamlit run app.py

Requirements

Python 3.8+

Streamlit

pdfplumber

docx2txt

sentence-transformers

numpy

Install all dependencies using:

pip install -r requirements.txt
