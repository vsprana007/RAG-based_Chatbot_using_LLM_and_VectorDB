from langchain.llms import Ollama
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
def get_conversation_chain(vector_store:FAISS, system_message:str, human_message:str) -> ConversationalRetrievalChain:
    llm = Ollama(model='mistral')
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": ChatPromptTemplate.from_messages(
                [
                    system_message,
                    human_message,
                ]
            ),
        },
    )
    return conversation_chain





embeddings = OllamaEmbeddings(model="mistral")




system_message_prompt = SystemMessagePromptTemplate.from_template(
        """
        you are an ai assistent.
       
        If you don't know the answer, just say that you don't know. Do not use external knowledge.
        Be polite and helpful. 
        Make sure to reference your sources with quotes of the provided context as citations.
        \nContext: {context} \nAnswer:
        
        
        
        \nQuestion: {question} 
        
        
        """
)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
vector_store = FAISS.load_local("./webkul_vectorDB", embeddings)
if "vector_store" not in st.session_state:
    st.session_state.vector_store = vector_store
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

st.set_page_config(
    page_title="Webkul Chatbot",
    page_icon="🤖",
)

st.title("Webkul Chatbot")
st.subheader("Chat with AI Assistent At Webkul")
st.markdown(
    """
    This chatbot was created to answer questions about the Webkul.
    This chatbot is an ai assistent at webkul which provide information related to the webkul
    """
)
st.image("https://cdn.pixabay.com/photo/2017/05/10/19/29/robot-2301646_1280.jpg") 

user_question = st.text_input("Ask your question")
with st.spinner("Processing..."):
    if user_question:
        response = st.session_state.conversation({"question": user_question})
        st.session_state.chat_history = response["chat_history"]
        human_style = "background-color: #e6f7ff; border-radius: 10px; padding: 10px;"
        chatbot_style = "background-color: #f9f9f9; border-radius: 10px; padding: 10px;"

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                print(i,response["chat_history"])
                st.markdown(
                    f"<p style='text-align: right;'><b>User</b></p> <p style='text-align: right;{human_style}'> <i>{message.content}</i> </p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<p style='text-align: left;'><b>Chatbot</b></p> <p style='text-align: left;{chatbot_style}'> <i>{message.content}</i> </p>",
                    unsafe_allow_html=True,
                )
st.session_state.conversation = get_conversation_chain(
    st.session_state.vector_store, system_message_prompt, human_message_prompt
)


