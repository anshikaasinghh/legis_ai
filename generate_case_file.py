
with open('dummy.txt','r') as fs:
    input_text=fs.read()

import re
import os

# Split the text into individual cases
cases = re.split(r'\bCase \d+\b', input_text)[1:]

# Create output directory
output_dir = "extracted_cases"
os.makedirs(output_dir, exist_ok=True)

# Define regex patterns for fields
patterns = {
    "Case Name": r"\* Case Name:\s*(.*)",
    "Citation": r"\* Citation:\s*(.*)",
    "Full Legal Case Text": r"\* Full Legal Case Text \(Narrative\):\s*((?:.|\n)*?)\* Parties:",
    "Parties": r"\* Parties:\s*(.*)",
    "Issues": r"\* Issues:\s*(.*)",
    "Risks": r"\* Risks:\s*(.*)",
    "Summary": r"\* Summary \(Pre-generated\):\s*((?:.|\n)*?)$"
}

print(cases)
# Extract and save each case
for i, case_text in enumerate(cases, start=1):
    extracted = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, case_text)
        extracted[field] = match.group(1).strip() if match else "Not found"

    # Save to a text file
    filename = os.path.join(output_dir, f"case_{i}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for key, value in extracted.items():
            f.write(f"{key}:\n{value}\n\n")

print(f"Extracted and saved {len(cases)} cases to '{output_dir}' directory.")

