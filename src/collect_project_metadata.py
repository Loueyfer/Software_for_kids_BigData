import pandas as pd
import requests
import time


INPUT_FILE = "data/project_sample.csv"
OUTPUT_FILE = "data/project_metadata.csv"


def get_project_metadata(project_id):
    url = f"https://api.scratch.mit.edu/projects/{project_id}"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return response.json()


def extract_metadata(project):
    stats = project.get("stats", {})
    remix = project.get("remix", {})
    author = project.get("author", {})

    return {
        "project_id": project.get("id"),
        "title": project.get("title", ""),
        "author": author.get("username", ""),
        "views": stats.get("views", 0),
        "loves": stats.get("loves", 0),
        "favorites": stats.get("favorites", 0),
        "comments": stats.get("comments", 0),
        "remix_count": remix.get("count", 0),
    }

def main():
    sample = pd.read_csv(INPUT_FILE)

    collected_metadata = []

    for _, row in sample.iterrows():
        project_id = row["project_id"]
        print(f"Collecting metadata for project {project_id}")

        try:
            project = get_project_metadata(project_id)
            metadata = extract_metadata(project)

            # Keep our original sample information too
            metadata["theme"] = row.get("theme", "")
            metadata["source"] = row.get("source", "")

            collected_metadata.append(metadata)

        except requests.RequestException as error:
            print(f"Could not collect metadata for project {project_id}: {error}")

        # Small pause so we do not send requests too aggressively
        time.sleep(0.5)

    metadata_df = pd.DataFrame(collected_metadata)
    metadata_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved metadata for {len(metadata_df)} projects to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()