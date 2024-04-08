import streamlit as st

from langchain_openai import ChatOpenAI
from datetime import date

import locale 

from streamlit_extras.stylable_container import stylable_container 

from module import extract_news, summarize_news, create_retriever, rag_chain_with_history

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

load_dotenv()
vigilance_key = os.environ["VIGILENCE_API_KEY"]
openai_key = os.environ["OPENAI_API_KEY"]

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Import llm, retriever & rag
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
retriever = create_retriever()
chain = rag_chain_with_history(llm, retriever)


# Stocker l'historique des messages
history = StreamlitChatMessageHistory(key="chat_messages")

msgs = StreamlitChatMessageHistory(key="special_app_key")
if len(msgs.messages) == 0:
    msgs.add_ai_message("Comment puis-je vous aider ?")
    
# Chaine d'actions
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  
    input_messages_key="question",
    history_messages_key="chat_history",
)

# """
# Sidebar : Clés APIs
# """
#openai_key = st.sidebar.text_input('OpenAI key')

#vigilance_key = st.sidebar.text_input('Bulletin Vigilance key')

if openai_key:
    if 'sumary' not in st.session_state:
        news = extract_news(vigilance_key)
        st.session_state['sumary'] = summarize_news(llm, news)
else:
    st.session_state['sumary'] = ""


# """
# Sidebar : Informations générales
# """
side = st.sidebar
# Ajout du logo
side.image('logo.png')
#Ajout de la date
day = date.today().strftime("%A %d").capitalize()
month = date.today().strftime("%B %Y").capitalize()
with side:
    with st.spinner():
        st.title('📌Informations générales')
        st.write(f"📆**{day} {month}**")
        st.write(st.session_state['sumary'].content)
        st.write('')
        st.write('🖐️*Pour plus d\'informations posez vos questions à notre Chatbot*')
        st.write('')
        st.write('🔗https://vigilance.meteofrance.fr/fr')

# """
# Titre de l'application
# """


# Définition du style du conteneur
container_style = """
    {
        border: 5px solid #c71585;
        border-radius: 20px;
        padding: 40px;
        background-color: white;
        width:800px;
    }
"""
with stylable_container(
    key="chatbot_container",
    css_styles=container_style
):
    st.title('💬 Chatbot Vigilance Météo France')
    # Affichage des messages
    for msg in msgs.messages:
        st.chat_message(msg.type, avatar='🤖').write(msg.content)

    # Interactions entre utilisateurs et chatbot
    if prompt := st.chat_input("Posez votre question"):
        st.chat_message("human", avatar='🧑‍💻').write(prompt)
        config = {"configurable": {"session_id": "any"}}
        response = chain_with_history.stream({"question": prompt, "vigilance":st.session_state['sumary']}, config)
        st.chat_message("ai", avatar='🤖').write_stream(response)







