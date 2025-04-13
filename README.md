# 📚 LLM-Powered Code Summarization Pipeline

This project is a lightweight, modular architecture for automating the summarization of source code using Large Language Models (LLMs). It reads project files, intelligently splits them into manageable chunks, and uses an LLM (via OpenRouter) to generate structured summaries, helping developers quickly understand the purpose, structure, and functionality of any codebase.

---

## 🔧 Tech Stack

- **LlamaIndex**: Framework for RAG pipeline
- **OpenRouter**: Free access to powerful LLMs (e.g., OpenAI GPT)
- **Python**: Core scripting and backend logic

---

## 🏗️ Architecture Overview
```
+-------------------+
|   Source Code     |
+--------+----------+
         |
         v
+--------+----------+
|  Code Reader/Splitter |
| (e.g., file traversal, |
|  chunking logic)      |
+--------+----------+
         |
         v
+--------+----------+
| Prompt Template   |
| Generator         |
| (for summarization)|
+--------+----------+
         |
         v
+--------+----------+
| LLM Inference     |
| (OpenRouter via   |
| LlamaIndex/OpenAI |
| like interface)   |
+--------+----------+
         |
         v
+--------+----------+
| Summarized Output |
| (JSON/Markdown)   |
+-------------------+
```

## 🔧 Components
1. Code Reader & Splitter
    Recursively traverses a given project directory.

    Identifies .java, .py, or relevant files.

    Splits large files into manageable chunks for token-friendly processing.

2. Prompt Templates
    Custom prompt template that asks the LLM to extract:

    Project or file purpose

    Key classes/functions and their descriptions

    Design patterns or unique implementations

    Any notable complexity

3. LLM API (OpenRouter)
    Accesses models like llama-3-70b-instruct via OpenRouter.

    Utilizes LlamaIndex's OpenRouter class to standardize interaction.

4. Output Formatter
    Cleans and parses JSON responses.

    Saves structured summaries to .json or .md.

    Extracts high-level project summaries from all components.

    Output gets saved in the output folder in 2 json files.
        final_knowledge.json (breakdown of each code file, Key methods, method signatures, and descriptions)
        overview_knoledge.json (A high-level overview of the project's purpose and functionality)


## 🚀 Getting Started
```
git clone <repo>
cd <project>
pip install -r requirements.txt
python main.py --dir path/to/codebase
```