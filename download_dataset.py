import json
from datasets import load_dataset

DATASET_ID = "maryamdar/topic-classification-dataset"


def download_dataset():

    dataset = load_dataset(DATASET_ID)

    data = list(dataset["train"])
    df = dataset["train"].to_pandas()

    print(df.head())
    print()
    print(df.columns)
    print()
    print(df.info())

    with open("dataset.json", "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Downloaded {len(data)} examples.")
    print("Saved as dataset.json")


if __name__ == "__main__":
    download_dataset()