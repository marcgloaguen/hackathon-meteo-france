import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
from module import vignettenationale, gpt_from_api, extract_news, summarize_news
from dotenv import load_dotenv
import os
load_dotenv()



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

# ONGLET 1 = Accueil
def onglet1():
    st.title('Accueil')
    st.write('Contenu de la page Accueil')
    d_day = date.today().strftime("%d/%m/%Y")
    st.write(d_day)
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
        st.image(vignettenationale(vigilance_key, "J"))
    
    
    #vignette Jour J+1 AVEC TEXTE
    with col2:
        st.image(vignettenationale(vigilance_key, "J1"))
    
    
    
# ONGLET 2 = Présentation
def onglet2():
    st.title('Présentation')
    st.write('Contenu de la page Présentation')
    st.text(openai_key)
# ONGLET 3 = Chatbot
def onglet3():
    st.title('💬 Chatbot')
    st.write('Contenu de la page Chatbot')
    st.text(openai_key)


# """
# Sidebar : affichage des onglets
# """
def main():
    with st.sidebar:
        selected_onglets = option_menu('', ['Accueil', 'Prédictions', 'Chatbot'],
                icons=['house', 'gear', 'gear'], menu_icon='cast', default_index=0)

    if selected_onglets == 'Accueil':
        onglet1()
    elif selected_onglets == 'Prédictions':
        onglet2()
    else:
        onglet3()

if __name__ == '__main__':
    main()



