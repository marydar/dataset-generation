import json
from pathlib import Path

MASTER_DATASET = "dataset.json"
RAW_FOLDER = Path("raw")
MODEL = "deepseek-v4"
SOURCE = "generated"

VALID_LABELS = [
    "Desktop & Mobile & Web Development",
    "Cybersecurity",
    "AI / Machine Learning / Data Science",
    "Infrastructure (DevOps, Cloud, Databases, Networking)",
    "Clinical Diagnosis, Treatment & Surgery",
    "Medication & Pharmacology",
    "Mental Health (Clinical)",
    "Healthcare Organizations, System, Hospitals",
    "Nutrition",
    "Payments & Personal Budgeting",
    "Banking",
    "Investment, Markets & Cryptocurrency",
    "Corporate Accounting",
    "Physics & Mathematics",
    "Chemistry",
    "Biology",
    "Team Sports",
    "Individual Sports",
    "Fitness & Training",
    "Civil, Structural & Architecture",
    "Mechanical & Electrical Engineering",
    "Family & Relationships",
    "Personal Growth & Reflection",
    "Travel",
    "Marketing & Sales",
    "Entrepreneurship & Startups",
    "Management & Strategy & Human Resources",
    "Criminal & Civil Law",
    "Labor, Family & Contract Law",
    "Corporate, Regulatory & International Law",
    "General Law (misc.)",
    "Game",
    "Film",
    "Music",
    "Literature",
    "Painting",
]
# Parent-to-Child Mapping Hierarchy
HIERARCHY = {
    "Technology & Programming": [
        "Desktop & Mobile & Web Development",
        "Cybersecurity",
        "AI / Machine Learning / Data Science",
        "Infrastructure (DevOps, Cloud, Databases, Networking)"
    ],
    "Medical": [
        "Clinical Diagnosis, Treatment & Surgery",
        "Medication & Pharmacology",
        "Mental Health (Clinical)",
        "Healthcare Organizations, System, Hospitals",
        "Nutrition"
    ],
    "Finance": [
        "Payments & Personal Budgeting",
        "Banking",
        "Investment, Markets & Cryptocurrency",
        "Corporate Accounting"
    ],
    "Science": [
        "Physics & Mathematics",
        "Chemistry",
        "Biology"
    ],
    "Sports": [
        "Team Sports",
        "Individual Sports",
        "Fitness & Training"
    ],
    "Engineering": [
        "Civil, Structural & Architecture",
        "Mechanical & Electrical Engineering",
    ],
    "Personal": [
        "Family & Relationships",
        "Personal Growth & Reflection",
        "Travel"
    ],
    "Business": [
        "Marketing & Sales",
        "Entrepreneurship & Startups",
        "Management & Strategy & Human Resources"
    ],
     "Law": [
        "Criminal & Civil Law",
        "Labor, Family & Contract Law",
        "Corporate, Regulatory & International Law",
        "General Law (misc.)"
    ],
     "Art": [
        "Game",
        "Film",
        "Music",
        "Literature",
        "Painting"
    ],


}

VALID_LABELS = set(VALID_LABELS)
# Invert mapping to find a parent from any child label
CHILD_TO_PARENT = {
    child: parent
    for parent, children in HIERARCHY.items()
    for child in children
}

def validate_item(item):
    """
    Returns cleaned item or None if invalid.
    """

    if not isinstance(item, dict):
        return None

    text = item.get("text")
    label = item.get("label")

    if not isinstance(text, str):
        return None

    if not isinstance(label, str):
        return None

    text = text.strip()
    label = label.strip()

    if not text or not label:
        return None

    if label not in VALID_LABELS:
        print(f"Invalid label: {label}")
        return None

    item["text"] = text
    item["label"] = label

    return item

def enrich_item(item):
    """
    Add new columns if they don't already exist.
    """

    if "parent_label" not in item:
        item["parent_label"] = CHILD_TO_PARENT[item["label"]]

    if "generator_model" not in item:
        item["generator_model"] = MODEL

    if "source" not in item:
        item["source"] = SOURCE

    return item

def normalize_text(text: str) -> str:
    return text.strip().lower()


def load_json(path: Path):

    if not path.exists():
        return []

    if path.stat().st_size == 0:
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"{path} is not a JSON list.")
            return []

        return data

    except json.JSONDecodeError:
        print(f"{path} contains invalid JSON.")
        return []

def save_json(data, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_all_batches():

    master_path = Path(MASTER_DATASET)

    dataset = load_json(master_path)
    dataset = [enrich_item(item) for item in dataset]
    
    
    existing = {
        normalize_text(item["text"])
        for item in dataset
        if "text" in item
    }

    added = 0

    json_files = sorted(RAW_FOLDER.glob("*.json"))

    if not json_files:
        print("No batch files found.")
        

    for batch_file in json_files:

        print(f"Merging {batch_file.name}")

        batch = load_json(batch_file)

        for item in batch:

            item = validate_item(item)

            if item is None:
                continue

            item = enrich_item(item)

            key = normalize_text(item["text"])

            if key in existing:
                continue

            dataset.append(item)
            existing.add(key)
            added += 1

        # Delete the batch after it has been merged
        batch_file.unlink()

    save_json(dataset, master_path)

    print(f"\nAdded {added} new examples.")
    print(f"Dataset now contains {len(dataset)} examples.")
    print("Processed batch files have been deleted.")


if __name__ == "__main__":
    merge_all_batches()