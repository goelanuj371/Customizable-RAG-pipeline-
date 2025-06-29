import yaml
import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


class RAGPipeline:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.embedding_model = self._init_embedding_model()
        self.llm_model, self.use_sdk = self._init_llm_model()

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"❌ config.yaml not found at: {config_path}")
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def _init_embedding_model(self):
        provider = self.config["embedding"]["provider"]
        model_name = self.config["embedding"]["model"]
        api_keys = self.config.get("api_keys", {})

        if provider == "sentence-transformers":
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(model_name)

        elif provider == "openai":
            from langchain.embeddings import OpenAIEmbeddings
            key = api_keys.get("openai")
            if not key:
                raise ValueError("❌ Missing OpenAI API key.")
            return OpenAIEmbeddings(model=model_name, openai_api_key=key)

        elif provider == "gemini":
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            key = api_keys.get("gemini")
            if not key:
                raise ValueError("❌ Missing Gemini Cloud Console API key.")
            return GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=key)

        elif provider == "gemini_studio":
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            key = api_keys.get("gemini_studio")
            if not key:
                raise ValueError("❌ Missing Gemini Studio API key.")
            return GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=key)

        elif provider == "huggingface":
            from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
            key = api_keys.get("huggingface")
            if not key:
                raise ValueError("❌ Missing HuggingFace API key.")
            return HuggingFaceInferenceAPIEmbeddings(api_key=key, model_name=model_name)

        elif provider == "xai":
            from langchain_xai import XAIEmbeddings
            key = api_keys.get("xai")
            if not key:
                raise ValueError("❌ Missing xAI API key.")
            return XAIEmbeddings(api_key=key, model=model_name)

        else:
            raise ValueError(f"❌ Unknown embedding provider: {provider}")

    def _init_llm_model(self):
        provider = self.config["llm"]["provider"]
        model_name = self.config["llm"]["model"]
        api_keys = self.config.get("api_keys", {})

        if provider == "openai":
            from langchain.chat_models import ChatOpenAI
            key = api_keys.get("openai")
            if not key:
                raise ValueError("❌ Missing OpenAI API key.")
            return ChatOpenAI(model_name=model_name, openai_api_key=key), False

        elif provider == "gemini_studio":
            from langchain_google_genai import ChatGoogleGenerativeAI
            key = api_keys.get("gemini_studio")
            if not key:
                raise ValueError("❌ Missing Gemini Studio API key.")
            return ChatGoogleGenerativeAI(model=model_name, google_api_key=key), False

        elif provider == "gemini":
            from google import genai
            key = api_keys.get("gemini")
            if not key:
                raise ValueError("❌ Missing Gemini Cloud Console API key.")
            client = genai.Client(api_key=key)  # ✅ this is correct
            return client, True  # indicate we're using SDK


        elif provider == "xai":
            from langchain_xai import ChatXAI
            key = api_keys.get("xai")
            if not key:
                raise ValueError("❌ Missing xAI API key.")
            return ChatXAI(api_key=key, model=model_name), False

        elif provider == "huggingface":
            from langchain.llms import HuggingFaceHub
            key = api_keys.get("huggingface")
            if not key:
                raise ValueError("❌ Missing HuggingFace API key.")
            return HuggingFaceHub(repo_id=model_name, huggingfacehub_api_token=key), False

        else:
            raise ValueError(f"❌ Unknown LLM provider: {provider}")

    def build_vectorstore(self, doc_path: str, save_path: str = "faiss_index"):
        if not os.path.exists(doc_path):
            raise FileNotFoundError(f"📂 Document not found at: {doc_path}")

        ext = os.path.splitext(doc_path)[-1].lower()

        if ext == ".txt":
            loader = TextLoader(doc_path)

        elif ext == ".csv":
            from langchain.document_loaders import CSVLoader
            loader = CSVLoader(doc_path)

        elif ext == ".json":
            from langchain.document_loaders import JSONLoader
            loader = JSONLoader(file_path=doc_path, jq_schema=".[]", text_content=False)

        elif ext == ".md":
            loader = TextLoader(doc_path)

        elif ext == ".pdf":
            from langchain.document_loaders import PyPDFLoader
            loader = PyPDFLoader(doc_path)

        elif ext == ".docx":
            from langchain.document_loaders import UnstructuredWordDocumentLoader
            loader = UnstructuredWordDocumentLoader(doc_path)

        else:
            raise ValueError(f"❌ Unsupported file type: {ext}")

        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        split_docs = splitter.split_documents(docs)

        print(f"📄 Loaded {len(split_docs)} chunks from {doc_path}")

        vectorstore = FAISS.from_documents(split_docs, self.embedding_model)
        vectorstore.save_local(save_path)
        print(f"✅ Vectorstore saved at: {save_path}")

    def query(self, question: str, index_path: str = "faiss_index"):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"❌ FAISS index not found at: {index_path}")

        vectorstore = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
        relevant_docs = vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""Answer the question based on the context below:\n\n{context}\n\nQuestion: {question}"""

        if self.use_sdk:
            model_name = self.config["llm"]["model"]  # ✅ Fix: get model name from config
            response = self.llm_model.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            answer = response.text
    
        else:
            qa = RetrievalQA.from_chain_type(
                llm=self.llm_model,
                retriever=vectorstore.as_retriever(),
                return_source_documents=False
            )
            answer = qa.run(question)

        print(f"🤖 Answer: {answer}")
        return answer
