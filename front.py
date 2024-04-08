import streamlit as st
from streamlit_option_menu import option_menu

# """
# Titre de l'application
# """
#st.title('Chatbot et Vigilance Météo France')

# """
# Sidebar : les champs Clés APIs
# """
openai_key = st.sidebar.text_input('OpenAI key')
vigilance_key = st.sidebar.text_input('Bulletin Vigilance key')

# """
# Sidebar : création des onglets
# """

# ONGLET 1 = Accueil
def onglet1():
    st.title('Accueil')
    st.write('Contenu de la page Accueil')
    st.text(openai_key)
    
    
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



