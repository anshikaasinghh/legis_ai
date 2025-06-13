
from langchain.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai


#load all env variables
genai.configure(api_key='''AIzaSyAUD7wyBizj2rH_UO5N8MuMIgz7-9_1tfk''')
model = genai.GenerativeModel("gemini-1.5-flash")



def run_agent(task_name, instructions, context, model):
    prompt = f"""
    You are a legal analysis assistant. Your task is to perform the following:

    ### Task:
    {instructions}

    ### Legal Context:
    {context}

    ### Response:
    """
    response = model.generate_content(prompt)
    print(f"\n🔍 Agent: {task_name}")
    print("response.text in run_agent: ", response.text)
    return response.text


# Reuse existing Gemini-Pro model
from langchain.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("./vector_db/", embedding_model, allow_dangerous_deserialization=True)

query = "Summarize the environmental mining case and extract its legal and social implications."
docs = db.similarity_search(query, k=3)
context = "\n\n".join([doc.page_content for doc in docs])
print(context)

print(f" docs ----------------\n{docs}")
print('-'*30)
for doc in docs:
    print(doc)
    print('-'*30)


# Agent 1: Legal Issue Extractor
issues = run_agent("Issue Extractor", "Extract the key legal issues being debated in this case in bullet points.", context, model)

# Agent 2: Party Extractor
parties = run_agent("Parties Extractor", "Identify the petitioner(s) and respondent(s) from the case context.", context, model)

# Agent 3: Risk Evaluator
risks = run_agent("Risk Evaluator", "List out any legal, environmental, financial or social risks associated with the case.", context, model)

# Agent 4: Precedent Linker
precedents = run_agent("Precedent Linker", "If available, name any similar cases or legal precedents mentioned or implied.", context, model)

# Agent 5: Summary Generator
summary = run_agent("Summary Generator", "Write a concise, neutral summary of the case in 4–6 sentences.", context, model)

import json

agent_response = {
    "query": query,
    "summary": summary.strip(),
    "legal_issues": issues.strip().split("\n"),
    "parties": parties.strip(),
    "risks": risks.strip().split("\n"),
    "related_cases_or_precedents": precedents.strip()
}

with open("case25_agentic_output.json", "w") as f:
    json.dump(agent_response, f, indent=2)


# Optional: Print nicely
print("\n📦 Final Structured Response:")
print(json.dumps(agent_response, indent=2))

