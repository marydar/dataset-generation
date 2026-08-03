from datasets import load_dataset

DATASET_ID = "maryamdar/topic-classification-dataset"

REVISION = "c7ff25f"  # The commit you want to restore

# Load the old revision
dataset = load_dataset(
    DATASET_ID,
    revision=REVISION,
)


# Push it back to the HEAD of the repository
dataset.push_to_hub(DATASET_ID)

print("Dataset restored successfully.")