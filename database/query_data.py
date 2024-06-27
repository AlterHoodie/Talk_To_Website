import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import time
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:
Even if little context is given answer from that context only
{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    start_time = time.time()
    query_rag(query_text)
    end_time = time.time()
    time_taken = end_time - start_time
    print("Time taken:",time_taken,"seconds")


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    print("Context retrieved")

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text,question=query_text)
    # print(prompt) 

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc in results]
    print(sources)
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)
    print(response_text)
    return response_text


if __name__ == "__main__":
    main()
