import csv
import requests
import time


SEARCH_TERMS = ["game", "animation", "story", "music", "tutorial"]
PROJECTS_PER_TERM = 20

OUTPUT_FILE = "data/project_sample.csv"


def search_projects(query, limit=20, offset=0):
    url = "https://api.scratch.mit.edu/search/projects"

    params = {
        "q": query,
        "mode": "popular",
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    return response.json()


def collect_sample():
    collected_projects = []
    seen_ids = set()

    for term in SEARCH_TERMS:
        print(f"Searching projects for theme: {term}")

        term_count = 0
        offset = 0

        while term_count < PROJECTS_PER_TERM:
            try:
                projects = search_projects(term, limit=20, offset=offset)
            except requests.RequestException as error:
                print(f"Could not collect projects for {term}: {error}")
                break

            if not projects:
                break

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
                    "source": "scratch_search_popular",
                })

                seen_ids.add(project_id)
                term_count += 1

                if term_count >= PROJECTS_PER_TERM:
                    break

            offset += 20
            time.sleep(0.5)

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