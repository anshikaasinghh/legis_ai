from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv
import os

#load all env variables
genai.configure(api_key='''AIzaSyAUD7wyBizj2rH_UO5N8MuMIgz7-9_1tfk''')
# 1. Load your vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("vector_db", embedding_model, allow_dangerous_deserialization=True)

# 2. User asks a legal question
query = "What are the environmental risks in the mining lease case?"

# 3. Retrieve top 3 relevant chunks
docs = db.similarity_search(query, k=3)

# 4. Construct context
context = "\n\n".join([doc.page_content for doc in docs])

# 5. Prepare Gemini LLM
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-flash"

# 6. Prompt LLM
prompt = f"""You are a legal assistant. Based on the context from legal case documents, answer the following query neutrally and clearly.

### Context:
{context}

### Question:
{query}

### Answer:
"""

response = model.generate_content(prompt)

# 7. Print the result
print("\n🧠 Gemini's Answer:\n")
print(response.text)
