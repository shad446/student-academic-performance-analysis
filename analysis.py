import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("StudentsPerformance.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nBasic statistics:")
print(df.describe())
# ==========================================
# 2. CREATE AVERAGE SCORE
# ==========================================

df["Average Score"] = (
    df["math score"] +
    df["reading score"] +
    df["writing score"]
) / 3

print("\nAverage Score created successfully!")

print("\nAverage Score Statistics:")
print(df["Average Score"].describe())
# ==========================================
# 3. KEY ACADEMIC PERFORMANCE KPIs
# ==========================================

total_students = len(df)

average_math = df["math score"].mean()
average_reading = df["reading score"].mean()
average_writing = df["writing score"].mean()
overall_average = df["Average Score"].mean()

highest_average = df["Average Score"].max()
lowest_average = df["Average Score"].min()

print("\n==========================================")
print("     KEY ACADEMIC PERFORMANCE KPIs")
print("==========================================")

print(f"Total Students: {total_students:,}")
print(f"Average Math Score: {average_math:.2f}")
print(f"Average Reading Score: {average_reading:.2f}")
print(f"Average Writing Score: {average_writing:.2f}")
print(f"Overall Average Score: {overall_average:.2f}")
print(f"Highest Average Score: {highest_average:.2f}")
print(f"Lowest Average Score: {lowest_average:.2f}")

print("==========================================")
# ==========================================
# 4. PERFORMANCE BY GENDER
# ==========================================

gender_performance = (
    df.groupby("gender")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE PERFORMANCE BY GENDER:")
print(gender_performance)

# Create chart
plt.figure(figsize=(8, 5))

gender_performance.plot(kind="bar")

plt.title("Average Academic Performance by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

# Add values above bars
for i, value in enumerate(gender_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "performance_by_gender.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 5. PERFORMANCE BY PARENTAL EDUCATION
# ==========================================

parental_performance = (
    df.groupby("parental level of education")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE PERFORMANCE BY PARENTAL EDUCATION:")
print(parental_performance)

# Create chart
plt.figure(figsize=(10, 6))

parental_performance.plot(kind="bar")

plt.title("Average Academic Performance by Parental Education")
plt.xlabel("Parental Level of Education")
plt.ylabel("Average Score")
plt.xticks(rotation=45, ha="right")

# Add values
for i, value in enumerate(parental_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "performance_by_parental_education.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 6. PERFORMANCE BY TEST PREPARATION
# ==========================================

test_prep_performance = (
    df.groupby("test preparation course")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE PERFORMANCE BY TEST PREPARATION:")
print(test_prep_performance)

# Create chart
plt.figure(figsize=(8, 5))

test_prep_performance.plot(kind="bar")

plt.title("Average Academic Performance by Test Preparation")
plt.xlabel("Test Preparation Course")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

# Add values
for i, value in enumerate(test_prep_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "performance_by_test_preparation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 7. SUBJECT PERFORMANCE COMPARISON
# ==========================================

subject_averages = {
    "Math": df["math score"].mean(),
    "Reading": df["reading score"].mean(),
    "Writing": df["writing score"].mean()
}

subject_performance = pd.Series(subject_averages).sort_values(ascending=False)

print("\nAVERAGE SCORE BY SUBJECT:")
print(subject_performance)

# Create chart
plt.figure(figsize=(8, 5))

subject_performance.plot(kind="bar")

plt.title("Average Score by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

# Add values
for i, value in enumerate(subject_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "average_score_by_subject.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 8. PERFORMANCE BY LUNCH TYPE
# ==========================================

lunch_performance = (
    df.groupby("lunch")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE PERFORMANCE BY LUNCH TYPE:")
print(lunch_performance)

# Create chart
plt.figure(figsize=(8, 5))

lunch_performance.plot(kind="bar")

plt.title("Average Academic Performance by Lunch Type")
plt.xlabel("Lunch Type")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

# Add values
for i, value in enumerate(lunch_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "performance_by_lunch.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 9. HIGH AND LOW PERFORMING STUDENTS
# ==========================================

# Top 10 students
top_students = (
    df.sort_values("Average Score", ascending=False)
    .head(10)
)

print("\nTOP 10 HIGH-PERFORMING STUDENTS:")
print(
    top_students[
        ["gender", "race/ethnicity", "parental level of education",
         "test preparation course", "Average Score"]
    ]
)

# Bottom 10 students
bottom_students = (
    df.sort_values("Average Score", ascending=True)
    .head(10)
)

print("\nBOTTOM 10 PERFORMING STUDENTS:")
print(
    bottom_students[
        ["gender", "race/ethnicity", "parental level of education",
         "test preparation course", "Average Score"]
    ]
)

# Save results
top_students.to_csv("top_10_students.csv", index=False)
bottom_students.to_csv("bottom_10_students.csv", index=False)

print("\nTop and bottom student files saved successfully!")
# ==========================================
# 10. CORRELATION ANALYSIS
# ==========================================

correlation_data = df[
    ["math score", "reading score", "writing score", "Average Score"]
]

correlation_matrix = correlation_data.corr()

print("\nCORRELATION MATRIX:")
print(correlation_matrix)

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Between Academic Scores")

plt.tight_layout()

plt.savefig(
    "score_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 11. PERFORMANCE BY RACE/ETHNICITY
# ==========================================

race_performance = (
    df.groupby("race/ethnicity")["Average Score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE PERFORMANCE BY RACE/ETHNICITY:")
print(race_performance)

# Create chart
plt.figure(figsize=(8, 5))

race_performance.plot(kind="bar")

plt.title("Average Academic Performance by Race/Ethnicity")
plt.xlabel("Race/Ethnicity")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

# Add values
for i, value in enumerate(race_performance):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
plt.savefig(
    "performance_by_race_ethnicity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 12. SCORE DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["Average Score"],
    bins=10,
    edgecolor="black"
)

plt.title("Distribution of Average Student Scores")
plt.xlabel("Average Score")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig(
    "average_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nScore distribution chart saved successfully!")