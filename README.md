# Text Dataset Generation Pipeline

A lightweight pipeline for incrementally generating high-quality text classification datasets using OpenCode, validating and merging generated batches, and publishing the dataset to Hugging Face.

---

## Project Structure

```text
.
├── labels.json                 # Labels and their descriptions
├── dataset.json                # Local working copy of the dataset
├── raw/                        # Newly generated batches
│   ├── batch_2026_07_28_153045.json
│   └── ...
├── create_prompt.py            # Generates generation_prompt.md
├── generation_prompt.md        # Prompt to give to OpenCode
├── merge_dataset.py            # Merges new batches into dataset.json
├── download_dataset.py         # Downloads dataset from Hugging Face
├── create_hf_dataset.py        # Uploads dataset.json to Hugging Face
├── main.py                     # Runs the complete update pipeline
└── README.md
```

---

## Workflow

### Step 1 — Configure the labels

Edit `labels.json` and define the labels you want to generate.

Example:

```json
{
    "Desktop & Mobile & Web Development": "Building websites, mobile apps, desktop applications, programming languages, frameworks, debugging, UI/UX, browsers and software development.",
    "Cybersecurity": "Security, authentication, malware, encryption, exploits, vulnerabilities, penetration testing and network security.",
    "AI / Machine Learning / Data Science": "Machine learning, NLP, computer vision, LLMs, data pipelines, model training and MLOps."
}
```

Each label should have a clear description describing the boundaries of that category.

---

### Step 2 — Generate the prompt

Choose how many examples you want **per label** and run:

```bash
python create_prompt.py
```

This creates:

```text
generation_prompt.md
```

---

### Step 3 — Generate a new batch with OpenCode

Open `generation_prompt.md`.

Copy the entire prompt.

Paste it into OpenCode.

OpenCode will generate a new batch and save it inside:

```text
raw/
```

For example:

```text
raw/batch_2026_07_28_153045.json
```

You may generate multiple batch files before continuing.

---

### Step 4 — Merge and upload

Run:

```bash
python main.py
```

This automatically:

1. Downloads the latest dataset from Hugging Face.
2. Converts it into the local `dataset.json`.
3. Merges every JSON batch inside `raw/`.
4. Removes duplicate texts.
5. Updates `dataset.json`.
6. Uploads the updated dataset back to Hugging Face.
7. Removes the processed batch files from `raw/`.

---

## Daily Workflow

```text
Edit labels.json (if needed)
        ↓
Run create_prompt.py
        ↓
Copy generation_prompt.md into OpenCode
        ↓
OpenCode creates batch files inside raw/
        ↓
Run main.py
        ↓
Dataset updated on Hugging Face
```

---

## Output Format

Each generated batch must be a JSON array with the following structure:

```json
[
    {
        "text": "How can I deploy a Docker container on AWS?",
        "label": "Infrastructure (DevOps, Cloud, Databases, Networking)"
    },
    {
        "text": "Why does my React application fail during production build?",
        "label": "Desktop & Mobile & Web Development"
    }
]
```

The final merged dataset has the same format.

---

## Notes

* `dataset.json` is the local working copy of the dataset.
* The Hugging Face dataset is the permanent source of truth.
* Batch files are temporary and are deleted after a successful merge.
* Duplicate texts are removed automatically during the merge process.
* Labels should remain consistent across generations to maintain dataset quality.
