# Global config for Ollama mode with values 'raw' or 'langchain'
MODE = None

# Ollama model settings
OLLAMA_URL = "http://localhost:11434/generate"
OLLAMA_MODEL = "llama3.2"
OLLAMA_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.95,
    "repeat_penalty": 1.1,
    "max_tokens": 2048,
}
