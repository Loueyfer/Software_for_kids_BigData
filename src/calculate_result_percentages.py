import pandas as pd


INPUT_FILE = "data/project_features.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    # Keep only projects with valid scores
    df = df.dropna(subset=["engagement_score", "complexity_score"])

    total_projects = len(df)

    median_engagement = df["engagement_score"].median()
    median_complexity = df["complexity_score"].median()

    high_engagement = df[df["engagement_score"] >= median_engagement]
    low_complexity = df[df["complexity_score"] <= median_complexity]

    both = df[
        (df["engagement_score"] >= median_engagement)
        & (df["complexity_score"] <= median_complexity)
    ]

    print("Total valid projects:", total_projects)
    print("Median engagement:", median_engagement)
    print("Median complexity:", median_complexity)

    print()
    print("High engagement projects:", len(high_engagement))
    print("High engagement percentage:", round(len(high_engagement) / total_projects * 100, 2), "%")

    print()
    print("Low complexity projects:", len(low_complexity))
    print("Low complexity percentage:", round(len(low_complexity) / total_projects * 100, 2), "%")

    print()
    print("Both high engagement and low complexity:", len(both))
    print("Both percentage:", round(len(both) / total_projects * 100, 2), "%")


if __name__ == "__main__":
    main()