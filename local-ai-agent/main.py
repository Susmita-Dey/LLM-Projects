# type: ignore
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
# create a prompt template with the above template
prompt = ChatPromptTemplate.from_template(template)
# chain the prompt with the model thus combining multiple things together to run our loop.
chain = prompt | model

while True:
    print("\n\n------------------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)
