# Talk to Website
This project aims to develop a system capable of answering questions based on the content extracted from a website.

## Project Overview
The project consists of several key components:

### Web Crawler:

* A crawler that explores a specified base website and other pages within its domain.
* Returns the crawled HTML content in JSON format.

### Content Extractor:

* Cleans the HTML by removing unnecessary tags such as headers, footers, and navbars.
* Divides the cleaned HTML into chunks based on semantic similarity.
* Utilizes the CosineStrategy based on cosine similarity to group related content chunks and then converts these grouped html chunks into markdown format for better readability for the llm.

### Database Population:

* Converts the content chunks into vectors.
* Stores these vectors in a vector database (Chroma DB).

### Query Data:

* Allows users to input queries.
* Retrieves relevant content from the database based on the query.
* Utilizes a Language Model (LM), specifically Mistral, to generate answers based on the retrieved context.

Components and Technologies
Web Crawler: TypeScript based crawler which uses Playwright to crawl website.
Content Extractor: Implements semantic similarity and clustering using Python.
Database: Utilizes Chroma DB for storing vector representations of content chunks.
Query Processing: Integrates Mistral (a Language Model) for generating answers to user queries.
