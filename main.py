from pathlib import Path

from download_dataset import download_dataset
from merge_datasets import merge_all_batches
from create_hf_dataset import create_dataset


RAW_FOLDER = Path("raw")
HF_DATASET = "maryamdar/topic-classification-dataset-v2"


def main():
    # Check if there are any batch files to process
    json_files = list(RAW_FOLDER.glob("*.json"))

    if not json_files:
        print("No batch files found in 'raw/'. Nothing to do.")
        return

    print("Downloading latest dataset from Hugging Face...")
    download_dataset(HF_DATASET)

    print("Merging new batches...")
    merge_all_batches()

    print("Uploading updated dataset to Hugging Face...")
    create_dataset(HF_DATASET)

    print("\n✅ Dataset updated successfully!")


if __name__ == "__main__":
    main()