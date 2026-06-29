import time

import pandas as pd
import requests


INPUT_FILE = "data/project_engagement_features.csv"
OUTPUT_FILE = "data/project_features.csv"


def safe_divide(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator


def get_project_token(project_id):
    metadata_url = f"https://api.scratch.mit.edu/projects/{project_id}"

    response = requests.get(metadata_url, timeout=15)
    response.raise_for_status()

    metadata = response.json()
    return metadata.get("project_token")


def get_project_structure(project_id):
    token = get_project_token(project_id)

    if token is None:
        raise ValueError(f"No project token found for project {project_id}")

    structure_url = f"https://projects.scratch.mit.edu/{project_id}?token={token}"

    response = requests.get(structure_url, timeout=20)
    response.raise_for_status()

    return response.json()


def count_complexity_features(project_structure):
    targets = project_structure.get("targets", [])

    number_of_sprites = 0
    number_of_blocks = 0
    number_of_scripts = 0

    broadcasts = 0
    clones = 0
    custom_blocks = 0

    for target in targets:
        # Stage is not counted as a sprite
        if not target.get("isStage", False):
            number_of_sprites += 1

        blocks = target.get("blocks", {})
        number_of_blocks += len(blocks)

        for block in blocks.values():
            # Sometimes Scratch blocks can contain non-dictionary values
            if not isinstance(block, dict):
                continue

            opcode = block.get("opcode", "")

            # A top-level block usually starts a script
            if block.get("topLevel", False):
                number_of_scripts += 1

            # Broadcast-related blocks
            if opcode in [
                "event_broadcast",
                "event_broadcastandwait",
                "event_whenbroadcastreceived",
            ]:
                broadcasts += 1

            # Clone-related blocks
            if opcode in [
                "control_create_clone_of",
                "control_delete_this_clone",
                "control_start_as_clone",
            ]:
                clones += 1

            # Custom block / procedure blocks
            if opcode in [
                "procedures_definition",
                "procedures_call",
            ]:
                custom_blocks += 1

    scripts_per_sprite = safe_divide(number_of_scripts, number_of_sprites)

    advanced_feature_count = broadcasts + clones + custom_blocks

    complexity_score = (
        number_of_blocks
        + (10 * number_of_sprites)
        + (20 * scripts_per_sprite)
        + (30 * advanced_feature_count)
    )

    return {
        "project_id": None,
        "number_of_sprites": number_of_sprites,
        "number_of_blocks": number_of_blocks,
        "number_of_scripts": number_of_scripts,
        "scripts_per_sprite": scripts_per_sprite,
        "broadcasts": broadcasts,
        "clones": clones,
        "custom_blocks": custom_blocks,
        "advanced_feature_count": advanced_feature_count,
        "complexity_score": complexity_score,
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    complexity_rows = []

    for _, row in df.iterrows():
        project_id = row["project_id"]
        print(f"Extracting complexity features for project {project_id}")

        try:
            project_structure = get_project_structure(project_id)
            complexity_features = count_complexity_features(project_structure)

            complexity_features["project_id"] = project_id
            complexity_rows.append(complexity_features)

        except (requests.RequestException, ValueError) as error:
            print(f"Could not extract complexity for project {project_id}: {error}")

        time.sleep(0.5)

    if not complexity_rows:
        print("No complexity features were extracted. No output file was created.")
        return

    complexity_df = pd.DataFrame(complexity_rows)

    final_df = df.merge(complexity_df, on="project_id", how="left")

    final_df = final_df.dropna(subset=["complexity_score"])

    final_df = final_df[final_df["number_of_blocks"] > 0]

    final_df = final_df.sort_values(
    by=["engagement_score", "complexity_score"],
    ascending=[False, True]
)

    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved final project features to {OUTPUT_FILE}")

    print(
        final_df[
            [
                "project_id",
                "title",
                "engagement_score",
                "number_of_sprites",
                "number_of_blocks",
                "number_of_scripts",
                "scripts_per_sprite",
                "broadcasts",
                "clones",
                "custom_blocks",
                "advanced_feature_count",
                "complexity_score",
            ]
        ]
    )


if __name__ == "__main__":
    main()