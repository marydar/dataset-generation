from datasets import Dataset
import json


def create_dataset(
    DATASET_ID,
    json_path="dataset.json",
    output_path="hf_dataset"
):

    # Load JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    required_columns = {
        "text",
        "parent_label",
        "label",
        "generator_model",
        "source",
    }

    missing = required_columns - set(data[0].keys())

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    # Convert to Hugging Face Dataset
    dataset = Dataset.from_list(data)

    # Save locally
    dataset.save_to_disk(output_path)
    print(dataset)
    print(f"Saved to {output_path}")
    dataset.push_to_hub(
    DATASET_ID
    )



if __name__ == "__main__":
    create_dataset()
   