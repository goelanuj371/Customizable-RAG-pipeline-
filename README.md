# customrag

**customrag** is a customizable **Retrieval-Augmented Generation (RAG)** pipeline implemented as a Python library. It allows developers to quickly integrate RAG into their applications using a simple configuration system. With support for multiple LLM and embedding providers, `customrag` offers an easy way to experiment with various APIs and document formats.

---

## Features

* Easy `pip` installation: `pip install customrag`
* YAML-based configuration for flexibility
* Works with `.txt`, `.pdf`, `.csv`, `.json`, `.docx`, and `.md` files
* Embedding storage and retrieval using FAISS
* Supports Gemini SDK (Cloud Console) and LangChain-native providers
* CLI tool for quick config generation

---

## Installation

```bash
pip install customrag
```

---

## Quick Setup

Generate a default `config.yaml` in your project directory:

```bash
customrag-setup
```

Edit the file to include your API keys and desired models.

---

## Sample config.yaml

```yaml
embedding:
  provider: gemini
  model: models/embedding-001

llm:
  provider: gemini
  model: gemini-1.5-pro

api_keys:
  gemini: your_gemini_api_key_here
  gemini_studio: your_gemini_studio_api_key_here
  openai: your_openai_api_key_here
  huggingface: your_huggingface_token_here
  xai: your_xai_api_key_here
```

---

## How to Use

### Step 1: Initialize the RAG pipeline

```python
from customrag import RAGPipeline

pipeline = RAGPipeline(config_path="config.yaml")
```

### Step 2: Build a Vectorstore

```python
pipeline.build_vectorstore("path_to_your_file.pdf")
```

This loads and chunks the document, embeds it, and stores it using FAISS.

### Step 3: Ask Questions

```python
answer = pipeline.query("What is this document about?")
print(answer)
```

The pipeline uses the configured LLM (via SDK or LangChain) to generate answers from the context.

---

## Supported Providers

| Provider                      | Embeddings | LLM Chat | SDK Support |
| ----------------------------- | ---------- | -------- | ----------- |
| OpenAI                        | Yes        | Yes      | No          |
| Gemini (Cloud Console)        | Yes        | No       | Yes         |
| Gemini Studio                 | Yes        | Yes      | No          |
| HuggingFace Inference API     | Yes        | Yes      | No          |
| xAI                           | Yes        | Yes      | No          |
| sentence-transformers (local) | Yes        | No       | No          |

---

## CLI Support

```bash
customrag-setup
```

This creates a starter config that can be modified per your needs.

---

## License

MIT License

Copyright (c) [2024] [Anuj Goel]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author

Developed by Anuj Goel. Contributions and feedback are welcome.
