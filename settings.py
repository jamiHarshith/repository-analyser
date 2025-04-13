from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openrouter import OpenRouter

openrouter_api_key = 'add your key'

llm = OpenRouter(
    # model="open-r1/olympiccoder-7b:free",
    # model="qwen/qwen-2.5-coder-32b-instruct:free",
    model="meta-llama/llama-3.3-70b-instruct:free",
    api_key=openrouter_api_key,
    max_tokens=1024
)

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

Settings.llm = llm
Settings.embed_model = embed_model
# splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
# Settings.transformations = [splitter]
# Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
# Settings.num_output = 512
# Settings.context_window = 3900

print(Settings.embed_model)

# llm.complete("is the endpoint working?")
# from llama_index.core.llms import ChatMessage
# response = llm.chat([ChatMessage(role= "user", content='is the endpoint working?')])
# print(response)