import pandas as pd


INPUT_FILE = "data/project_metadata.csv"
OUTPUT_FILE = "data/project_engagement_features.csv"


def safe_divide(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator


def add_engagement_features(df):
    df["love_rate"] = df.apply(
        lambda row: safe_divide(row["loves"], row["views"]),
        axis=1
    )

    df["favorite_rate"] = df.apply(
        lambda row: safe_divide(row["favorites"], row["views"]),
        axis=1
    )

    df["remix_rate"] = df.apply(
        lambda row: safe_divide(row["remix_count"], row["views"]),
        axis=1
    )

    df["engagement_score"] = (
        0.3 * df["love_rate"]
        + 0.4 * df["favorite_rate"]
        + 0.3 * df["remix_rate"]
    )

    return df


def main():
    df = pd.read_csv(INPUT_FILE)

    df = add_engagement_features(df)

    df = df.sort_values(by="engagement_score", ascending=False)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved engagement features to {OUTPUT_FILE}")
    print(
        df[
            [
                "project_id",
                "title",
                "views",
                "loves",
                "favorites",
                "remix_count",
                "love_rate",
                "favorite_rate",
                "remix_rate",
                "engagement_score",
            ]
        ]
    )


if __name__ == "__main__":
    main()