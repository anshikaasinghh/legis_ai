from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from data_ingestion import load_all_cases

# Load your case dicts
cases = load_all_cases("case_files")

# Define chunking strategy
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

documents = []
i=0
for case in cases:
    chunks = text_splitter.split_text(case["Full Legal Case Text"])
    for chunk in chunks:
        doc = Document(
            page_content=chunk,
            metadata={
                "Case Name": case["Case Name"],
                "Citation": case["Citation"],
            }
        )
        documents.append(doc)
        if i==0 or i==8 or i==23:
            print(doc,'\n---------------------')

# Use HuggingFace's free embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vectorstore
vectorstore = FAISS.from_documents(documents, embedding_model)

# Save for reuse
vectorstore.save_local("vector_db/")
