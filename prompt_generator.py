def generate_generation_prompt(
    labels: dict,
    samples_per_label: int,
    batch_size: int
) -> str:
    label_info = []
    for name, desc in labels.items():
        label_info.append(f"- **{name}**: {desc} ({samples_per_label} examples)")

    labels_text = "\n".join(label_info)

    prompt = f"""You are generating a high quality text classification dataset.

**Task**: Generate realistic user-written texts belonging to the provided labels.


generate texts for all the labels
at the end save the output as a json file

**Labels and descriptions**:
{labels_text}

example:
Label:
AI / Machine Learning / Data Science

Description:
Building and training machine learning models, artificial intelligence, NLP, computer vision, large language models, data analysis, data pipelines, model deployment, and MLOps.

Requirements:
- Every example must belong clearly to this category.
- Do not generate examples from other categories.
- Use realistic user questions.
- Include different difficulty levels.
- Avoid repeating similar wording.

**Diversity requirements**: Examples should vary in:
- wording
- sentence structure
- difficulty
- user intent
- vocabulary

**Quality requirements**: Avoid:
- duplicates
- meaningless sentences
- overly short examples
- examples mentioning the label name directly
- artificial generated wording

Important:
Use the provided label descriptions as the source of truth.
The description defines the boundaries of each category.
Do not create examples that fit another label.

**Output format**: Return ONLY valid JSON. No markdown, no ```json blocks, no explanation before or after JSON.
Return only the JSON content, which will be saved directly as a .json file. Do not add explanations.
Required format:
[
  {{
    "text": "example user text",
    "label": "Label Name"
  }}
]

Save the output as a JSON file

**Additional rules**:
- Create balanced data across all labels
- Use exactly the provided labels - no variations, no extra labels
- Generate exactly the number of examples specified per label"""
    return prompt