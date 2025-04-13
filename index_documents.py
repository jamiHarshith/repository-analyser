import settings

from ingest import load_all
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.simple import SimpleVectorStore

all_docs = load_all()

storage_context = StorageContext.from_defaults(
    persist_dir="./storage",
    vector_store=SimpleVectorStore()
)

index = VectorStoreIndex.from_documents(
    all_docs,
    storage_context=storage_context,
)

index.storage_context.persist(persist_dir="./storage")
print("Index built and saved to 'storage'")

# query_engine = index.as_query_engine()
# response = query_engine.query("What services do you offer?")
# print(response)
