# Vector search is a database; it's gonna be hosted locally on our own computer using something called ChromaDB. This allows us to quickly look up relevant information that we can then pass to our model in order to get some contextually relevant information from the model.
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv("realistic_restaurant_reviews.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={
                "rating": row["Rating"],
                "date": row["Date"],
            },
            id=str(i),  # Use the index as the ID
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings,
)

# if directory doesn't exists, add documents to vector store
if add_documents:
    vector_store.add_documents(documents)
    vector_store.persist()

# this is the retriever that we will use to look up documents in the vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
