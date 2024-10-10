import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings  # Still using the deprecated class for now
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import TextLoader

def process_candidate(check):
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(api_key=check)

    # Manually handle file reading with 'errors=ignore'
    try:
        with open('combined_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Save the content into a temporary file for processing
    with open('temp_combined_text.txt', 'w', encoding='utf-8') as temp_file:
        temp_file.write(file_content)

    # Load documents using TextLoader (no need for 'errors' argument here)
    loader = TextLoader('temp_combined_text.txt', encoding='utf-8')
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(separators=[" ", ",", "\n"], chunk_size=4000, chunk_overlap=100, length_function=len)
    chunks = text_splitter.split_documents(documents)

    # Initialize the combined vectorstore
    combined_vectorstore = None

    def process_chunk(chunk):
        try:
            return FAISS.from_documents(documents=[chunk], embedding=embeddings)
        except Exception as e:
            print(f"Error processing chunk: {e}")
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result is not None:
                    if combined_vectorstore is None:
                        combined_vectorstore = result
                    else:
                        combined_vectorstore.merge_from(result)
                    print("Successfully processed and merged a chunk.")
            except Exception as e:
                print(f"Exception while processing a chunk: {e}")

    # Save the combined vectorstore
    if combined_vectorstore is not None:
        combined_vectorstore.save_local("embeddings")

    # Cleanup the temporary file
    os.remove('temp_combined_text.txt')

# Example usage
if __name__ == "__main__":
    process_candidate("")
