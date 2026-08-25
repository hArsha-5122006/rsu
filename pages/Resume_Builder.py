import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="3D Resume Builder",
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

/* Neumorphic Form Container */
.input-card {
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 8px 8px 20px #050209, -8px -8px 20px #211335, inset 0px 1px 1px rgba(255, 255, 255, 0.08);
    margin-bottom: 20px;
}

/* Glassmorphism Resume Preview Paper */
.resume-preview-box {
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.8), rgba(14, 7, 23, 0.95));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(192, 132, 252, 0.3);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 12px 12px 35px rgba(0,0,0,0.7), 0 0 25px rgba(168, 85, 247, 0.3);
    color: #e2d9f3;
    font-family: 'Courier New', Courier, monospace;
}

/* Form Inputs & Text Areas Styling */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {
    background-color: #180d26 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(192, 132, 252, 0.3) !important;
    color: #e2d9f3 !important;
}

/* Number Input Buttons & Framework Controls */
div[data-testid="stNumberInput"] input {
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
    width: 100%;
}

div.stButton > button:hover, div.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.7) !important;
    background: linear-gradient(135deg, #c084fc 0%, #7e22ce 100%) !important;
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
# HEADER
# =====================================
st.markdown('<p class="main-title">📄 INTERACTIVE RESUME BUILDER</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ Input Your Credentials & Generate a Live 3D Document Preview</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Layout Split: Input Form (Left) vs Live Resume Preview (Right)
col_form, col_preview = st.columns([1, 1], gap="large")

with col_form:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">👤 Personal Information</p>', unsafe_allow_html=True)
    
    f1, f2 = st.columns(2)
    with f1:
        name = st.text_input("Full Name", value="Alex Mercer")
        email = st.text_input("Email", value="alex.mercer@example.com")
    with f2:
        phone = st.text_input("Phone Number", value="+1 (555) 019-2834")
        branch = st.text_input("Branch / Specialization", value="Computer Science & Engineering")

    st.markdown('<p class="section-title">🎓 Academic Information</p>', unsafe_allow_html=True)
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=8.8, step=0.1)

    st.markdown('<p class="section-title">🛠️ Technical Skills</p>', unsafe_allow_html=True)
    skills = st.text_area(
        "Skills (Comma Separated)",
        value="Python, Machine Learning, SQL, Data Structures, TensorFlow, Streamlit"
    )

    st.markdown('<p class="section-title">🚀 Projects & Experience</p>', unsafe_allow_html=True)
    projects = st.text_area(
        "Project Details",
        value="Placement Prediction System: Built an XGBoost pipeline predicting student recruitment odds with 92% accuracy."
    )
    internships = st.text_area(
        "Internship Experience",
        value="Data Science Intern at TechCorp: Optimized SQL queries and automated EDA pipelines for client datasets."
    )
    certifications = st.text_area(
        "Certifications",
        value="AWS Certified Cloud Practitioner, Deep Learning Specialization (Coursera)"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# RESUME FORMATTING
# =====================================
formatted_name = name.upper() if name else "YOUR NAME"

resume_text = f"""==================================================
                  CURRICULUM VITAE
==================================================

NAME   : {formatted_name}
EMAIL  : {email}
PHONE  : {phone}
BRANCH : {branch}
CGPA   : {cgpa} / 10.0

--------------------------------------------------
SKILLS
--------------------------------------------------
{skills}

--------------------------------------------------
PROJECTS
--------------------------------------------------
{projects}

--------------------------------------------------
INTERNSHIPS
--------------------------------------------------
{internships}

--------------------------------------------------
CERTIFICATIONS
--------------------------------------------------
{certifications}

=================================================="""

# =====================================
# LIVE 3D PREVIEW PANEL
# =====================================
with col_preview:
    st.markdown('<p class="section-title">👁️ Live 3D Document Preview</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="resume-preview-box">
        <h2 style="color:#d8b4fe; margin-top:0; border-bottom: 1px solid rgba(192,132,252,0.3); padding-bottom:10px;">{formatted_name}</h2>
        <p style="color:#c084fc; margin-bottom:15px;"><b>Email:</b> {email} | <b>Phone:</b> {phone}</p>
        <p style="color:#c084fc;"><b>Degree:</b> {branch} (CGPA: {cgpa})</p>
        
        <h4 style="color:#d8b4fe; margin-top:20px; margin-bottom:5px;">🛠️ SKILLS</h4>
        <p style="font-size:14px; margin-top:0;">{skills}</p>

        <h4 style="color:#d8b4fe; margin-top:20px; margin-bottom:5px;">📂 PROJECTS</h4>
        <p style="font-size:14px; margin-top:0;">{projects}</p>

        <h4 style="color:#d8b4fe; margin-top:20px; margin-bottom:5px;">💼 INTERNSHIPS</h4>
        <p style="font-size:14px; margin-top:0;">{internships}</p>

        <h4 style="color:#d8b4fe; margin-top:20px; margin-bottom:5px;">🏆 CERTIFICATIONS</h4>
        <p style="font-size:14px; margin-top:0;">{certifications}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Resume (.txt)",
        data=resume_text,
        file_name=f"{name.replace(' ', '_')}_Resume.txt" if name else "Resume.txt",
        mime="text/plain"
    )

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Resume Builder | Placement Prediction System UI")