import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
import locale 
from module import vignettenationale, gpt_from_api, extract_news, summarize_news
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

load_dotenv()
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Stocker l'historique des messages
history = StreamlitChatMessageHistory(key="chat_messages")

msgs = StreamlitChatMessageHistory(key="special_app_key")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")
    
# Chaine d'actions
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  
    input_messages_key="question",
    history_messages_key="history",
)

# """
# Sidebar : Clés APIs
# """
openai_key = st.sidebar.text_input('OpenAI key')
openai_key = os.environ["OPENAI_API_KEY"]
#vigilance_key = st.sidebar.text_input('Bulletin Vigilance key')
vigilance_key = os.environ["VIGILENCE_API_KEY"]

if openai_key:
    news = extract_news(vigilance_key)
    llm = gpt_from_api(openai_key)
    summary = summarize_news(llm, news)
else:
    summary = ""


# """
# Sidebar : Informations générales
# """
side = st.sidebar
day = date.today().strftime("%A %d").capitalize()
month = date.today().strftime("%B %Y").capitalize()
with side:
    with st.spinner():
        st.write('Informations générales')
        st.write(f"{day} {month}")
        st.write(summary)
        st.write('')
        st.write('Pour plus d\'informations posez vos questions à notre Chatbot')
        st.write('')
        st.write('https://vigilance.meteofrance.fr/fr')

# """
# Titre de l'application
# """
st.title('💬 Chatbot Vigilance Météo France')



# Affichage des messages
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# Interactions entre utilisateurs et chatbot
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": prompt}, config)
    st.chat_message("ai").write(response.content)







