from prompt_generator import generate_generation_prompt
import json

SAMPLES_PER_LABEL = 5
def main():

    with open("labels.json", "r", encoding="utf-8") as f:
        labels = json.load(f)


    prompt = generate_generation_prompt(
        labels,
        samples_per_label=SAMPLES_PER_LABEL,
        batch_size=5
    )


    with open(
        "generation_prompt.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(prompt)


    print("Prompt created: generation_prompt.md")


if __name__ == "__main__":
    main()