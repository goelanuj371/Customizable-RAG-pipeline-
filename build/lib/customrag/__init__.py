def _init_embedding_model(self):
    provider = self.config["embedding"]["provider"]
    model_name = self.config["embedding"]["model"]
    api_keys = self.config.get("api_keys", {})

    if provider == "sentence-transformers":
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(model_name)

    elif provider == "openai":
        from langchain.embeddings import OpenAIEmbeddings
        openai_key = api_keys.get("openai")
        if not openai_key:
            raise ValueError("❌ OpenAI API key missing in config.")
            return OpenAIEmbeddings(model=model_name, openai_api_key=openai_key)

    elif provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        gemini_key = api_keys.get("gemini")
        if not gemini_key:
            raise ValueError("❌ Gemini Cloud Console key missing in config.")
            return GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=gemini_key)

    elif provider == "gemini_studio":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        studio_key = api_keys.get("gemini_studio")
        if not studio_key:
            raise ValueError("❌ Gemini Studio API key missing in config.")
            return GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=studio_key)

    elif provider == "huggingface":
        from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
        hf_token = api_keys.get("huggingface")
        if not hf_token:
            raise ValueError("❌ HuggingFace API key missing in config.")
            return HuggingFaceInferenceAPIEmbeddings(api_key=hf_token, model_name=model_name)

    elif provider == "xai":
        from langchain_xai import XAIEmbeddings
        xai_key = api_keys.get("xai")
        if not xai_key:
            raise ValueError("❌ xAI API key missing in config.")
            return XAIEmbeddings(api_key=xai_key, model=model_name)

    else:
        raise ValueError(f"❌ Unknown embedding provider: {provider}")
