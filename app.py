import ollama
import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.vectorstores import FAISS


embeddings = OllamaEmbeddings(model="mistral")
vectorstore = FAISS.load_local("./webkul_vectorDB", embeddings)



retriever = vectorstore.as_retriever()
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define the Ollama LLM function
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Define the RAG chain
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

# # Use the RAG chain
# result = rag_chain("What is webkul?")
# print(result)

iface = gr.Interface(
    fn=rag_chain,
    inputs="text",
    outputs="text",
    title="RAG Chain Question Answering",
    description="Enter a query to get answers from the RAG chain."
)

# Launch the app
iface.launch()

