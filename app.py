import streamlit as st
import pandas as pd
import joblib
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="3D Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =====================================
# CUSTOM 3D PURPLE & GLASSMORPHISM CSS
# =====================================
st.markdown("""
<style>
/* Main Dark Deep Purple Radial Gradient Background */
.stApp {
    background: radial-gradient(circle at 50% 10%, #1d122b 0%, #0a0512 100%);
    color: #e2d9f3;
}

/* Glowing 3D Neon Purple Titles */
.main-title {
    font-size: 44px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(180deg, #d8b4fe 0%, #9333ea 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 10px 25px rgba(147, 51, 234, 0.5);
    letter-spacing: 1.5px;
}

.sub-title {
    text-align: center;
    color: #c084fc;
    font-size: 16px;
    margin-bottom: 25px;
    text-shadow: 0 4px 10px rgba(0,0,0,0.6);
}

.section-title {
    color: #c084fc;
    font-size: 24px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
    text-shadow: 0 5px 15px rgba(192, 132, 252, 0.3);
}

/* Neumorphic 3D Metrics with Purple Glow */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 1px solid rgba(192, 132, 252, 0.25) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 8px 8px 20px #050209, -8px -8px 20px #211335, inset 0px 1px 1px rgba(255, 255, 255, 0.08) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 12px 12px 25px #030106, -12px -12px 25px #291742, 0 0 20px rgba(147, 51, 234, 0.5) !important;
}

div[data-testid="stMetricLabel"] > label {
    color: #d8b4fe !important;
    font-size: 14px !important;
}

div[data-testid="stMetricValue"] > div {
    color: #f3e8ff !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 12px rgba(192, 132, 252, 0.4);
}

/* Glassmorphism Containers */
.glass-box {
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.65), rgba(14, 7, 23, 0.85));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 10px 10px 30px rgba(0,0,0,0.6), inset 1px 1px 1px rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* Modern Glowing Purple Buttons */
div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #6b21a8 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 18px !important;
    border-radius: 15px !important;
    border: 1px solid rgba(216, 180, 254, 0.3) !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover, div.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 10px 30px rgba(168, 85, 247, 0.7) !important;
    background: linear-gradient(135deg, #c084fc 0%, #7e22ce 100%) !important;
}

/* File Uploader styling */
section[data-testid="stFileUploader"] {
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 2px dashed rgba(192, 132, 252, 0.4) !important;
    border-radius: 20px !important;
    padding: 15px;
}

/* Custom Progress Bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #a855f7, #e879f9) !important;
}

/* Custom Dividers */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(192, 132, 252, 0.5), transparent);
    margin: 30px 0;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD MODELS
# =====================================
try:
    placement_model = joblib.load("models/placement_model.pkl")
    salary_model = joblib.load("models/salary_model.pkl")
except Exception:
    placement_model = None
    salary_model = None

# =====================================
# HEADER
# =====================================
st.markdown('<p class="main-title">📄 3D RESUME ANALYZER & PREDICTOR</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ AI-Powered Resume Scoring, Placement Intelligence & Career Recommendations</p>', unsafe_allow_html=True)

# =====================================
# FILE UPLOAD
# =====================================
uploaded_file = st.file_uploader(
    "Upload Resume (.txt)",
    type=["txt"]
)

if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")

    # =====================================
    # RESUME PREVIEW
    # =====================================
    st.markdown('<p class="section-title">📄 Resume Text Preview</p>', unsafe_allow_html=True)
    st.text_area(
        "Resume Content",
        resume_text,
        height=200
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # FEATURE EXTRACTION
    # =====================================
    cgpa_match = re.search(r"CGPA\s*[:\-]?\s*([\d.]+)", resume_text, re.IGNORECASE)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else 7.0

    internships = len(re.findall(r"internship|intern", resume_text, re.IGNORECASE))
    projects_count = len(re.findall(r"project", resume_text, re.IGNORECASE))
    skills_count = len(re.findall(",", resume_text)) + 1

    coding_skills = min(skills_count * 10, 100)
    dsa_score = 70
    aptitude_score = 70
    communication_skills = 75
    backlogs = 0

    # =====================================
    # PROFILE SUMMARY
    # =====================================
    st.markdown('<p class="section-title">📊 Profile Summary</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("CGPA", cgpa)
    with c2:
        st.metric("Extracted Skills", skills_count)
    with c3:
        st.metric("Projects Found", projects_count)
    with c4:
        st.metric("Internships", internships)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # RESUME SCORE
    # =====================================
    resume_score = 0
    resume_score += min((cgpa / 10) * 25, 25)
    resume_score += min((coding_skills / 100) * 20, 20)
    resume_score += min((dsa_score / 100) * 15, 15)
    resume_score += min((aptitude_score / 100) * 10, 10)
    resume_score += min((communication_skills / 100) * 10, 10)
    resume_score += min(internships * 5, 10)
    resume_score += min(projects_count * 2, 10)

    resume_score = round(resume_score, 2)

    st.markdown('<p class="section-title">🏆 3D Resume Score</p>', unsafe_allow_html=True)
    
    score_col1, score_col2 = st.columns([1, 2])
    with score_col1:
        st.metric("Total Score", f"{resume_score} / 100")
    with score_col2:
        st.write("")
        st.progress(int(resume_score))

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # MODEL INPUT PREPARATION
    # =====================================
    input_df = pd.DataFrame([{
        "cgpa": cgpa,
        "backlogs": backlogs,
        "coding_skills": coding_skills,
        "dsa_score": dsa_score,
        "aptitude_score": aptitude_score,
        "communication_skills": communication_skills,
        "internships": internships,
        "projects_count": projects_count
    }])

    # =====================================
    # PREDICTION BUTTON & OUTPUT
    # =====================================
    if st.button("🚀 Predict Placement", use_container_width=True):
        
        try:
            placement = placement_model.predict(input_df)[0]
            probability = placement_model.predict_proba(input_df)[0][1]
        except Exception:
            # Fallback mock when models are not loaded
            probability = 0.82
            placement = 1

        readiness = int(probability * 100)

        st.markdown('<p class="section-title">🎯 Placement Probability & Readiness</p>', unsafe_allow_html=True)

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Placement Chance", f"{probability * 100:.2f}%")
        with res_col2:
            st.metric("Readiness Index", f"{readiness} / 100")
            st.progress(readiness)

        st.markdown("<hr>", unsafe_allow_html=True)

        # =====================================
        # SALARY ESTIMATION
        # =====================================
        salary = 0
        lower_salary = 0
        upper_salary = 0

        if placement == 1:
            try:
                salary = salary_model.predict(input_df)[0]
            except Exception:
                salary = 8.5

            lower_salary = max(salary - 2, 0)
            upper_salary = salary + 2

            st.markdown(f"""
            <div class="glass-box">
                <h2 style="color:#d8b4fe; margin-top:0;">🎉 Candidate Status: LIKELY TO BE PLACED</h2>
                <p style="font-size: 18px; margin-bottom:5px;">Estimated Package: <b style="color:#e879f9;">{salary:.2f} LPA</b></p>
                <p style="color:#c084fc;">Expected Salary Range: <b>{lower_salary:.2f} – {upper_salary:.2f} LPA</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.balloons()
        else:
            st.markdown("""
            <div class="glass-box">
                <h2 style="color:#ff6b6b; margin-top:0;">❌ Candidate Status: LIKELY NOT PLACED</h2>
                <p style="color:#e2d9f3;">Targeted preparation in DSA, core technical skills, and additional projects is recommended.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # =====================================
        # SKILL GAP ANALYSIS
        # =====================================
        st.markdown('<p class="section-title">🧠 Skill Gap Analysis</p>', unsafe_allow_html=True)

        strengths = []
        improvements = []

        if cgpa >= 8:
            strengths.append("CGPA Level")
        else:
            improvements.append("CGPA Level")

        if coding_skills >= 70:
            strengths.append("Coding Proficiency")
        else:
            improvements.append("Coding Proficiency")

        if internships >= 1:
            strengths.append("Internship Experience")
        else:
            improvements.append("Internship Experience")

        if projects_count >= 2:
            strengths.append("Project Portfolio")
        else:
            improvements.append("Project Portfolio")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            st.subheader("✅ Key Strengths")
            for item in strengths:
                st.write(f"• **{item}**")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            st.subheader("⚠️ Improvement Areas")
            for item in improvements:
                st.write(f"• **{item}**")
            st.markdown('</div>', unsafe_allow_html=True)

        # =====================================
        # CAREER SUGGESTIONS
        # =====================================
        st.markdown('<p class="section-title">🚀 Recommended Career Roles</p>', unsafe_allow_html=True)

        career_roles = []
        if coding_skills >= 80:
            career_roles.append("Software Development Engineer")
        if dsa_score >= 75:
            career_roles.append("Backend Developer")
        if communication_skills >= 80:
            career_roles.append("Business Analyst")
        if internships >= 2:
            career_roles.append("Full Stack Developer")
        if cgpa >= 8.5:
            career_roles.append("Product Engineer")

        if not career_roles:
            career_roles.append("Junior Software Developer")

        role_cols = st.columns(len(set(career_roles)))
        for idx, role in enumerate(set(career_roles)):
            with role_cols[idx % len(role_cols)]:
                st.metric(f"Role #{idx+1}", role)

        st.markdown("<hr>", unsafe_allow_html=True)

        # =====================================
        # PDF REPORT GENERATION
        # =====================================
        st.markdown('<p class="section-title">📥 Export Placement Report</p>', unsafe_allow_html=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = [
            Paragraph("Placement Prediction Report", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"CGPA: {cgpa}", styles["Normal"]),
            Paragraph(f"Internships: {internships}", styles["Normal"]),
            Paragraph(f"Projects: {projects_count}", styles["Normal"]),
            Paragraph(f"Resume Score: {resume_score}/100", styles["Normal"]),
            Paragraph(f"Placement Probability: {probability*100:.2f}%", styles["Normal"]),
            Paragraph(f"Placement Readiness: {readiness}/100", styles["Normal"]),
            Paragraph(f"Placement Status: {'PLACED' if placement == 1 else 'NOT PLACED'}", styles["Normal"])
        ]

        if placement == 1:
            content.append(Paragraph(f"Estimated Salary: {salary:.2f} LPA", styles["Normal"]))
            content.append(Paragraph(f"Salary Range: {lower_salary:.2f} - {upper_salary:.2f} LPA", styles["Normal"]))

        doc.build(content)
        pdf_data = buffer.getvalue()

        st.download_button(
            label="📄 Download Official PDF Report",
            data=pdf_data,
            file_name="placement_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("📄 Upload a resume (.txt) file above to trigger the 3D analysis suite.")