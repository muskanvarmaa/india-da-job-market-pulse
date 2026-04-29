import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="India DA Job Market Pulse",
    page_icon="📊",
    layout="wide"
)

# ---- CSS ----
st.markdown("""
<style>
.main { background-color: #0f0f1a !important; }
.block-container { padding: 1.5rem 2rem !important; }

[data-testid="stSidebar"] {
    background-color: #12122a !important;
    border-right: 1px solid #2a2a40;
}

[data-testid="stMetric"] {
    background: #1a1a2e;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    box-shadow: 0 4px 15px rgba(127, 119, 221, 0.1);
}

[data-testid="stMetricLabel"] {
    color: #888 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 600 !important;
}

h1 {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #7F77DD, #1D9E75);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 { color: #ffffff !important; }

[data-testid="stSelectbox"] > div {
    background: #1a1a2e !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 8px !important;
    color: white !important;
}

hr { border-color: #2a2a40 !important; }
</style>
""", unsafe_allow_html=True)

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect("jobs.db")
        df = pd.read_sql("SELECT * FROM jobs", conn)
        conn.close()
    except:
        df = pd.read_csv("data/sample_jobs.csv")
    return df

df = load_data()

# ---- SKILLS PROCESSING ----
@st.cache_data
def get_skills(df):
    all_skills = []
    for skills_str in df['skills']:
        if pd.notna(skills_str):
            for s in skills_str.split(","):
                all_skills.append(s.strip().lower())
    skills_df = pd.Series(all_skills).value_counts().reset_index()
    skills_df.columns = ['skill', 'count']
    return skills_df

# ---- SIDEBAR FILTERS ----
st.sidebar.title("🔍 Filters")
cities = ['All'] + sorted(df['location'].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("City", cities)

experiences = ['All'] + sorted(df['experience'].dropna().unique().tolist())
selected_exp = st.sidebar.selectbox("Experience", experiences)

# ---- FILTER DATA ----
filtered_df = df.copy()
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_city]
if selected_exp != 'All':
    filtered_df = filtered_df[filtered_df['experience'] == selected_exp]

# ---- HEADER ----
st.title("🇮🇳 India DA Job Market Pulse")
st.markdown(f"**{len(filtered_df):,} job postings** scraped from Naukri.com · Auto-updated weekly")
st.markdown("---")

# ---- METRIC CARDS ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Jobs", f"{len(filtered_df):,}")
with col2:
    top_city = filtered_df['location'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
    st.metric("Top City", top_city)
with col3:
    fresher = len(filtered_df[filtered_df['experience'].str.contains('0-2', na=False)])
    pct = round(fresher/len(filtered_df)*100) if len(filtered_df) > 0 else 0
    st.metric("Fresher Friendly", f"{pct}%")
with col4:
    remote = len(filtered_df[filtered_df['location'].str.contains('Remote', na=False)])
    st.metric("Remote Jobs", f"{remote}")

st.markdown("---")

# ---- ROW 1: CITIES + SKILLS ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Top Cities Hiring")
    city_counts = filtered_df['location'].value_counts().head(15).reset_index()
    city_counts.columns = ['city', 'count']
    fig1 = px.bar(
        city_counts,
        x='count', y='city',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        title="Job Count by City"
    )
    fig1.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🛠️ Top Skills in Demand")
    skills_df = get_skills(filtered_df)
    fig2 = px.bar(
        skills_df.head(15),
        x='count', y='skill',
        orientation='h',
        color='count',
        color_continuous_scale='Purples',
        title="Most Demanded Skills"
    )
    fig2.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---- ROW 2: EXPERIENCE + COMPANIES ----
col3, col4 = st.columns(2)

with col3:
    st.subheader("📅 Experience Distribution")
    exp_counts = filtered_df['experience'].value_counts().head(10).reset_index()
    exp_counts.columns = ['experience', 'count']
    fig3 = px.bar(
        exp_counts,
        x='experience', y='count',
        color='count',
        color_continuous_scale='Teal',
        title="Jobs by Experience Level"
    )
    fig3.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🏢 Top Hiring Companies")
    company_counts = filtered_df['company'].value_counts().head(15).reset_index()
    company_counts.columns = ['company', 'count']
    fig4 = px.treemap(
        company_counts,
        path=['company'],
        values='count',
        color='count',
        color_continuous_scale='Blues',
        title="Companies Hiring Most"
    )
    fig4.update_layout(
        paper_bgcolor='#1a1a2e',
        font_color='white',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---- KEY INSIGHTS ----
st.markdown("---")
st.subheader("💡 Key Findings")

col1, col2 = st.columns(2)
with col1:
    st.success("**Pune = Bengaluru for DA jobs** — 23 vs 24 openings. No need to relocate!")
    st.info("**SQL beats Python** — SQL appears in 36 postings vs Python in 20. SQL is non-negotiable.")
with col2:
    st.warning("**Market is fresher friendly** — 52% of roles open to 0-2 yrs experience.")
    st.error("**Remote is real** — 12% of all DA roles are remote. Work from anywhere.")

# ---- RAW DATA TABLE ----
st.markdown("---")
st.subheader("🔎 Explore Raw Jobs")
st.dataframe(
    filtered_df[['title', 'company', 'experience', 'salary', 'location', 'skills', 'posted']],
    use_container_width=True,
    height=300
)