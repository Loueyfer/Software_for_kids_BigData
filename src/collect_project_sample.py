import csv
import requests


SEARCH_TERMS = ["game", "animation", "story", "music", "art"]
PROJECT_LIMIT = 10

OUTPUT_FILE = "data/project_sample.csv"


def search_projects(query, limit=10):
    url = "https://api.scratch.mit.edu/search/projects"

    params = {
        "q": query,
        "mode": "popular",
        "limit": limit,
        "offset": 0
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    return response.json()


def collect_sample():
    collected_projects = []
    seen_ids = set()

    for term in SEARCH_TERMS:
        print(f"Searching projects for theme: {term}")

        try:
            projects = search_projects(term, limit=10)
        except requests.RequestException as error:
            print(f"Could not collect projects for {term}: {error}")
            continue

        for project in projects:
            project_id = project.get("id")

            if project_id is None:
                continue

            if project_id in seen_ids:
                continue

            collected_projects.append({
                "project_id": project_id,
                "title": project.get("title", ""),
                "theme": term,
                "source": "scratch_search_popular"
            })

            seen_ids.add(project_id)

            if len(collected_projects) >= PROJECT_LIMIT:
                return collected_projects

    return collected_projects


def save_sample(projects):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["project_id", "title", "theme", "source"]
        )

        writer.writeheader()
        writer.writerows(projects)


def main():
    projects = collect_sample()
    save_sample(projects)

    print(f"Saved {len(projects)} projects to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()