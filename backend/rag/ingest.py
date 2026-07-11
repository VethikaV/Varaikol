import os
import chromadb

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from rag.embeddings import get_embedding

client = chromadb.PersistentClient(path="vectordb")

collection = client.get_or_create_collection(
    name="drawing_knowledge"
)

knowledge_path = "knowledge_base"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

doc_id = 0

for pdf in os.listdir(knowledge_path):

    if not pdf.endswith(".pdf"):
        continue

    loader = PyPDFLoader(os.path.join(knowledge_path, pdf))

    pages = loader.load()

    chunks = splitter.split_documents(pages)

    for chunk in chunks:

        text = chunk.page_content

        embedding = get_embedding(text)

        collection.add(
            ids=[str(doc_id)],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": pdf}]
        )

        doc_id += 1

print("Knowledge base indexed successfully.")