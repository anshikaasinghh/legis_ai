
with open('dummy.txt','r') as fs:
    input_text=fs.read()

import re
import os

# Split the text into individual cases
cases = re.split(r'\bCase \d+\b', input_text)[1:]

def load_all_cases(cases_files):
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


    cases_list=[]
    # Extract and save each case
    for i, case_text in enumerate(cases, start=1):
        extracted = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, case_text)
            extracted[field] = match.group(1).strip() if match else "Not found"
        cases_list.append(extracted)

    # for i in cases_list:
    #     print(f"Extracted and saved {i}")
    #     print("-"*25)
    return cases_list
# c=load_all_cases('dummy.txt')
# print(len(c), '\n---------', c[-1], '\n---------', c[24], '\n---------', c[21], '\n---------', c[23])