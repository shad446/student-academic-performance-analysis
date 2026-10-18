import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Student Academic Performance",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# DARK THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

[data-testid="stMetricValue"] {
    color: #38BDF8;
}

h1 {
    color: #38BDF8;
}

h2, h3 {
    color: #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("StudentsPerformance.csv")

# Create Average Score
df["Average Score"] = (
    df["math score"] +
    df["reading score"] +
    df["writing score"]
) / 3

# ==========================================
# TITLE
# ==========================================

st.title("🎓 Student Academic Performance Dashboard")

st.write(
    "Interactive analysis of student academic performance "
    "and related factors."
)

# ==========================================
# KPI CARDS
# ==========================================

total_students = len(df)
overall_average = df["Average Score"].mean()
average_math = df["math score"].mean()
average_reading = df["reading score"].mean()
average_writing = df["writing score"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👨‍🎓 Total Students", f"{total_students:,}")
col2.metric("📊 Overall Average", f"{overall_average:.2f}")
col3.metric("➗ Math Average", f"{average_math:.2f}")
col4.metric("📖 Reading Average", f"{average_reading:.2f}")
col5.metric("✍️ Writing Average", f"{average_writing:.2f}")
# ==========================================
# SIDEBAR FILTERS
# ==========================================
# ==========================================
# APPLY FILTERS
# ==========================================

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🎛️ Dashboard Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

race_filter = st.sidebar.multiselect(
    "Race/Ethnicity",
    options=df["race/ethnicity"].unique(),
    default=df["race/ethnicity"].unique()
)

parental_filter = st.sidebar.multiselect(
    "Parental Education",
    options=df["parental level of education"].unique(),
    default=df["parental level of education"].unique()
)

lunch_filter = st.sidebar.multiselect(
    "Lunch",
    options=df["lunch"].unique(),
    default=df["lunch"].unique()
)

test_prep_filter = st.sidebar.multiselect(
    "Test Preparation",
    options=df["test preparation course"].unique(),
    default=df["test preparation course"].unique()
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["race/ethnicity"].isin(race_filter)) &
    (df["parental level of education"].isin(parental_filter)) &
    (df["lunch"].isin(lunch_filter)) &
    (df["test preparation course"].isin(test_prep_filter))
]


# ==========================================
# FILTERED DATA
# ==========================================

st.subheader("📋 Filtered Student Data")

st.write(f"Showing **{len(filtered_df):,} students**")

st.dataframe(
    filtered_df,
    use_container_width=True
)# ==========================================
# SUBJECT PERFORMANCE
# ==========================================

st.subheader("📊 Average Score by Subject")

subject_averages = {
    "Math": filtered_df["math score"].mean(),
    "Reading": filtered_df["reading score"].mean(),
    "Writing": filtered_df["writing score"].mean()
}

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    subject_averages.keys(),
    subject_averages.values()
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Score by Subject")

for i, value in enumerate(subject_averages.values()):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

st.pyplot(fig)# ==========================================
# PERFORMANCE BY GENDER
# ==========================================

st.subheader("👥 Average Performance by Gender")

gender_performance = (
    filtered_df.groupby("gender")["Average Score"]
    .mean()
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    gender_performance.index,
    gender_performance.values
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Academic Performance by Gender")

for i, value in enumerate(gender_performance.values):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

st.pyplot(fig)# ==========================================
# PERFORMANCE BY PARENTAL EDUCATION
# ==========================================

st.subheader("🎓 Performance by Parental Education")

parental_performance = (
    filtered_df.groupby("parental level of education")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    parental_performance.index,
    parental_performance.values
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Performance by Parental Education")

plt.xticks(rotation=35, ha="right")

for i, value in enumerate(parental_performance.values):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

plt.tight_layout()

st.pyplot(fig)# ==========================================
# PERFORMANCE BY TEST PREPARATION
# ==========================================

st.subheader("📚 Performance by Test Preparation")

test_prep_performance = (
    filtered_df.groupby("test preparation course")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    test_prep_performance.index,
    test_prep_performance.values
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Performance by Test Preparation")

for i, value in enumerate(test_prep_performance.values):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

st.pyplot(fig)
# ==========================================
# SCORE DISTRIBUTION
# ==========================================

st.subheader("📈 Distribution of Average Scores")

fig, ax = plt.subplots(figsize=(9, 4))

ax.hist(
    filtered_df["Average Score"],
    bins=10,
    edgecolor="black"
)

ax.set_xlabel("Average Score")
ax.set_ylabel("Number of Students")
ax.set_title("Distribution of Average Student Scores")

st.pyplot(fig)# ==========================================
# PERFORMANCE BY LUNCH TYPE
# ==========================================

st.subheader("🍱 Performance by Lunch Type")

lunch_performance = (
    filtered_df.groupby("lunch")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    lunch_performance.index,
    lunch_performance.values
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Performance by Lunch Type")

for i, value in enumerate(lunch_performance.values):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

st.pyplot(fig)# ==========================================
# PERFORMANCE BY RACE/ETHNICITY
# ==========================================

st.subheader("🌍 Performance by Race/Ethnicity")

race_performance = (
    filtered_df.groupby("race/ethnicity")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    race_performance.index,
    race_performance.values
)

ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)
ax.set_title("Average Performance by Race/Ethnicity")

for i, value in enumerate(race_performance.values):
    ax.text(
        i,
        value + 1,
        f"{value:.1f}",
        ha="center"
    )

st.pyplot(fig)# ==========================================
# CORRELATION HEATMAP
# ==========================================

st.subheader("🔗 Correlation Between Subject Scores")

correlation_data = filtered_df[
    ["math score", "reading score", "writing score"]
]

correlation_matrix = correlation_data.corr()

fig, ax = plt.subplots(figsize=(7, 5))

im = ax.imshow(correlation_matrix)

ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_yticks(range(len(correlation_matrix.columns)))

ax.set_xticklabels(correlation_matrix.columns)
ax.set_yticklabels(correlation_matrix.columns)

plt.setp(
    ax.get_xticklabels(),
    rotation=45,
    ha="right"
)

for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix.columns)):
        ax.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

ax.set_title("Correlation Between Academic Subjects")

fig.colorbar(im)

plt.tight_layout()

st.pyplot(fig)