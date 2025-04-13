# import json
# from llama_index.core import Document
# from pathlib import Path
# from docx import Document as DocxDocument
# import fitz

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import CodeSplitter
import json
from pathlib import Path

# Load all files from the SakilaProject folder
reader = SimpleDirectoryReader(
    input_dir="../SakilaProject",
    recursive=True,
    required_exts=[".java", '.html'],  # Add more if needed
    exclude_hidden=True
)

# Load as documents
documents = reader.load_data()

# Use LlamaIndex's code-aware splitter
ext_to_splitter = {
    ".java": CodeSplitter(
                language="java",
                chunk_lines=100,
                chunk_lines_overlap=10
            ),
    ".html": CodeSplitter(
                language="html",
                chunk_lines=100,
                chunk_lines_overlap=10
            ),
}
# splitter = CodeSplitter(
#     language="java",
#     chunk_lines=100,
#     chunk_lines_overlap=10
# )
def get_splitter_from_path(path):
    return ext_to_splitter.get(Path(path).suffix.lower(), "auto")

def load_all():
    # nodes = splitter.get_nodes_from_documents(documents)
    split_nodes = []
    for doc in documents:
        splitter = get_splitter_from_path(doc.metadata.get("file_path", ""))
        split_nodes.extend(splitter.get_nodes_from_documents([doc]))
        
    output = []
    for i, node in enumerate(split_nodes):
        pt = node.metadata.get("file_path", "unknown").split('..\\')[1]
        output.append({
            "id": i,
            "source": pt,
            "content": node.text
        })

    with open("llama_chunks.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    print(f"Saved {len(output)} chunks to llama_chunks.json")
    # return output
load_all()

# def load_pdfs(pdf_dir="data/InsurancePDFs"):
#     docs = []
#     for path in Path(pdf_dir).glob("*.pdf"):
#         with fitz.open(path) as pdf:
#             text = "\n".join([page.get_text() for page in pdf])
#             if text.strip():
#                 docs.append(Document(text=text, metadata={"file": str(path)}))
#     return docs

# def load_docs(doc_dir="data/InsurancePDFs"):
#     docs = []
#     for path in Path(doc_dir).glob("*.docx"):
#         doc = DocxDocument(path)
#         text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
#         if text:
#             docs.append(Document(text=text, metadata={"file": str(path)}))
#     return docs

# def load_all():
    # web = load_web_docs()
    # pdfs = load_pdfs()
    # docs = load_docs()
    # print(f"Loaded {len(web)} web docs, {len(pdfs)} PDFs, {len(docs)} Word docs")
    # return web + pdfs + docs
