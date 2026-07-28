from datasets import load_dataset


DATASET_ID = "maryamdar/topic-classification-dataset"
dataset = load_dataset(DATASET_ID)

dataset.save_to_disk(
    "data/my_dataset"
)


print(dataset)

print("\nFirst example:")
print(dataset["train"][0])