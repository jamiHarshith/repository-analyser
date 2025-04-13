import settings
import json
import pickle
from tqdm import tqdm
from collections import defaultdict
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.prompts import PromptTemplate
from llama_index.core.utils import get_tokenizer

tokenizer = get_tokenizer()
MAX_TOKENS = 8192
RESERVED_FOR_RESPONSE = 1000  # leave space for LLM response
MAX_PROMPT_TOKENS = MAX_TOKENS - RESERVED_FOR_RESPONSE

llm = settings.llm
nodes_by_file = defaultdict(list)
all_nodes = []
with open('llama_chunks.json', 'r') as f:
    all_nodes = json.load(f)
for node in all_nodes:
    file_path = node.get("source", "unknown")
    nodes_by_file[file_path].append(node)
print(len(nodes_by_file))

def batch_nodes_by_tokens(nodes, max_tokens=100000):
    batches = []
    current_batch = []
    current_tokens = 0
    for node in nodes:
        node_tokens = len(tokenizer(node.get('content','')))
        if current_tokens + node_tokens > max_tokens:
            batches.append(current_batch)
            current_batch = [node]
            current_tokens = node_tokens
        else:
            current_batch.append(node)
            current_tokens += node_tokens

    if current_batch:
        batches.append(current_batch)
    return batches

custom_prompt_template_str = """
    You are a code analysis assistant. Given a code snippet, extract the following in JSON format:

    - purpose: A short description of what this code does.
    - key_methods: A list of method/function names with their signatures and what they do. This can be json too
    - complexity_notes: Any noteworthy complexity, design patterns, or unusual implementations.

    Respond ONLY in JSON format. json.load should be able to parse it into json

    Code:
    {context_str}
    """

custom_prompt = PromptTemplate(custom_prompt_template_str)

def extract():
    extracted_knowledge = []
    for file_path, nodes in tqdm(nodes_by_file.items(), desc="Processing files"):
        batches = batch_nodes_by_tokens(nodes)
        # print(batches[0])
        for i, batch in enumerate(batches):
            combined_code = "\n\n".join(node.get('content','') for node in batch)
            prompt = custom_prompt.format(context_str=combined_code)
            # print(prompt)
            response = llm.complete(prompt)
            json_data = {}
            try:
                response = llm.complete(prompt)
                # json_data['response'] = response.text.strip()
                json_data = json.loads(response.text.strip()[8:-3].replace('\"', '"'))
            except Exception as e:
                json_data = {
                    "purpose": "",
                    "key_methods": [],
                    "complexity_notes": "",
                    "error": str(e)
                }

            json_data["file_path"] = file_path
            json_data["batch_id"] = i
            extracted_knowledge.append(json_data)
    with open("./output/final_knowledge.json", "w") as f:
        json.dump(extracted_knowledge, f, indent=2)
# extract()

overal_overview_template = '''
You are analyzing a software project based on metadata from its components. Each component includes a purpose and other structural details. 

Your task is to provide a **high-level overview** of the project's overall **purpose and functionality**, as if explaining it to a new developer or stakeholder.

Here is the data:

{project_metadata}

---

Summarize the project covering:
- What the project is (its domain or type)
- What it does (main functionality)
- Who it serves or how it's used
- Any unique architectural or design aspects (if mentioned)

Ensure the extracted knowledge is structured in a well-organized, readable, and easily consumable JSON format.'''

overal_overview_prompt = PromptTemplate(overal_overview_template)

def get_overal_overview():
    extract()
    
    with open("./output/final_knowledge.json", "rb") as f:
        loaded_data = json.load(f)
        
    purposes = [item["purpose"] for item in loaded_data]
    full_context = " ".join(purposes)
    prompt = custom_prompt.format(context_str=full_context)
    response = llm.complete(prompt)
    json_data = json.loads(response.text.strip()[8:-3].replace('\"', '"'))
    
    with open('./output/overview_knoledge.json', "w") as f:
        json.dump(json_data, f, indent=2)
        
get_overal_overview()
    