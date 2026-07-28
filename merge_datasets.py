import json
from pathlib import Path

MASTER_DATASET = "dataset.json"
RAW_FOLDER = Path("raw")


def normalize_text(text: str) -> str:
    return text.strip().lower()


def load_json(path: Path):
    if not path.exists():
        return []

    if path.stat().st_size == 0:
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {path} is not valid JSON. Skipping.")
        return []


def save_json(data, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_all_batches():

    master_path = Path(MASTER_DATASET)

    dataset = load_json(master_path)

    existing = {
        normalize_text(item["text"])
        for item in dataset
        if "text" in item
    }

    added = 0

    json_files = sorted(RAW_FOLDER.glob("*.json"))

    if not json_files:
        print("No batch files found.")
        return

    for batch_file in json_files:

        print(f"Merging {batch_file.name}")

        batch = load_json(batch_file)

        for item in batch:

            if not isinstance(item, dict):
                continue

            text = item.get("text", "").strip()

            if not text:
                continue

            key = normalize_text(text)

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