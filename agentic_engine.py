# agentic_engine.py

import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

#load all env variables
genai.configure(api_key='''AIzaSyAUD7wyBizj2rH_UO5N8MuMIgz7-9_1tfk''')
model = genai.GenerativeModel("gemini-1.5-flash")


# Load Vector Store once
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("./vector_db/", embedding_model, allow_dangerous_deserialization=True)

def run_agent(task_name, instructions, context):
    prompt = f"""
You are a legal analysis assistant. Your task is:

### Task:
{instructions}

### Legal Context:
{context}

### Response:
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def analyze_case_with_agents(query):
    docs = db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    output = {
        "query": query,
        "summary": run_agent("Summary Generator", "Write a concise, neutral summary.", context),
        "legal_issues": run_agent("Issue Extractor", "Extract key legal issues in bullet points.", context).split("\n"),
        "parties": run_agent("Parties Extractor", "Identify petitioner(s) and respondent(s).", context),
        "risks": run_agent("Risk Evaluator", "List legal, financial or environmental risks.", context).split("\n"),
        "related_precedents": run_agent("Precedent Linker", "Mention any similar legal cases or precedents.", context)
    }

    return output


from fpdf import FPDF
from datetime import datetime

def create_pdf_report(agent_output: dict, file_name="case_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def sanitize(text):
        return text.encode('latin1', 'ignore').decode('latin1')

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, sanitize("LEGAL CASE REPORT"), ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, sanitize(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.ln(5)

    def write_section(title, content):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, sanitize(f"\n{title}"), ln=True)
        pdf.set_font("Arial", "", 12)

        if isinstance(content, list):
            for line in content:
                pdf.multi_cell(0, 8, sanitize(f"• {line}"))
        else:
            pdf.multi_cell(0, 8, sanitize(str(content)))
        pdf.ln(3)

    write_section("Query", agent_output.get("query", ""))
    write_section("Summary", agent_output.get("summary", ""))
    write_section("Legal Issues", agent_output.get("legal_issues", []))
    write_section("Parties", agent_output.get("parties", ""))
    write_section("Risks", agent_output.get("risks", []))
    write_section("Related Precedents", agent_output.get("related_precedents", ""))

    pdf.output(file_name)
    return file_name
