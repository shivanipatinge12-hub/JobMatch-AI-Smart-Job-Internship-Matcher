# JobMatch AI – Smart Job & Internship Matcher

## 📌 Project Overview

JobMatch AI is a Python-based web application developed using Streamlit that helps job seekers identify suitable job and internship opportunities based on their resume content.

The application allows users to upload their resumes in PDF format, extract technical skills, and compare their resume content with available job descriptions. It uses TF-IDF vectorization and cosine similarity to calculate text similarity scores and rank job listings according to their relevance to the uploaded resume.

The application also identifies matching skills and potential skill gaps, helping candidates understand which skills are already present in their resumes and which additional skills are mentioned in the job descriptions.

The main objective of this project is to simplify the initial job-search process and help candidates explore opportunities that align with their existing skills.

## 🎯 Objectives

- Automate the initial comparison of resumes and job descriptions.
- Identify technical skills mentioned in a candidate's resume.
- Recommend relevant job and internship listings based on text similarity.
- Highlight matching skills and potential skill gaps.
- Provide an interactive interface for exploring job recommendations.
- Allow users to download their job-matching results for future reference.

## ✨ Key Features

### 1. Resume Upload
Users can upload their resumes in PDF format through the application's sidebar.

### 2. Automatic Skill Extraction
The application extracts readable text from the uploaded resume and identifies recognized technical skills using a predefined skill dictionary.

The dictionary includes skills and technologies such as:
- Python and SQL
- MySQL and Oracle
- Pandas and NumPy
- Machine Learning and Deep Learning
- Scikit-learn, TensorFlow, and PyTorch
- Git and GitHub


The extracted skills are displayed in the application.

### 3. Resume and Job Description Matching
The application compares the resume text with job titles and job descriptions using TF-IDF vectorization and cosine similarity.

TF-IDF converts text into numerical representations, while cosine similarity measures how similar those representations are.

Based on the calculated similarity scores, job listings are ranked from highest to lowest similarity.

### 4. Matching Skills Identification
The application compares the skills extracted from the resume with the skills identified in each job description.

It displays the recognized skills that appear in both the resume and the job description.

### 5. Potential Skill Gap Identification
The application highlights recognized skills mentioned in a job description that were not detected in the resume.

This feature can help candidates identify areas they may want to learn or improve.

### 6. Top Five Job Recommendations
The application displays the five highest-ranked job listings based on their text similarity scores.

For each recommendation, users can view the job title, company name, job description, matching skills, and potential missing skills.

### 7. Job Matching Summary
A summary table presents the top job recommendations along with their similarity scores, matching skills, and potential skill gaps.

### 8. Download Results
Users can download the job-matching summary as a CSV file for future reference.

### 9. Job Listings Dataset
The application reads job listings from a local CSV file named `jobs.csv`. This dataset provides the job titles, company names, and job descriptions used for matching.

## 🛠️ Technologies Used

- **Python:** Core programming language used to develop the application.
- **Streamlit:** Creates the interactive web interface.
- **Pandas:** Loads, processes, filters, and organizes job listing data.
- **Scikit-learn:** Provides TF-IDF vectorization and cosine similarity calculations.
- **pypdf:** Extracts readable text from uploaded PDF resumes.
- **Regular Expressions (re):** Helps identify recognized skills in resume and job description text.
- **CSV:** Stores job listings and allows matching results to be downloaded.

## ⚙️ How It Works

The application follows these steps:

1. **Load Job Data:** Reads job listings from `jobs.csv` and validates the required columns.
2. **Upload Resume:** Accepts a candidate's resume in PDF format.
3. **Extract Resume Text:** Uses pypdf to extract readable text from the uploaded document.
4. **Identify Skills:** Searches the extracted text for skills listed in the predefined skill dictionary.
5. **Process Job Descriptions:** Identifies recognized skills in the available job descriptions.
6. **Calculate Text Similarity:** Applies TF-IDF vectorization and cosine similarity to compare the resume with job titles and descriptions.
7. **Rank Job Listings:** Sorts job listings by their similarity scores and selects the top five.
8. **Identify Skill Gaps:** Compares the recognized resume skills with the skills found in each job description.
9. **Display Results:** Presents recommendations, similarity scores, matching skills, and potential skill gaps.
10. **Download Summary:** Allows users to export the matching results to a CSV file.

## 📂 Project Structure

```text
jobmatch-ai/
│
├── app.py
├── jobs.csv
├── requirements.txt
├── README.md
└── .gitignore
```

### File Descriptions

- `app.py` – Contains the main application code, including resume processing, skill extraction, similarity calculations, and result display.
- `jobs.csv` – Contains job listings with titles, company names, and descriptions.
- `requirements.txt` – Lists the Python libraries required to run the application.
- `README.md` – Provides project documentation and setup instructions.


## 📋 Dataset Format

The application requires a CSV file named `jobs.csv` with the following columns:

| Column | Description |

| `Title` | Job or internship title |
| `Company` | Company name |
| `Description` | Job description containing the required skills and responsibilities |

Example:

```csv
Title,Company,Description
Python Developer,ABC Technologies,Looking for Python and SQL skills
Data Analyst,XYZ Solutions,Requires Python Excel and data analysis
Machine Learning Intern,Tech Company,Knowledge of Python and machine learning
```

The above entries are examples for demonstration purposes, not verified job vacancies.

## 💻 Installation and Setup

### Prerequisites

Before running the application, ensure that Python and pip are installed on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/jobmatch-ai.git
```

Replace `YOUR-USERNAME` with your GitHub username and use your actual repository URL.

### Step 2: Navigate to the Project Folder

```bash
cd jobmatch-ai
```

### Step 3: Install Dependencies

Install the required libraries using:

```bash
python -m pip install -r requirements.txt
```

### Step 4: Verify the Project Files

Ensure that `app.py`, `jobs.csv`, and `requirements.txt` are present in the project folder.

The `jobs.csv` file must contain the required columns: `Title`, `Company`, and `Description`.

### Step 5: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL that you can open in your web browser.

### Step 6: Use the Application

1. Open the application in your browser.
2. Upload a readable PDF resume using the sidebar.
3. Review the technical skills detected in your resume.
4. Explore the top five matching job listings.
5. Review the text similarity scores and matching skills.
6. Identify potential skill gaps.
7. Download the matching summary as a CSV file if required.

## 📊 Matching Methodology

### TF-IDF Vectorization

Term Frequency–Inverse Document Frequency (TF-IDF) converts text into numerical features based on the importance of words within the documents being compared.

In this project, the resume and job documents are converted into TF-IDF vectors.

### Cosine Similarity

Cosine similarity measures the similarity between the resume vector and each job document vector.

The resulting scores are converted to percentages for display. Higher scores indicate greater text similarity within this matching approach.

**Important:** These percentages measure text similarity. They do not represent the probability of being hired or guarantee that a job is suitable for a candidate.

## ⚠️ Current Limitations

- Job listings are loaded from a local CSV dataset.
- Live job listings from external job portals are not currently retrieved by the application.
- Skill extraction depends on a predefined dictionary of recognized skills.
- Skills expressed using unrecognized terms or alternative wording may not be detected.
- Text similarity may not fully capture a candidate's experience, proficiency, qualifications, or suitability for a role.
- Missing skills are based on the predefined skill dictionary and should be treated as suggestions for further review.
- The application works best with PDF resumes containing readable text. Image-based or scanned PDFs may not produce usable text.

## 🚀 Future Enhancements

Potential improvements include:

- Integrating authorized job APIs to retrieve current job listings.
- Adding job title, location, experience, and employment-type filters.
- Improving skill extraction to recognize additional terms and variations.
- Introducing more advanced resume and job description matching techniques.
- Adding user-friendly job search and recommendation filters.
- Deploying the application online so users can access it through a web browser.

These are proposed enhancements and are not all implemented in the current version.

## 👩‍💻 Author

**Shivani Patinge**

Engineering Graduate | Python | SQL | Data Analysis | Machine Learning | Deep Learning

GitHub: Add your GitHub profile link here.

## 📄 Disclaimer

JobMatch AI is an educational project designed to demonstrate resume text extraction, skill identification, and job description matching.

The application provides recommendations based on text similarity and a predefined skill dictionary. It does not guarantee employment, verify job vacancies, or replace a recruiter's assessment.
