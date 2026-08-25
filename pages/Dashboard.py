import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Placement Dashboard 3D",
    page_icon="📈",
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
    font-size: 48px;
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
    font-size: 32px !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 10px rgba(168, 85, 247, 0.4);
}

/* Glassmorphism Container wrapper for Plotly charts */
.stPlotlyChart {
    background: linear-gradient(135deg, rgba(24, 13, 38, 0.65), rgba(14, 7, 23, 0.85));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(192, 132, 252, 0.2);
    border-radius: 20px;
    box-shadow: 10px 10px 30px rgba(0,0,0,0.6), inset 1px 1px 1px rgba(255,255,255,0.05);
    padding: 10px;
    transition: transform 0.3s ease;
}

.stPlotlyChart:hover {
    border: 1px solid rgba(192, 132, 252, 0.45);
}

/* Custom Dataframe Container */
div[data-testid="stDataFrame"] {
    background: linear-gradient(145deg, #180d26, #0e0717) !important;
    border: 1px solid rgba(192, 132, 252, 0.25) !important;
    border-radius: 16px !important;
    padding: 10px !important;
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
# LOAD DATA
# =====================================
try:
    df = pd.read_csv("dataset/placement_data.csv")
except Exception:
    # Fallback dummy dataframe for preview if file path is missing
    df = pd.DataFrame({
        "cgpa": [7.5, 8.8, 6.2, 9.1, 7.0, 8.2, 5.9, 9.4],
        "placement_status": ["Placed", "Placed", "Not Placed", "Placed", "Not Placed", "Placed", "Not Placed", "Placed"],
        "projects_count": [2, 4, 1, 3, 2, 3, 1, 5],
        "internships": [1, 2, 0, 3, 0, 1, 0, 2],
        "coding_skills": [70, 85, 50, 95, 60, 80, 45, 90],
        "dsa_score": [65, 88, 55, 90, 62, 78, 40, 92],
        "aptitude_score": [72, 80, 60, 88, 65, 75, 50, 94],
        "communication_skills": [78, 82, 65, 90, 70, 85, 55, 88],
        "salary_package_lpa": [6.5, 12.0, None, 15.5, None, 9.0, None, 18.0]
    })

# =====================================
# DATA CLEANING
# =====================================
df["placement_status"] = df["placement_status"].astype(str).str.strip()
placed_students = df[df["placement_status"].isin(["1", "Placed"])]
not_placed_students = df[df["placement_status"].isin(["0", "Not Placed"])]

# =====================================
# HEADER
# =====================================
st.markdown('<p class="main-title">PLACEMENT ANALYTICS DASHBOARD</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ Next-Gen 3D Interactive Placement Insights</p>', unsafe_allow_html=True)

# =====================================
# KPI SECTION
# =====================================
total_students = len(df)
placed_count = len(placed_students)
not_placed_count = len(not_placed_students)
placement_rate = round((placed_count / total_students) * 100, 2) if total_students > 0 else 0
avg_cgpa = round(df["cgpa"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", f"{total_students:,}")
with col2:
    st.metric("Placed Students", f"{placed_count:,}")
with col3:
    st.metric("Placement Rate", f"{placement_rate}%")
with col4:
    st.metric("Average CGPA", avg_cgpa)

st.markdown("<hr>", unsafe_allow_html=True)

# Shared Plotly 3D Layout configuration helper
def get_3d_layout():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2d9f3", family="Sans-Serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(24, 13, 38, 0.5)", gridcolor="rgba(192, 132, 252, 0.15)", showbackground=True, zerolinecolor="rgba(192, 132, 252, 0.3)"),
            yaxis=dict(backgroundcolor="rgba(24, 13, 38, 0.5)", gridcolor="rgba(192, 132, 252, 0.15)", showbackground=True, zerolinecolor="rgba(192, 132, 252, 0.3)"),
            zaxis=dict(backgroundcolor="rgba(24, 13, 38, 0.5)", gridcolor="rgba(192, 132, 252, 0.15)", showbackground=True, zerolinecolor="rgba(192, 132, 252, 0.3)"),
        )
    )

# =====================================
# ROW 1: CHARTS (DONUT & 3D SCATTER)
# =====================================
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<p class="section-title">Placement Ratio</p>', unsafe_allow_html=True)
    
    # 3D Depth Donut Chart with purple and neon pink color scheme
    fig1 = go.Figure(data=[go.Pie(
        labels=["Placed", "Not Placed"],
        values=[placed_count, not_placed_count],
        hole=0.6,
        pull=[0.08, 0],
        marker=dict(
            colors=["#c084fc", "#ff4b6e"],
            line=dict(color="#0a0512", width=3)
        ),
        textinfo="label+percent",
        hoverinfo="label+value+percent"
    )])
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2d9f3", showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.markdown('<p class="section-title">3D Analysis: Projects vs CGPA vs Internships</p>', unsafe_allow_html=True)
    
    # True 3D Scatter Plot (Interactive Orbit/Zoom)
    fig4 = px.scatter_3d(
        df,
        x="projects_count",
        y="cgpa",
        z="internships",
        color="placement_status",
        hover_data=["coding_skills"] if "coding_skills" in df.columns else None,
        color_discrete_map={"Placed": "#c084fc", "1": "#c084fc", "Not Placed": "#ff4b6e", "0": "#ff4b6e"},
        opacity=0.85
    )
    fig4.update_traces(marker=dict(size=6, line=dict(width=0.5, color="white")))
    fig4.update_layout(get_3d_layout())
    st.plotly_chart(fig4, use_container_width=True)

# =====================================
# ROW 2: CGPA & SKILL ANALYTICS
# =====================================
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<p class="section-title">CGPA Distribution</p>', unsafe_allow_html=True)
    
    fig2 = px.histogram(
        df,
        x="cgpa",
        nbins=25,
        color_discrete_sequence=["#c084fc"]
    )
    fig2.update_traces(marker=dict(line=dict(width=1, color='#0a0512')))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2d9f3",
        xaxis=dict(gridcolor="rgba(192,132,252,0.1)"),
        yaxis=dict(gridcolor="rgba(192,132,252,0.1)")
    )
    st.plotly_chart(fig2, use_container_width=True)

with row2_col2:
    st.markdown('<p class="section-title">Average Skill Scores</p>', unsafe_allow_html=True)
    
    skill_columns = [col for col in ["coding_skills", "dsa_score", "aptitude_score", "communication_skills"] if col in df.columns]
    
    if skill_columns:
        skill_df = pd.DataFrame({
            "Skill": skill_columns,
            "Average Score": df[skill_columns].mean()
        })

        fig5 = px.bar(
            skill_df,
            x="Skill",
            y="Average Score",
            color="Average Score",
            color_continuous_scale=["#3b0764", "#c084fc", "#e9d5ff"]
        )
        fig5.update_traces(marker=dict(line=dict(width=1, color='#a855f7')))
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2d9f3",
            xaxis=dict(gridcolor="rgba(192,132,252,0.1)"),
            yaxis=dict(gridcolor="rgba(192,132,252,0.1)")
        )
        st.plotly_chart(fig5, use_container_width=True)

# =====================================
# SALARY ANALYSIS (IF AVAILABLE)
# =====================================
if "salary_package_lpa" in df.columns:
    salary_df = df.dropna(subset=["salary_package_lpa"])
    if not salary_df.empty:
        st.markdown('<p class="section-title">Salary Distribution (LPA)</p>', unsafe_allow_html=True)

        fig6 = px.histogram(
            salary_df,
            x="salary_package_lpa",
            nbins=30,
            color_discrete_sequence=["#d8b4fe"]
        )
        fig6.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2d9f3",
            xaxis=dict(gridcolor="rgba(192,132,252,0.1)"),
            yaxis=dict(gridcolor="rgba(192,132,252,0.1)")
        )
        st.plotly_chart(fig6, use_container_width=True)

# =====================================
# DATA PREVIEW
# =====================================
st.markdown('<p class="section-title">Dataset Preview</p>', unsafe_allow_html=True)
st.dataframe(df.head(20), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.success("Dashboard Loaded Successfully")
st.caption("Placement Analytics Dashboard | Streamlit 3D Purple Edition")