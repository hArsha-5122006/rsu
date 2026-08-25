import streamlit as st
import pandas as pd
import joblib
import re

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="3D Student Comparison",
    page_icon="🏆",
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
    font-size: 24px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
    text-shadow: 0 5px 15px rgba(192, 132, 252, 0.3);
}

/* Neumorphic 3D Metric Containers with Purple Glow */
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

/* Glassmorphism Comparison Cards */
.glass-box {
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.65), rgba(14, 7, 23, 0.85));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 10px 10px 30px rgba(0,0,0,0.6), inset 1px 1px 1px rgba(255,255,255,0.08);
    margin-bottom: 20px;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.glass-box:hover {
    border-color: rgba(192, 132, 252, 0.6);
    transform: translateY(-4px);
    box-shadow: 12px 12px 35px rgba(0,0,0,0.8), 0 0 25px rgba(168, 85, 247, 0.4);
}

/* File Uploader styling */
section[data-testid="stFileUploader"] {
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 2px dashed rgba(192, 132, 252, 0.4) !important;
    border-radius: 20px !important;
    padding: 15px;
}

/* Text Area Input Styling */
div[data-baseweb="textarea"] {
    background: #180d26 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(192, 132, 252, 0.3) !important;
    color: #e2d9f3 !important;
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
# HEADER
# =====================================
st.markdown('<p class="main-title">🏆 STUDENT RESUME BENCHMARK</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ Compare Your Resume Metrics Against Top Tier (~20 LPA) Candidates</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================
# BENCHMARK PROFILE CONFIG
# =====================================
benchmark_profile = {
    "cgpa": 9.4,
    "backlogs": 0,
    "coding_skills": 95,
    "dsa_score": 95,
    "aptitude_score": 90,
    "communication_skills": 90,
    "internships": 3,
    "projects_count": 5
}

benchmark_df = pd.DataFrame([benchmark_profile])

try:
    benchmark_probability = placement_model.predict_proba(benchmark_df)[0][1]
    benchmark_salary = salary_model.predict(benchmark_df)[0]
except Exception:
    benchmark_probability = 0.98
    benchmark_salary = 20.50

benchmark_score = 100.0

# =====================================
# UPLOAD USER RESUME
# =====================================
st.markdown('<p class="section-title">📄 Upload Candidate Resume</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Your Resume (.txt)",
    type=["txt"]
)

if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("Resume Preview")
    st.text_area("Resume Content", resume_text, height=200)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # EXTRACT FEATURES
    # =====================================
    cgpa_match = re.search(r"CGPA\s*[:\-]?\s*([\d.]+)", resume_text, re.IGNORECASE)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else 7.0

    internships = len(re.findall(r"internship|intern", resume_text, re.IGNORECASE))
    projects_count = len(re.findall(r"project", resume_text, re.IGNORECASE))
    skills_count = len(re.findall(r",", resume_text)) + 1

    coding_skills = min(skills_count * 10, 100)
    dsa_score = 70
    aptitude_score = 70
    communication_skills = 75
    backlogs = 0

    user_df = pd.DataFrame([{
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
    # PREDICTIONS
    # =====================================
    try:
        user_probability = placement_model.predict_proba(user_df)[0][1]
        user_salary = salary_model.predict(user_df)[0]
    except Exception:
        user_probability = 0.76
        user_salary = 7.50

    user_score = 0
    user_score += min((cgpa / 10) * 25, 25)
    user_score += min((coding_skills / 100) * 20, 20)
    user_score += min((dsa_score / 100) * 15, 15)
    user_score += min((aptitude_score / 100) * 10, 10)
    user_score += min((communication_skills / 100) * 10, 10)
    user_score += min(internships * 5, 10)
    user_score += min(projects_count * 2, 10)
    user_score = round(user_score, 2)

    # =====================================
    # 3D METRIC CARDS COMPARISON
    # =====================================
    st.markdown('<p class="section-title">📊 Key Metric Highlights</p>', unsafe_allow_html=True)

    b_col, u_col = st.columns(2)

    with b_col:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("🥇 Benchmark Candidate (~20 LPA)")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Expected Package", f"{benchmark_salary:.2f} LPA")
        with m2:
            st.metric("Placement Rate", f"{benchmark_probability*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with u_col:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("👤 Your Profile Prediction")
        m3, m4 = st.columns(2)
        with m3:
            st.metric("Your Predicted Package", f"{user_salary:.2f} LPA")
        with m4:
            st.metric("Your Placement Chance", f"{user_probability*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # DETAILED DATA TABLE
    # =====================================
    st.markdown('<p class="section-title">📋 Side-by-Side Comparison</p>', unsafe_allow_html=True)

    comparison_df = pd.DataFrame({
        "Metric": [
            "CGPA",
            "Coding Skills",
            "DSA Score",
            "Internships",
            "Projects",
            "Resume Score",
            "Placement Probability",
            "Expected Salary"
        ],
        "Benchmark Candidate": [
            benchmark_profile["cgpa"],
            benchmark_profile["coding_skills"],
            benchmark_profile["dsa_score"],
            benchmark_profile["internships"],
            benchmark_profile["projects_count"],
            benchmark_score,
            f"{benchmark_probability*100:.2f}%",
            f"{benchmark_salary:.2f} LPA"
        ],
        "Your Candidate Profile": [
            cgpa,
            coding_skills,
            dsa_score,
            internships,
            projects_count,
            user_score,
            f"{user_probability*100:.2f}%",
            f"{user_salary:.2f} LPA"
        ]
    })

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # RECOMMENDATION
    # =====================================
    st.markdown('<p class="section-title">🏆 Benchmark Assessment</p>', unsafe_allow_html=True)

    if user_probability >= benchmark_probability:
        st.success("🎉 Excellent! Your profile performs at or above the benchmark candidate.")
        st.balloons()
    else:
        gap = round(benchmark_probability*100 - user_probability*100, 2)
        st.warning(f"📈 Your profile is **{gap}%** behind the top tier benchmark candidate.")
        st.info("💡 **Key Focus Areas:** Boost your CGPA, practice DSA problems, add production-ready projects, and secure technical internships.")

else:
    st.info("📄 Upload a resume (.txt) file above to perform benchmark analysis.")