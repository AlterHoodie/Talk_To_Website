import argparse
import os
import shutil
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma
import json
from database.processor import *
CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print(" Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    add_to_chroma(documents)
    print('Finished')

def add_to_db(data):
    documents = load_documents(data)
    add_to_chroma(documents)
    print('Finished')

def load_documents(data):
    docs = []
    # Load JSON File 
    url_links = []
    
    crawler = create_crawler()
    for page in data:
        i=0
        page_title = page['title']
        page_url = page['url']
        page_chunks = processor(page_url,page['html'],crawler,url_links,100)
        for chunk in page_chunks:
            metadata = {"title":page_title,"url":page_url,"id":f"{page_url}:{i}"}
            i+=1
            # print(metadata)
            # print(chunk)
            docs.append(Document(page_content=chunk,metadata=metadata))

    return docs


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    # chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    
    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f" Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        print('Finished')
        db.persist()
    else:
        print(" No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        url = chunk.metadata.get("url")
        chunk_id = chunk.metadata.get("id")
        # current_page_id = f"{url}:{chunk_id}"

        # # If the page ID is the same as the last one, increment the index.
        # if current_page_id == last_page_id:
        #     current_chunk_index += 1
        # else:
        #     current_chunk_index = 0

        # # Calculate the chunk ID.
        # chunk_id = f"{current_page_id}:{current_chunk_index}"
        # last_page_id = current_page_id

        # # Add it to the page meta-data.
        chunk.metadata["id"] = f"{url}:{chunk_id}"
        print(chunk.metadata)
    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
