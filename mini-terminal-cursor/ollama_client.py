import config
from utils.logger import log_info

MODE = config.MODE

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
        try:
            return chain.invoke({"question": prompt})
        except Exception as e:
            log_info("[red]❌ Could not connect to Ollama server. Is it running?[/red]")
            log_info(f"[red]Error: {e}[/red]")
            exit(1)

else:
    import requests

    def query_ollama(prompt: str) -> str:
        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            **config.OLLAMA_PARAMS,
        }
        try:
            response = requests.post(config.OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            log_info("[red]❌ Could not connect to Ollama server. Is it running?[/red]")
            log_info(f"[red]Error: {e}[/red]")
            exit(1)
