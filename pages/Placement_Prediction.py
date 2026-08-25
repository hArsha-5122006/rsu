import streamlit as st
import pandas as pd
import joblib
from io import BytesIO
from reportlab.pdfgen import canvas

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="3D Placement Prediction System",
    page_icon="🎯",
    layout="wide"
)

# =====================================
# CUSTOM 3D DEEP PURPLE & GLASSMORPHISM CSS
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
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(180deg, #d8b4fe 0%, #9333ea 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 10px 25px rgba(147, 51, 234, 0.5);
    letter-spacing: 1px;
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
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 10px;
    text-shadow: 0 5px 15px rgba(192, 132, 252, 0.3);
}

/* Neumorphic Form & Metric Container */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 1px solid rgba(192, 132, 252, 0.25) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 8px 8px 20px #050209, -8px -8px 20px #211335, inset 0px 1px 1px rgba(255, 255, 255, 0.08) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 12px 12px 25px #020403, -12px -12px 25px #27163f, 0 0 20px rgba(168, 85, 247, 0.5) !important;
}

div[data-testid="stMetricLabel"] > label {
    color: #c084fc !important;
    font-size: 14px !important;
}

div[data-testid="stMetricValue"] > div {
    color: #d8b4fe !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 10px rgba(168, 85, 247, 0.4);
}

/* Glassmorphism Results Card */
.glass-box {
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.75), rgba(14, 7, 23, 0.9));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(192, 132, 252, 0.3);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 10px 10px 30px rgba(0,0,0,0.6), inset 1px 1px 1px rgba(255,255,255,0.05);
    margin-bottom: 20px;
}

/* Form Inputs & Sliders Styling */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {
    background-color: #180d26 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(192, 132, 252, 0.3) !important;
    color: #e2d9f3 !important;
}

/* Button & Download Button Styling */
div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #6b21a8 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border: 1px solid rgba(216, 180, 254, 0.3) !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    box-shadow: 0 5px 20px rgba(168, 85, 247, 0.4) !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover, div.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.7) !important;
    background: linear-gradient(135deg, #c084fc 0%, #7e22ce 100%) !important;
}

/* Custom Progress Bar */
.stProgress > div > div > div > div {
    background-color: #a855f7 !important;
}

/* Custom Divider */
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
# PDF GENERATOR
# =====================================
def generate_pdf_report(
    cgpa,
    internships,
    projects_count,
    resume_score,
    placement_status,
    probability,
    salary,
    strengths,
    improvements,
    career_roles
):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Placement Prediction Report")

    y = 800

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Placement Prediction Report")

    y -= 40
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, y, f"CGPA: {cgpa}")
    y -= 20
    pdf.drawString(50, y, f"Internships: {internships}")
    y -= 20
    pdf.drawString(50, y, f"Projects: {projects_count}")
    y -= 20
    pdf.drawString(50, y, f"Resume Score: {resume_score}/100")
    y -= 20
    pdf.drawString(50, y, f"Placement Status: {placement_status}")
    y -= 20
    pdf.drawString(50, y, f"Placement Probability: {probability:.2f}%")
    y -= 20

    if salary is not None:
        pdf.drawString(50, y, f"Estimated Salary: {salary:.2f} LPA")
        y -= 30

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Strengths")
    y -= 20

    pdf.setFont("Helvetica", 12)
    for item in strengths:
        pdf.drawString(70, y, f"- {item}")
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Needs Improvement")
    y -= 20

    pdf.setFont("Helvetica", 12)
    for item in improvements:
        pdf.drawString(70, y, f"- {item}")
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Career Suggestions")
    y -= 20

    pdf.setFont("Helvetica", 12)
    for role in career_roles:
        pdf.drawString(70, y, f"- {role}")
        y -= 18

    pdf.save()
    buffer.seek(0)
    return buffer

# =====================================
# HEADER
# =====================================
st.markdown('<p class="main-title">🎯 PLACEMENT PREDICTION SYSTEM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ Predict placement chances, estimated packages, skill gaps, and custom career paths</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================
# INPUTS
# =====================================
st.markdown('<p class="section-title">📋 Student Profile Inputs</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.5)
    backlogs = st.number_input("Backlogs", 0, 20, 0)
    coding_skills = st.slider("Coding Skills Score", 0, 100, 70)
    dsa_score = st.slider("DSA Score", 0, 100, 70)

with col2:
    aptitude_score = st.slider("Aptitude Score", 0, 100, 70)
    communication_skills = st.slider("Communication Skills Score", 0, 100, 70)
    internships = st.number_input("Internships Count", 0, 10, 1)
    projects_count = st.number_input("Projects Count", 0, 20, 2)

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================
# PREDICTION LOGIC
# =====================================
if st.button("🚀 Run Prediction Model", use_container_width=True):

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

    # Score Calculation
    resume_score = 0
    resume_score += min((cgpa / 10) * 25, 25)
    resume_score += min((coding_skills / 100) * 20, 20)
    resume_score += min((dsa_score / 100) * 15, 15)
    resume_score += min((aptitude_score / 100) * 10, 10)
    resume_score += min((communication_skills / 100) * 10, 10)
    resume_score += min(internships * 5, 10)
    resume_score += min(projects_count * 2, 10)
    resume_score = round(resume_score, 2)

    # Model Predictions
    if placement_model is not None:
        placement_prediction = placement_model.predict(input_df)[0]
        probability = placement_model.predict_proba(input_df)[0][1]
    else:
        probability = min((resume_score / 100) * 1.1, 0.95)
        placement_prediction = 1 if probability >= 0.50 else 0

    readiness_score = int(probability * 100)

    # Display Top Metrics
    st.markdown('<p class="section-title">📊 Key Prediction Metrics</p>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Resume Score", f"{resume_score} / 100")
    with m2:
        st.metric("Placement Probability", f"{probability * 100:.2f}%")
    with m3:
        st.metric("Readiness Level", f"{readiness_score} / 100")

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(readiness_score)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Salary and Outcome Results
    salary_prediction = None
    if placement_prediction == 1:
        if salary_model is not None:
            salary_prediction = salary_model.predict(input_df)[0]
        else:
            salary_prediction = 6.5 + (cgpa * 0.4) + (coding_skills * 0.05)

        lower_salary = max(salary_prediction - 2, 0)
        upper_salary = salary_prediction + 2

        st.markdown(f"""
        <div class="glass-box">
            <h2 style="color:#d8b4fe; margin-top:0;">🎉 Likely to be PLACED</h2>
            <p style="font-size: 18px; margin-bottom:5px;">Estimated Package: <b style="color:#c084fc;">{salary_prediction:.2f} LPA</b></p>
            <p style="color:#e2d9f3;">Expected Salary Range: <b>{lower_salary:.2f} - {upper_salary:.2f} LPA</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-box">
            <h2 style="color:#ff6b6b; margin-top:0;">❌ Likely NOT PLACED Currently</h2>
            <p style="color:#e2d9f3;">Focused skill development in DSA, coding, and internship exposure can significantly lift placement probabilities.</p>
        </div>
        """, unsafe_allow_html=True)

    # Skill Gap Analysis
    strengths = []
    improvements = []

    if cgpa >= 8: strengths.append("CGPA")
    else: improvements.append("CGPA")

    if coding_skills >= 70: strengths.append("Coding Skills")
    else: improvements.append("Coding Skills")

    if dsa_score >= 70: strengths.append("DSA")
    else: improvements.append("DSA")

    if aptitude_score >= 70: strengths.append("Aptitude")
    else: improvements.append("Aptitude")

    if communication_skills >= 70: strengths.append("Communication")
    else: improvements.append("Communication")

    if internships >= 1: strengths.append("Internships")
    else: improvements.append("Internships")

    if projects_count >= 2: strengths.append("Projects")
    else: improvements.append("Projects")

    st.markdown('<p class="section-title">🧠 Skill Gap Breakdown</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("✅ Identified Strengths")
        for item in strengths:
            st.write(f"• **{item}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("⚠️ Areas needing Improvement")
        for item in improvements:
            st.write(f"• **{item}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Career Suggestions
    career_roles = []
    if coding_skills >= 80 and dsa_score >= 80: career_roles.append("Software Development Engineer")
    if dsa_score >= 75: career_roles.append("Backend Developer")
    if communication_skills >= 80: career_roles.append("Business Analyst")
    if aptitude_score >= 75: career_roles.append("Consultant")
    if internships >= 2 and projects_count >= 3: career_roles.append("Full Stack Developer")
    if cgpa >= 8.5: career_roles.append("Product Engineer")
    if not career_roles: career_roles.append("Junior Software Developer")

    st.markdown('<p class="section-title">🚀 Top Role Matches</p>', unsafe_allow_html=True)
    role_cols = st.columns(len(set(career_roles)))
    for idx, role in enumerate(set(career_roles)):
        with role_cols[idx]:
            st.info(f"🎯 **{role}**")

    st.markdown("<hr>", unsafe_allow_html=True)

    # PDF Download
    pdf_file = generate_pdf_report(
        cgpa,
        internships,
        projects_count,
        resume_score,
        "PLACED" if placement_prediction == 1 else "NOT PLACED",
        probability * 100,
        salary_prediction,
        strengths,
        improvements,
        career_roles
    )

    st.markdown('<p class="section-title">📄 Download Comprehensive Report</p>', unsafe_allow_html=True)
    st.download_button(
        "⬇ Download Placement Report (.pdf)",
        data=pdf_file,
        file_name="Placement_Prediction_Report.pdf",
        mime="application/pdf"
    )

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Placement Prediction System | Streamlit + XGBoost UI")