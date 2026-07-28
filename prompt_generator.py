def generate_generation_prompt(
    labels: dict,
    samples_per_label: int,
    batch_size: int
) -> str:

    label_info = []

    for name, desc in labels.items():
        label_info.append(
            f"""Label:
{name}

Description:
{desc}

Number of examples:
{samples_per_label}
"""
        )

    labels_text = "\n\n".join(label_info)

    prompt = f"""
You are generating a high-quality text classification dataset.

Your task is to create realistic user-written messages and assign them to the correct category.

Generate examples only from the labels and descriptions provided below.

==================================================

LABEL DEFINITIONS:

{labels_text}

==================================================

DATA GENERATION RULES

1. Each example must clearly belong to exactly one label.
2. Use the descriptions as the source of truth for category boundaries.
3. Do not mix topics between categories.
4. Use exactly the provided label names.
5. Do not create new labels.
6. Do not mention the label name inside the generated text.

==================================================

QUALITY REQUIREMENTS

Generated texts should look like real users asking questions or describing problems.

Include variety in:
- wording
- sentence structure
- technical difficulty
- user intent
- vocabulary
- level of expertise

Examples can include:
- beginner questions
- advanced technical questions
- troubleshooting requests
- comparison questions
- practical scenarios

Avoid:
- duplicate examples
- slightly reworded duplicates
- meaningless sentences
- very short texts
- generic statements
- artificial sounding sentences

Generate new examples. Avoid common examples and obvious textbook sentences.
Prefer diverse real-world user queries.

==================================================

OUTPUT FORMAT

Return ONLY valid JSON.

Do not include:
- explanations
- markdown
- ```json blocks
- comments

Required format:

[
  {{
    "text": "realistic user message",
    "label": "exact label name"
  }}
]

==================================================

FINAL CHECK

Verify that:

- every example has both "text" and "label"
- every label exactly matches one of the provided labels
- no duplicate texts exist
- examples are distributed across all requested labels
- the JSON is valid

==================================================

OUTPUT FILE REQUIREMENTS

Create exactly ONE file.

Save it inside:

raw/

Filename:

batch_YYYY_MM_DD_HHMMSS.json

Example:

raw/batch_2026_07_28_153045.json

If the folder does not exist, create it.

Do NOT modify:

- dataset.json
- labels.json
- prompt_generator.py
- any Python source file

Do NOT overwrite previous batch files.

This file must contain ONLY the newly generated examples.

==================================================

EXAMPLE FILE CONTENT

[
  {{
    "text": "How do I deploy a Docker container on AWS?",
    "label": "Infrastructure (DevOps, Cloud, Databases, Networking)"
  }},
  {{
    "text": "My React application fails during production build.",
    "label": "Desktop & Mobile & Web Development"
  }}
]

Do not wrap the JSON in markdown.

==================================================

AFTER GENERATION

Do not merge this batch into dataset.json.

The merge will be performed later by a Python script.

Simply create the new batch file and stop.
"""

    return prompt