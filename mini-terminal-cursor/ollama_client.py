import config

if MODE == "langchain":
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(
        model=config.OLLAMA_MODEL,
        temperature=config.OLLAMA_PARAMS["temperature"],
        top_p=config.OLLAMA_PARAMS["top_p"],
        repeat_penalty=config.OLLAMA_PARAMS["repeat_penalty"],
        max_tokens=config.OLLAMA_PARAMS["max_tokens"],
    )

    def query_ollama(prompt: str) -> str:
        template = ChatPromptTemplate.from_template("{question}")
        chain = template | llm
        return chain.invoke({"question": prompt})

else:
    import requests

    def query_ollama(prompt: str) -> str:
        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            **config.OLLAMA_PARAMS,
        }
        response = requests.post(config.OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
