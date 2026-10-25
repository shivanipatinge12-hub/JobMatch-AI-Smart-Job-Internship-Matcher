import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import io
import re


# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Smart Job Matcher",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Smart Job & Internship Matcher")

st.markdown(
    "Upload your resume to find matching jobs, identify your "
    "technical skills, and discover skills you may need to develop."
)

# 2. TECHNICAL SKILLS DICTIONARY
SKILLS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "Oracle": ["oracle"],
    "PL/SQL": ["pl/sql", "plsql"],
    "C": ["c programming", "programming in c"],
    "Java": ["java"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "Streamlit": ["streamlit"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Keras": ["keras"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Natural Language Processing": [
        "natural language processing",
        "nlp"
    ],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Microsoft Excel": ["microsoft excel", "ms excel", "excel"],
    "Statistics": ["statistics", "statistical analysis"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Visualization": ["data visualization"],
    "Data Cleaning": ["data cleaning", "data cleansing"],
    "Data Preprocessing": ["data preprocessing"],
    "Computer Vision": ["computer vision"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "Selenium": ["selenium"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi", "fast api"],
    "REST API": ["rest api", "restful api"],
    "Data Structures": ["data structures"],
    "OOP": ["object-oriented programming", "oops", "oop"],
    "Problem Solving": ["problem solving"]
}


# 3. EXTRACT SKILLS FROM TEXT
def extract_skills(text):
    """
    Identify known technical skills mentioned in text.
    Returns a list of detected skills.
    """

    if not text:
        return []

    detected_skills = []
    text_lower = text.lower()

    for skill, variations in SKILLS.items():

        for variation in variations:

            # Match whole words to reduce false matches.
            pattern = (
                r"(?<!\w)"
                + re.escape(variation.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                detected_skills.append(skill)
                break

    return detected_skills


# 4. EXTRACT TEXT FROM PDF
def extract_text_from_pdf(uploaded_file):

    try:
        pdf_reader = PdfReader(
            io.BytesIO(uploaded_file.getvalue())
        )

        if pdf_reader.is_encrypted:
            st.error(
                "This PDF is password-protected. "
                "Please upload an unprotected PDF."
            )
            return ""

        extracted_text = []

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text.append(page_text)

        return " ".join(extracted_text).strip()

    except Exception as error:
        st.error(f"Error reading PDF: {error}")
        return ""

# 5. LOAD JOBS DATASET
try:
    jobs_df = pd.read_csv("jobs.csv")

    required_columns = [
        "Title",
        "Company",
        "Description"
    ]

    if not all(
        column in jobs_df.columns
        for column in required_columns
    ):
        st.error(
            "jobs.csv must contain these columns: "
            "Title, Company, Description."
        )
        st.stop()

    jobs_df = jobs_df.dropna(
        subset=required_columns
    ).copy()

    for column in required_columns:
        jobs_df[column] = (
            jobs_df[column].astype(str).str.strip()
        )

    for column in required_columns:
        jobs_df = jobs_df[
            jobs_df[column] != ""
        ]

    if jobs_df.empty:
        st.error("No valid job listings were found in jobs.csv.")
        st.stop()

except FileNotFoundError:
    st.error(
        "jobs.csv was not found. Put it in the same folder "
        "as app.py."
    )
    st.stop()

except pd.errors.EmptyDataError:
    st.error("jobs.csv is empty. Please add job listings.")
    st.stop()

except pd.errors.ParserError:
    st.error("Could not read jobs.csv. Check its CSV formatting.")
    st.stop()


# 6. SIDEBAR: RESUME UPLOAD
st.sidebar.header("📋 Candidate Portal")

uploaded_file = st.sidebar.file_uploader(
    "Upload your Resume (PDF format)",
    type=["pdf"]
)



# 7. PROCESS RESUME

if uploaded_file is not None:

    st.sidebar.success("Resume uploaded successfully!")

    with st.spinner("Analyzing your resume..."):

        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:

            st.warning(
                "No readable text was extracted. "
                "Please upload a text-based PDF resume."
            )

        else:

            
            # A. EXTRACT RESUME SKILLS
            
            resume_skills = extract_skills(resume_text)

            st.subheader("🧑‍💻 Skills Found in Your Resume")

            if resume_skills:
                st.write(
                    ", ".join(resume_skills)
                )
            else:
                st.warning(
                    "No recognized skills were detected. "
                    "Check whether your resume contains readable "
                    "text and skills from the supported skill list."
                )

            st.divider()


            # B. EXTRACT SKILLS FROM EACH JOB
        
            results_df = jobs_df.copy()

            results_df["Job Skills"] = results_df[
                "Description"
            ].apply(extract_skills)

            
            # C. FIND MATCHING AND MISSING SKILLS
            resume_skill_set = set(resume_skills)

            results_df["Matching Skills"] = (
                results_df["Job Skills"].apply(
                    lambda job_skills: [
                        skill for skill in job_skills
                        if skill in resume_skill_set
                    ]
                )
            )

            results_df["Missing Skills"] = (
                results_df["Job Skills"].apply(
                    lambda job_skills: [
                        skill for skill in job_skills
                        if skill not in resume_skill_set
                    ]
                )
            )

            
            # D. CALCULATE TEXT SIMILARITY

            # Include job titles as well as descriptions.
            job_documents = (
                results_df["Title"]
                + " "
                + results_df["Description"]
            ).tolist()

            all_documents = [resume_text] + job_documents

            try:

                vectorizer = TfidfVectorizer(
                    stop_words="english"
                )

                tfidf_matrix = vectorizer.fit_transform(
                    all_documents
                )

                resume_vector = tfidf_matrix[0]
                job_vectors = tfidf_matrix[1:]

                similarity_scores = cosine_similarity(
                    resume_vector,
                    job_vectors
                ).flatten()

                results_df["Match Score (%)"] = [
                    round(float(score) * 100, 1)
                    for score in similarity_scores
                ]

            except ValueError:

                st.error(
                    "Unable to calculate text similarity. "
                    "Please check the text in your resume and jobs.csv."
                )
                st.stop()

            
            # E. RANK THE TOP FIVE JOBS
           
            results_df = results_df.sort_values(
                by="Match Score (%)",
                ascending=False
            )

            top_jobs = results_df.head(5)


            # F. DISPLAY BEST MATCH
        
            st.subheader("🎯 Your Top Job Matches")

            best_match = top_jobs.iloc[0]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Best Matching Role",
                best_match["Title"]
            )

            col2.metric(
                "Company",
                best_match["Company"]
            )

            col3.metric(
                "Text Similarity",
                f'{best_match["Match Score (%)"]}%'
            )

            st.divider()

            
            # G. DISPLAY JOB RECOMMENDATIONS
          
            for index, (_, job) in enumerate(
                top_jobs.iterrows(),
                start=1
            ):

                with st.expander(
                    f"{index}. {job['Title']} — "
                    f"{job['Match Score (%)']}% text similarity",
                    expanded=(index == 1)
                ):

                    st.write(
                        f"**Company:** {job['Company']}"
                    )

                    st.write("**Job Description:**")
                    st.write(job["Description"])

                    st.write("**✅ Matching Skills:**")

                    if job["Matching Skills"]:
                        st.success(
                            ", ".join(job["Matching Skills"])
                        )
                    else:
                        st.info(
                            "No matching skills from the "
                            "supported skill list were detected."
                        )

                    st.write("**📚 Skills to Develop:**")

                    if job["Missing Skills"]:
                        st.warning(
                            ", ".join(job["Missing Skills"])
                        )
                    else:
                        st.success(
                            "All recognized skills mentioned "
                            "in this job description were found "
                            "in your resume."
                        )

            
            # H. DISPLAY RESULTS TABLE
    
            st.divider()

            st.subheader("📊 Job Matching Summary")

            summary_df = top_jobs[
                [
                    "Title",
                    "Company",
                    "Match Score (%)",
                    "Matching Skills",
                    "Missing Skills"
                ]
            ].copy()

            summary_df["Matching Skills"] = (
                summary_df["Matching Skills"].apply(
                    lambda skills: ", ".join(skills) or "None detected"
                )
            )

            summary_df["Missing Skills"] = (
                summary_df["Missing Skills"].apply(
                    lambda skills: ", ".join(skills) or "None detected"
                )
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True
            )

            
            # I. DOWNLOAD RESULTS
        

            csv_data = summary_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Matching Results",
                data=csv_data,
                file_name="job_matching_results.csv",
                mime="text/csv"
            )

            st.caption(
                "Text similarity measures textual overlap, not "
                "your probability of being hired. Matching and "
                "missing skills are based on a predefined list "
                "of recognized skills and the job descriptions "
                "provided in jobs.csv. A missing skill may not "
                "necessarily be mandatory for the role."
            )


# 8. DEFAULT PAGE BEFORE RESUME UPLOAD

else:

    st.info(
        "💡 Upload your resume using the sidebar to analyze "
        "your skills and find matching jobs."
    )

    st.subheader("Available Jobs in Database")

    st.dataframe(
        jobs_df[["Title", "Company"]],
        use_container_width=True,
        hide_index=True
    )