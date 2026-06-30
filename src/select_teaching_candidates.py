import pandas as pd


INPUT_FILE = "data/project_features.csv"
OUTPUT_FILE = "data/teaching_candidates.csv"


def select_teaching_candidates(df):
    median_engagement = df["engagement_score"].median()
    median_complexity = df["complexity_score"].median()

    print(f"Median engagement score: {median_engagement}")
    print(f"Median complexity score: {median_complexity}")

    candidates = df[
        (df["engagement_score"] >= median_engagement)
        & (df["complexity_score"] <= median_complexity)
    ]

    return candidates


def main():
    df = pd.read_csv(INPUT_FILE)

    # Keep only projects where both scores exist
    df = df.dropna(subset=["engagement_score", "complexity_score"])

    candidates = select_teaching_candidates(df)

    candidates = candidates.sort_values(
        by=["engagement_score", "complexity_score"],
        ascending=[False, True]
    )

    candidates.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(candidates)} teaching candidates to {OUTPUT_FILE}")

    print(
        candidates[
            [
                "project_id",
                "title",
                "engagement_score",
                "complexity_score",
                "number_of_sprites",
                "number_of_blocks",
                "number_of_scripts",
                "scripts_per_sprite",
                "broadcasts",
                "clones",
                "custom_blocks",
            ]
        ]
    )


if __name__ == "__main__":
    main()