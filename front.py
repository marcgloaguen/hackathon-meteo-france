import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from functions import extract_news, summarize_news, create_retriever, rag_chain_with_history

from datetime import date
import locale
from dotenv import load_dotenv
import os

load_dotenv()
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


def sidebar(llm):

    """
    Create and display the sidebar with general information and news summary.

    Parameters:
    - llm: Language model for summarizing news.
    """

    ############################################################################

    # Display current date and summarized news in the sidebar

    jour = date.today().strftime("%A %d").capitalize()
    mois_annee = date.today().strftime("%B %Y").capitalize()

    # Check if news summary is not already stored in session state, if not, summarize news

    if 'sumary' not in st.session_state:
        vigilance_key = os.environ["VIGILENCE_API_KEY"]
        news = extract_news(vigilance_key)
        st.session_state['sumary'] = summarize_news(llm, news)

    ############################################################################

    # Create sidebar elements

    with st.sidebar:
        st.image('logo.png')
        st.title('📌 Informations générales')
        st.write(f"📆 **{jour} {mois_annee}**")
        st.write(st.session_state['sumary'].content)
        st.write('')
        st.write('🗣️ *Pour plus d\'informations posez vos questions à notre Chatbot*')
        st.write('')
        st.write('🔗 https://vigilance.meteofrance.fr/fr')

    ############################################################################


def main_page(llm):

    """
    Display the main chat page and handle user interaction.

    Parameters:
    - llm: Language model for chatbot responses.
    """

    ############################################################################

    # Initialize chat message history, add initial AI message if history is empty

    msgs = StreamlitChatMessageHistory(key="chat_messages")
    if len(msgs.messages) == 0:
        msgs.add_ai_message("Comment puis-je vous aider ?")

    ############################################################################

    # Create retriever and chatbot chain with history

    retriever = create_retriever()
    chain = rag_chain_with_history(llm, retriever)
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="question",
        history_messages_key="chat_history")

    ############################################################################

    # Define CSS style for chat container

    container_style = """
        {
            border: 3px solid #c71585;
            border-radius: 20px;
            padding: 20px;
            background-color: white;
            width:800px;
        }
    """

    # Create chatbot container with specified CSS style
    with stylable_container(
            key="chatbot_container",
            css_styles=container_style
    ):
        st.title('💬 Chatbot Vigilance Météo France')
        msg_container = st.container(border=True, height=500)

    ############################################################################

    # Display chat history in the message container

        for msg in msgs.messages:
            msg_container.chat_message(msg.type, avatar='🐸').write(msg.content)

    ############################################################################

    # Allow user to input questions and receive responses from the chatbot

        if prompt := st.chat_input("Posez votre question"):
            msg_container.chat_message("human", avatar='👤').write(prompt)
            response = chain_with_history.stream(
                input={"question": prompt, "vigilance": st.session_state['sumary']},
                config={"configurable": {"session_id": "any"}}
            )
            msg_container.chat_message("ai", avatar='🐸').write_stream(response)

    ############################################################################


def main():
    # Set page configuration
    st.set_page_config(page_title="Météo France | Chatbot", page_icon="🐸")
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Initialize ChatOpenAI model
    gpt_turbo = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Display sidebar and main chat page
    sidebar(gpt_turbo)
    main_page(gpt_turbo)


if __name__ == "__main__":
    main()
