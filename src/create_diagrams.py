import os

import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "data/project_features.csv"
RESULTS_DIR = "results"


def load_data():
    """
    Load the final project features dataset.
    This file contains both engagement_score and complexity_score.
    """
    df = pd.read_csv(INPUT_FILE)

    # Remove projects where one of the needed scores is missing
    df = df.dropna(subset=["engagement_score", "complexity_score"])

    return df


def create_engagement_complexity_scatter(df):
    """
    Create a scatter plot showing the relationship between
    complexity score and engagement score.
    """

    median_engagement = df["engagement_score"].median()
    median_complexity = df["complexity_score"].median()

    plt.figure(figsize=(10, 6))

    # Each point is one Scratch project
    plt.scatter(
        df["complexity_score"],
        df["engagement_score"],
        alpha=0.7
    )
    
    # Median lines
    plt.axvline(
        median_complexity,
        linestyle="--",
        label="Median complexity"
    )

    plt.axhline(
        median_engagement,
        linestyle="--",
        label="Median engagement"
    )

    plt.title("Engagement vs. Complexity of Scratch Projects")
    plt.xlabel("Complexity Score")
    plt.ylabel("Engagement Score")

    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(
        RESULTS_DIR,
        "engagement_vs_complexity_scatter.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved diagram: {output_path}")

def create_category_counts(df):
    """
    Create a bar chart showing how many projects belong to each
    engagement-complexity category.
    """

    median_engagement = df["engagement_score"].median()
    median_complexity = df["complexity_score"].median()

    high_engagement = df["engagement_score"] >= median_engagement
    low_complexity = df["complexity_score"] <= median_complexity

    categories = {
        "High engagement\nLow complexity": len(df[high_engagement & low_complexity]),
        "High engagement\nHigh complexity": len(df[high_engagement & ~low_complexity]),
        "Low engagement\nLow complexity": len(df[~high_engagement & low_complexity]),
        "Low engagement\nHigh complexity": len(df[~high_engagement & ~low_complexity]),
    }

    plt.figure(figsize=(10, 6))

    plt.bar(categories.keys(), categories.values())

    plt.title("Project Categories by Engagement and Complexity")
    plt.xlabel("Category")
    plt.ylabel("Number of Projects")

    # Add numbers above bars
    for index, value in enumerate(categories.values()):
        plt.text(index, value + 0.5, str(value), ha="center")

    plt.tight_layout()

    output_path = os.path.join(
        RESULTS_DIR,
        "category_counts.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved diagram: {output_path}")

def create_result_percentages(df):
    """
    Create a bar chart showing the percentage of projects with:
    - high engagement
    - low complexity
    - both high engagement and low complexity
    """

    median_engagement = df["engagement_score"].median()
    median_complexity = df["complexity_score"].median()

    total_projects = len(df)

    high_engagement = df["engagement_score"] >= median_engagement
    low_complexity = df["complexity_score"] <= median_complexity
    both = high_engagement & low_complexity

    percentages = {
        "High engagement": (high_engagement.sum() / total_projects) * 100,
        "Low complexity": (low_complexity.sum() / total_projects) * 100,
        "High engagement\nLow complexity": (both.sum() / total_projects) * 100,
    }

    plt.figure(figsize=(8, 6))

    plt.bar(percentages.keys(), percentages.values())

    plt.title("Percentage of Projects by Selection Criteria")
    plt.xlabel("Criterion")
    plt.ylabel("Percentage of Projects")

    plt.ylim(0, 100)

    # Add percentage labels above bars
    for index, value in enumerate(percentages.values()):
        plt.text(index, value + 2, f"{value:.1f}%", ha="center")

    plt.tight_layout()

    output_path = os.path.join(
        RESULTS_DIR,
        "result_percentages.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved diagram: {output_path}")

def create_candidate_themes():
    """
    Create a bar chart showing how many selected teaching candidates
    belong to each Scratch project theme.
    """

    candidates_df = pd.read_csv("data/teaching_candidates.csv")

    # Remove rows where the theme is missing
    candidates_df = candidates_df.dropna(subset=["theme"])

    theme_counts = candidates_df["theme"].value_counts()

    plt.figure(figsize=(8, 6))

    plt.bar(theme_counts.index, theme_counts.values)

    plt.title("Themes of Selected Teaching Candidates")
    plt.xlabel("Theme")
    plt.ylabel("Number of Candidate Projects")

    # Add numbers above bars
    for index, value in enumerate(theme_counts.values):
        plt.text(index, value + 0.2, str(value), ha="center")

    plt.tight_layout()

    output_path = os.path.join(
        RESULTS_DIR,
        "candidate_themes.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved diagram: {output_path}")

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    df = load_data()

    create_engagement_complexity_scatter(df)
    create_category_counts(df)
    create_result_percentages(df)
    create_candidate_themes()
if __name__ == "__main__":
    main()