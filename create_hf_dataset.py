from datasets import Dataset
import json


def create_dataset(
    json_path="dataset.json",
    output_path="hf_dataset"
):

    # Load JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert to Hugging Face Dataset
    dataset = Dataset.from_list(data)

    # Save locally
    dataset.save_to_disk(output_path)
    print(dataset)
    print(f"Saved to {output_path}")
    dataset.push_to_hub(
    "maryamdar/topic-classification-dataset"
    )



if __name__ == "__main__":
    create_dataset()
   