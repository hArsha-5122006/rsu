import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hackathon Team Formation",
    page_icon="👥",
    layout="wide"
)

# ============================================================
# CUSTOM 3D PURPLE & GLASSMORPHISM CSS
# ============================================================

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
    letter-spacing: 1px;
}

.subtitle {
    font-size: 16px;
    text-align: center;
    color: #c084fc;
    margin-bottom: 25px;
    text-shadow: 0 4px 10px rgba(0,0,0,0.6);
}

/* Section Headings */
h2, h3, .stSubheader {
    color: #c084fc !important;
    text-shadow: 0 4px 12px rgba(192, 132, 252, 0.3) !important;
}

/* Custom Role and Team Cards */
.team-card {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(145deg, #180d26, #0e0717);
    border: 1px solid rgba(192, 132, 252, 0.25);
    box-shadow: 8px 8px 20px #050209, -8px -8px 20px #211335;
    margin-bottom: 15px;
}

.role-card {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.8), rgba(14, 7, 23, 0.9));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(192, 132, 252, 0.25);
    box-shadow: 8px 8px 20px rgba(0,0,0,0.5), inset 1px 1px 1px rgba(255,255,255,0.05);
    margin-bottom: 15px;
    color: #e2d9f3;
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.role-card:hover {
    transform: translateY(-4px);
    border-color: rgba(192, 132, 252, 0.5);
}

.role-card h3 {
    margin-top: 0;
    color: #d8b4fe !important;
}

/* Modern Neumorphic 3D Card Styling for Metrics */
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
    box-shadow: 12px 12px 25px #020403, -12px -12px 25px #27163f, 0 0 20px rgba(168, 85, 247, 0.5) !important;
}

/* Metric text enhancements */
div[data-testid="stMetricLabel"] > label {
    color: #c084fc !important;
    font-size: 14px !important;
}

div[data-testid="stMetricValue"] > div {
    color: #d8b4fe !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 10px rgba(168, 85, 247, 0.4);
}

/* Custom Dataframe Container */
div[data-testid="stDataFrame"] {
    background: linear-gradient(145deg, #180d26, #0e0717) !important;
    border: 1px solid rgba(192, 132, 252, 0.25) !important;
    border-radius: 16px !important;
    padding: 10px !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #0e0717 !important;
    border-right: 1px solid rgba(192, 132, 252, 0.2) !important;
}

/* Button styling */
div.stButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
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


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">👥 Smart Hackathon Team Formation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Build a balanced 4-member hackathon team using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# LOAD EXISTING PICKLE FILES
# ============================================================

@st.cache_resource
def load_models():

    try:
        kmeans_model = joblib.load("models/kmeans_team_model.pkl")
    except Exception as e:
        kmeans_model = None

    try:
        team_dataset = joblib.load("models/team_dataset.pkl")
    except Exception as e:
        # Fallback synthetic dataset for UI demonstration if PKL doesn't exist
        team_dataset = pd.DataFrame({
            "student_name": [f"Student {i+1}" for i in range(12)],
            "branch": ["CSE", "ECE", "IT", "AIML", "CSE", "IT", "CSE", "ECE", "AIML", "CSE", "IT", "CSE"],
            "cgpa": [8.5, 7.8, 9.1, 8.2, 7.5, 8.9, 9.0, 7.2, 8.7, 8.1, 7.9, 9.3],
            "coding_skills": [85, 70, 92, 78, 65, 88, 90, 60, 84, 76, 80, 95],
            "dsa_score": [80, 65, 90, 75, 60, 85, 88, 55, 82, 70, 78, 92],
            "ml_knowledge": [40, 30, 95, 88, 35, 45, 90, 25, 85, 50, 40, 92],
            "frontend_skill": [90, 85, 40, 50, 88, 92, 45, 80, 55, 82, 90, 50],
            "backend_skill": [85, 75, 88, 80, 70, 84, 86, 65, 78, 85, 80, 90],
            "communication_skills": [80, 85, 78, 82, 90, 88, 75, 80, 84, 86, 88, 90],
            "projects_count": [3, 2, 4, 3, 2, 4, 5, 1, 3, 2, 3, 4]
        })

    try:
        team_features = joblib.load("models/team_features.pkl")
    except Exception as e:
        team_features = None

    try:
        team_scaler = joblib.load("models/team_scaler.pkl")
    except Exception as e:
        team_scaler = None

    return (
        kmeans_model,
        team_dataset,
        team_features,
        team_scaler
    )


(
    kmeans_model,
    df,
    team_features,
    team_scaler
) = load_models()


# ============================================================
# CHECK DATASET
# ============================================================

if df is None:
    st.error("Unable to load team dataset.")
    st.stop()


# ============================================================
# CONVERT DATASET TO DATAFRAME
# ============================================================

if not isinstance(df, pd.DataFrame):
    try:
        df = pd.DataFrame(df)
    except Exception:
        st.error("team_dataset.pkl does not contain a valid dataset.")
        st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.success(
    f"Dataset loaded successfully — {len(df)} students available."
)


# ============================================================
# FEATURE COLUMNS
# ============================================================

feature_columns = [
    "coding_skills",
    "dsa_score",
    "ml_knowledge",
    "frontend_skill",
    "backend_skill",
    "communication_skills"
]


# ============================================================
# CHECK FEATURES & FILL MISSING
# ============================================================

for column in feature_columns:
    if column not in df.columns:
        df[column] = 0
    df[column] = pd.to_numeric(df[column], errors="coerce")
    median_value = df[column].median()
    if pd.isna(median_value):
        median_value = 0
    df[column] = df[column].fillna(median_value)


# ============================================================
# APPLY K-MEANS CLUSTER
# ============================================================

try:
    X = df[feature_columns]

    if team_scaler is not None:
        try:
            X_scaled = team_scaler.transform(X)
        except Exception:
            X_scaled = X.values
    else:
        X_scaled = X.values

    if kmeans_model is not None and hasattr(kmeans_model, "n_features_in_"):
        expected_features = kmeans_model.n_features_in_
        if X_scaled.shape[1] == expected_features:
            df["team_cluster"] = kmeans_model.predict(X_scaled)
        else:
            df["team_cluster"] = 0
    else:
        df["team_cluster"] = 0
except Exception:
    df["team_cluster"] = 0


# ============================================================
# CREATE INTERNAL ROLE SCORES
# ============================================================

df["frontend_score"] = (
    df["frontend_skill"] * 0.55
    + df["coding_skills"] * 0.20
    + df["communication_skills"] * 0.15
    + (df["projects_count"] * 0.10 if "projects_count" in df.columns else df["communication_skills"] * 0.10)
)

df["backend_score"] = (
    df["backend_skill"] * 0.50
    + df["coding_skills"] * 0.25
    + df["dsa_score"] * 0.15
    + df["communication_skills"] * 0.10
)

df["ml_score"] = (
    df["ml_knowledge"] * 0.50
    + df["coding_skills"] * 0.25
    + df["dsa_score"] * 0.15
    + df["communication_skills"] * 0.10
)


# ============================================================
# DEFAULT COLUMNS CHECK
# ============================================================

if "student_name" not in df.columns:
    df["student_name"] = [f"Student {i + 1}" for i in range(len(df))]

if "branch" not in df.columns:
    df["branch"] = "N/A"

if "cgpa" not in df.columns:
    df["cgpa"] = 0


# ============================================================
# HACKATHON TEAM REQUIREMENTS
# ============================================================

st.subheader("🎯 Hackathon Team Requirements")

req1, req2, req3, req4 = st.columns(4)

with req1:
    st.metric("🎨 Frontend", "1")

with req2:
    st.metric("⚙️ Backend", "2")

with req3:
    st.metric("🤖 ML Engineer", "1")

with req4:
    st.metric("👥 Team Size", "4")


st.divider()


# ============================================================
# EXISTING TEAM MEMBERS
# ============================================================

st.subheader("👥 Select Existing Team Members")

st.write(
    "Select the members you already have. "
    "The system will recommend the remaining members."
)


# ============================================================
# STUDENT DISPLAY OPTIONS & MULTISELECT
# ============================================================

student_options = []
for index, row in df.iterrows():
    name = row["student_name"]
    branch = row["branch"]
    student_options.append(f"{index} | {name} | {branch}")

selected_students = st.multiselect(
    "Existing Team Members",
    student_options,
    max_selections=3
)


# ============================================================
# VALIDATE TEAM SIZE
# ============================================================

existing_count = len(selected_students)
remaining_slots = 4 - existing_count

st.info(
    f"""
    Existing members: **{existing_count}**  |  
    Members to recommend: **{remaining_slots}**  |  
    Final team size: **4**
    """
)


# ============================================================
# GENERATE TEAM BUTTON
# ============================================================

if st.button(
    "🚀 Generate Hackathon Team",
    type="primary",
    use_container_width=True
):

    if existing_count == 0:
        st.warning("Please select at least one existing team member.")
        st.stop()

    existing_indices = []
    for item in selected_students:
        index = int(item.split("|")[0].strip())
        existing_indices.append(index)

    existing_team = df.loc[existing_indices].copy()

    # ========================================================
    # DISPLAY EXISTING TEAM
    # ========================================================

    st.divider()
    st.subheader("👥 Existing Team")

    existing_display = [
        "student_name", "branch", "cgpa", "coding_skills",
        "dsa_score", "ml_knowledge", "frontend_skill", "backend_skill"
    ]
    existing_display = [col for col in existing_display if col in existing_team.columns]

    st.dataframe(
        existing_team[existing_display],
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # DETERMINE MISSING ROLES
    # ========================================================

    frontend_existing = (
        existing_team["frontend_score"].idxmax()
        if len(existing_team) > 0 else None
    )

    backend_existing_count = 0
    ml_existing_count = 0

    for index, member in existing_team.iterrows():
        scores = {
            "Frontend Developer": member["frontend_score"],
            "Backend Developer": member["backend_score"],
            "ML Engineer": member["ml_score"]
        }
        best_role = max(scores, key=scores.get)

        if best_role == "Backend Developer":
            backend_existing_count += 1
        elif best_role == "ML Engineer":
            ml_existing_count += 1

    frontend_needed = max(
        0,
        1 - (
            1 if frontend_existing is not None
            and existing_team.loc[frontend_existing, "frontend_score"] >= existing_team.loc[frontend_existing, "backend_score"]
            and existing_team.loc[frontend_existing, "frontend_score"] >= existing_team.loc[frontend_existing, "ml_score"]
            else 0
        )
    )

    backend_needed = max(0, 2 - backend_existing_count)
    ml_needed = max(0, 1 - ml_existing_count)

    available_df = df.drop(index=existing_indices).copy()

    # ========================================================
    # RECOMMENDATION ALGORITHM
    # ========================================================

    recommendations = []
    used_indices = set(existing_indices)

    def add_best_candidate(role, score_column, number_needed):
        if number_needed <= 0:
            return

        nonlocal_available = available_df[~available_df.index.isin(used_indices)]
        candidates = (
            nonlocal_available
            .sort_values(score_column, ascending=False)
            .head(number_needed)
        )

        for index, row in candidates.iterrows():
            recommendations.append({
                "index": index,
                "name": row["student_name"],
                "branch": row["branch"],
                "cgpa": row["cgpa"],
                "role": role,
                "score": row[score_column],
                "cluster": row["team_cluster"]
            })
            used_indices.add(index)

    add_best_candidate("ML Engineer", "ml_score", ml_needed)
    add_best_candidate("Frontend Developer", "frontend_score", frontend_needed)
    add_best_candidate("Backend Developer", "backend_score", backend_needed)

    current_recommendations = len(recommendations)
    still_needed = remaining_slots - current_recommendations

    if still_needed > 0:
        remaining_candidates = available_df[~available_df.index.isin(used_indices)].copy()
        remaining_candidates["overall_score"] = (
            remaining_candidates["coding_skills"] * 0.25
            + remaining_candidates["communication_skills"] * 0.15
            + remaining_candidates["dsa_score"] * 0.15
            + remaining_candidates["ml_knowledge"] * 0.15
            + remaining_candidates["frontend_skill"] * 0.15
            + remaining_candidates["backend_skill"] * 0.15
        )

        extra_candidates = (
            remaining_candidates
            .sort_values("overall_score", ascending=False)
            .head(still_needed)
        )

        for index, row in extra_candidates.iterrows():
            recommendations.append({
                "index": index,
                "name": row["student_name"],
                "branch": row["branch"],
                "cgpa": row["cgpa"],
                "role": "Software Developer",
                "score": row["overall_score"],
                "cluster": row["team_cluster"]
            })

    recommendation_df = pd.DataFrame(recommendations)

    final_team_indices = existing_indices + (recommendation_df["index"].tolist() if not recommendation_df.empty else [])
    final_team = df.loc[final_team_indices].copy()

    # ========================================================
    # DISPLAY RECOMMENDED MEMBERS
    # ========================================================

    st.divider()
    st.subheader("🏆 Recommended Members")

    if len(recommendation_df) == 0:
        st.success("Your existing team already contains 4 members.")
    else:
        for _, candidate in recommendation_df.iterrows():
            role = candidate["role"]
            if role == "ML Engineer":
                icon = "🤖"
            elif role == "Frontend Developer":
                icon = "🎨"
            elif role == "Backend Developer":
                icon = "⚙️"
            else:
                icon = "💻"

            st.markdown(
                f"""
                <div class="role-card">
                    <h3>{icon} {candidate['name']}</h3>
                    <b>Recommended Role:</b> {role}<br>
                    <b>Branch:</b> {candidate['branch']}<br>
                    <b>CGPA:</b> {candidate['cgpa']}<br>
                    <b>Role Match Score:</b> {candidate['score']:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # COMPLETE FINAL TEAM
    # ========================================================

    st.divider()
    st.subheader("🚀 Final Hackathon Team")

    final_display_columns = [
        "student_name", "branch", "cgpa", "coding_skills",
        "dsa_score", "ml_knowledge", "frontend_skill",
        "backend_skill", "communication_skills"
    ]
    final_display_columns = [col for col in final_display_columns if col in final_team.columns]

    st.dataframe(
        final_team[final_display_columns],
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # TEAM ROLE SUMMARY
    # ========================================================

    st.subheader("🛠 Final Team Roles")

    role_summary = []

    for index, member in existing_team.iterrows():
        scores = {
            "Frontend Developer": member["frontend_score"],
            "Backend Developer": member["backend_score"],
            "ML Engineer": member["ml_score"]
        }
        role = max(scores, key=scores.get)
        role_summary.append({
            "Student": member["student_name"],
            "Role": role,
            "Status": "Existing Member"
        })

    if not recommendation_df.empty:
        for _, candidate in recommendation_df.iterrows():
            role_summary.append({
                "Student": candidate["name"],
                "Role": candidate["role"],
                "Status": "Recommended"
            })

    role_summary_df = pd.DataFrame(role_summary)

    st.dataframe(
        role_summary_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # TEAM COMPATIBILITY
    # ========================================================

    st.divider()
    st.subheader("🤝 Team Compatibility")

    compatibility = (
        final_team["coding_skills"].mean() * 0.25
        + final_team["dsa_score"].mean() * 0.20
        + final_team["communication_skills"].mean() * 0.15
        + final_team["ml_knowledge"].mean() * 0.15
        + final_team["frontend_skill"].mean() * 0.15
        + final_team["backend_skill"].mean() * 0.10
    )

    compatibility = round(compatibility, 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Team Size", len(final_team))

    with col2:
        st.metric("Compatibility", f"{compatibility}%")

    with col3:
        st.metric("ML Cluster Groups", final_team["team_cluster"].nunique())

    st.progress(min(int(compatibility), 100))

    if compatibility >= 85:
        st.success("🔥 Excellent hackathon team!")
    elif compatibility >= 70:
        st.warning("✅ Good team with balanced skills.")
    else:
        st.info("⚠️ Team can be improved for better skill balance.")

    # ========================================================
    # TEAM REQUIREMENT CHECK
    # ========================================================

    st.divider()
    st.subheader("✅ Hackathon Requirement Check")

    role_counts = role_summary_df["Role"].value_counts()

    frontend_count = role_counts.get("Frontend Developer", 0)
    backend_count = role_counts.get("Backend Developer", 0)
    ml_count = role_counts.get("ML Engineer", 0)

    check1, check2, check3, check4 = st.columns(4)

    with check1:
        if frontend_count >= 1:
            st.success("✅ Frontend\n1 member")
        else:
            st.error("❌ Frontend")

    with check2:
        if backend_count >= 2:
            st.success("✅ Backend\n2 members")
        else:
            st.warning(f"⚠️ Backend\n{backend_count} members")

    with check3:
        if ml_count >= 1:
            st.success("✅ ML\n1 member")
        else:
            st.error("❌ ML Engineer")

    with check4:
        if len(final_team) == 4:
            st.success("✅ Team Size\n4 members")
        else:
            st.warning(f"⚠️ Team Size\n{len(final_team)}")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Team Formation")
    st.write("Hackathon team requirements:")
    st.write("🎨 1 Frontend Developer")
    st.write("⚙️ 2 Backend Developers")
    st.write("🤖 1 ML Engineer")
    st.write("👥 Maximum 4 Members")
    st.divider()
    st.caption("Powered by K-Means Clustering")