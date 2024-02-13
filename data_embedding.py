import os
import ollama
import pandas as pd
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from tqdm import tqdm

# from dotenv import load_dotenv

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')








dataset = pd.read_csv('new_webkul_dataset.csv')
raw_text = DataFrameLoader(dataset, page_content_column="body")

text_chunks = raw_text.load_and_split(
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, length_function=len
        )
    )
for doc in text_chunks:
        title = doc.metadata["title"]
        # description = doc.metadata["description"]
        content = doc.page_content
        url = doc.metadata["url"]
        final_content = f"TITLE: {title}\BODY: {content}\nURL: {url}"
        # final_content = f"TITLE: {title}\DESCRIPTION: {description}\BODY: {content}\nURL: {url}"
        doc.page_content = final_content
print(len(text_chunks))



# Download embeddings from OpenAI
# embeddings = OpenAIEmbeddings()
embeddings = OllamaEmbeddings(model="mistral")


if not os.path.exists("./webkul_vectorDB"):
    print("CREATING DB")
    vectorstore = FAISS.from_documents(
        text_chunks, embeddings
    )
    print("Okay done")


# if not os.path.exists("./webkul_vectorDB"):
#     print("CREATING DB")
#     vectorstore = FAISS.from_documents(
#         text_chunks[:1], embeddings
#     )
#     for i in tqdm(range(2,4355),desc="Vectors"):
#         temp = FAISS.from_documents(
#                 text_chunks[1:i], embeddings
#             )
#         vectorstore.merge_from(temp)


# if not os.path.exists("./webkul_vectorDB"):
#     print("CREATING DB")
#     vectorstore = FAISS.from_documents(
#         text_chunks[:354], embeddings
#     )
#     n2 = 354
#     while(n2<4354):
#         n1 = n2
#         n2 = n1 + 500
#         temp = FAISS.from_documents(
#                 text_chunks[n1:n2], embeddings
#             )
#         vectorstore.merge_from(temp)


    vectorstore.save_local("./webkul_vectorDB")





