import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
import locale 
from module import vignettenationale, gpt_from_api, extract_news, summarize_news
from dotenv import load_dotenv
import os
load_dotenv()

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# """
# Titre de l'application
# """
#st.title('Chatbot et Vigilance Météo France')

# """
# Sidebar : les champs Clés APIs
# """
openai_key = st.sidebar.text_input('OpenAI key')
openai_key = os.environ["OPENAI_API_KEY"]
vigilance_key = st.sidebar.text_input('Bulletin Vigilance key')
vigilance_key = os.environ["VIGILENCE_API_KEY"]
# """
# Sidebar : création des onglets
# """

# ONGLET 1 = Informations Vigilance
def onglet1():
    st.title('Informations Vigilance')
    st.write("")
    day = date.today().strftime("%A %d").capitalize()
    month = date.today().strftime("%B %Y").capitalize()
    st.write(f"{day} {month}")
    if openai_key :
        news = extract_news(vigilance_key)
        llm = gpt_from_api(openai_key)
        summary = summarize_news(llm, news)
        st.write(summary)
    else :
        st.write("")
    
    #division de la page en 2 colonnes
    col1, col2 = st.columns(2)
    
    #vignette Jour-J avec texte
    with col1:
        st.image(vignettenationale(vigilance_key, "J"), caption = "Aujourd'hui")
    
    
    #vignette Jour J+1 AVEC TEXTE
    with col2:
        st.image(vignettenationale(vigilance_key, "J1"), caption = "Demain")
    
    
    

# ONGLET 2 = Chatbot
def onglet2():
    st.title('💬 Chatbot')
    st.write('Contenu de la page Chatbot')
    st.text(openai_key)


# """
# Sidebar : affichage des onglets
# """
def main():
    with st.sidebar:
        selected_onglets = option_menu('', ['Informations Vigilance', 'Chatbot'],
                icons=['house', 'gear', 'gear'], menu_icon='cast', default_index=0)

    if selected_onglets == 'Informations Vigilance':
        onglet1()
    else:
        onglet2()

if __name__ == '__main__':
    main()



