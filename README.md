# Kannada Word Builder & Validator

## Problem Statement - 2: Kannada Word Builder & Validator

## Team Name: UK Boys
### Team members: 
1. Prem Kamble - 1MS23CS139
2. Dnyaneshwar Bhajantri - 1MS23CS063

## Project Description
A toolkit to build, join and validate Kannada words using grammatical rules (Sandhi), case-marker (vibhakti) handling, dictionary validation and fuzzy matching to suggest corrections. This repository contains the core generator script, supporting dictionaries, and example test cases.

---

## Table of contents

- [Features](#features)
- [How to run](#how-to-run)
- [Installation](#installation)
- [Usage](#usage)
- [Result Summary](#result-summary)
- [Dictionaries and data format](#dictionaries-and-data-format)
- [Testing](#testing)
- [Dependencies & environment](#dependencies--environment)

---

## Features

- Dictionary validation: checks if candidate words exist in the repository dictionaries
- Sandhi (joining) application: applies Kannada Sandhi rules to combine words
- Case marker (vibhakti) addition: attaches appropriate vibhakti endings where required
- Fuzzy matching: suggests likely corrections for typos using approximate string matching
- Smart hints & suggestions: proposes common/likely word combinations
- Compound validation: validates whether formed compounds are plausible given dictionary and rule checks

---

## How to run

1. Clone the repository:
   - git clone https://github.com/Dnyaneshwar-dnyanu/Kannada-word-builder--UK-Boys.git
2. Create and activate a Python virtual environment (recommended):
   - python -m venv venv
   - On Linux/macOS: source venv/bin/activate
   - On Windows: venv\Scripts\activate
3. Install dependencies (see [Dependencies & environment](#dependencies--environment)).
4. Inspect and run the main script:
   - python generate_words.py

(See the Usage section for examples and more details.)

---

## Installation

Minimal install (example):

```bash
# recommended: create and activate a virtual environment first
pip install pandas fuzzywuzzy python-levenshtein
```

If you prefer a requirements file, create one from the above packages and install via:

```bash
pip install -r requirements.txt
```

Recommended Python version: 3.8+

---

## Usage

The repository's primary script is `generate_words.py`. This script is the entry point for generating/joining Kannada word forms and validating them against the available dictionaries and rules.

Common usage patterns (examples):

- Basic run:
  - python generate_words.py
- To experiment with the dictionaries and rules, open `generate_words.py` and look for the sections where dictionaries are loaded and rules applied.

Note: The exact command-line options (if any) are defined in `generate_words.py`. If you need more detailed CLI flags, open the file to view help or argument parsing code.

Example conceptual workflow:

1. Provide two base Kannada words (or a base + suffix).
2. The tool attempts to join them applying Sandhi rules.
3. Produced candidates are checked against dictionaries.
4. Fuzzy matching runs to offer suggestions for misspelled inputs.
5. Results are returned with metadata (which rule applied, whether dictionary-validated, suggestions).

---

## Result Summary

At a high level, the code:

- Loads one or more dictionaries of Kannada words (from the `dictionaries/` directory).
- Implements Sandhi rules to join words correctly according to Kannada grammatical conventions.
- Adds vibhakti (case endings) where relevant to form grammatically valid inflections.
- Uses fuzzy string matching to propose corrections for unrecognized words or typos.
- Validates generated compound/inflected forms against the dictionary to filter implausible outputs.
- Optionally provides "smart hints" — frequently seen combinations or likely corrections.

The script is rule-driven (explicit rules for joining) with dictionary lookups and approximate matching layered on top.

---

## Dictionaries and data format

All word data used for validation and suggestions is stored under the `dictionaries/` directory.

- Typical formats that may appear:
  - Plain text files (one word per line)
  - CSV / TSV files with additional metadata columns (POS, lemma, etc.)
- To add words:
  - Add them to the appropriate dictionary file in `dictionaries/` following the existing file format.
  - If adding a new file, choose a consistent format and update `generate_words.py` to load it (search for the dictionary-loading logic).
- Quality of dictionary data directly affects validation and suggestion accuracy — prefer curated, normalized word lists.

Note: Open the files in `dictionaries/` to see the exact format used in this repo before editing.

---

## Sandhi rules, Vibhakti and validation (how it works)

- Sandhi rules:
  - Implement morphological joining rules for Kannada (example: vowel-contraction, consonant gemination, etc.).
  - Each rule typically inspects the boundary characters of two words and transforms the joining region accordingly.
- Vibhakti (case marker) handling:
  - Vibhakti endings are added/validated to produce correct case-marked forms for nouns/pronouns.
- Compound validation:
  - After generating candidate forms, the system checks dictionary presence and/or applies heuristics to determine plausibility.
- Fuzzy matching:
  - When a word isn't found in dictionaries, fuzzy matching suggests nearest candidates (via libraries such as fuzzywuzzy).
  - This helps with typos and OCR/text-input errors.

---

## Testing

- Example test cases are in `test_cases/`. They demonstrate inputs and expected outputs or usage examples.
- To run tests:
  - Inspect files in `test_cases/` for the provided instructions or sample scripts.
  - If tests are Python unit tests, you can commonly run:
    - python -m unittest discover test_cases
  - If custom test runners or scripts exist, follow the instructions at the top of those files.

---

## Dependencies & environment

Primary Python packages used by this project (installable via pip):

- pandas
- fuzzywuzzy
- python-levenshtein

Install with:

```bash
pip install pandas fuzzywuzzy python-levenshtein
```

Optional: create a virtual environment to isolate dependencies.

---

## Examples

Below are conceptual examples to illustrate expected behavior. Exact output and invocation depend on the implementation details in `generate_words.py`.

- Joining two words:
  - Input: ಪುಸ್ತಕ + ಆಲಯ
  - Action: Apply Sandhi rules to join them
  - Output: ಪುಸ್ತಕಾಲಯ
