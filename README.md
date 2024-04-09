# Hackathon Météo France
<img src=screenshot.jpeg alt="Screenshot" style="max-height: 10px;" />


## Chatbot d'Aide aux Intempéries et Vigilances Météo
Ce projet est un chatbot développé pour rendre plus facile et ludique l'utilisation du site de Vigilence Météo France, en fournissant aux utilisateurs des informations météorologiques précises et des alertes de vigilance de manière conviviale. Le chatbot utilise les données en temps réel de Météo France pour fournir des informations actualisées sur les conditions météorologiques et les alertes émises. Il vise à simplifier le processus de recherche d'informations météorologiques et de vigilance en permettant aux utilisateurs de poser des questions sur les prévisions météorologiques actuelles, les avertissements météo et de recevoir des conseils de sécurité en cas de vigilance. L'objectif est de fournir un point centralisé et convivial pour obtenir toutes les informations nécessaires liées à la météo et aux conditions d'urgence, tout en offrant une expérience utilisateur améliorée par rapport au site Web de Météo France.

## Fonctionnalités

- Fournit des informations en temps réel sur les conditions météorologiques et les vigilances émises par Météo France.
- Permet aux utilisateurs de poser des questions sur les prévisions météorologiques actuelles.
- Donne des alertes météo et des conseils pour rester en sécurité pendant les intempéries, en particulier en cas de vigilance.
- Sensibilise les utilisateurs aux risques météorologiques et promeut la prévention en fournissant des conseils et des recommandations appropriés.

## Installation

1. Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/marcgloaguen/hackathon-meteo-france.git
```
2. Accédez au répertoire du projet :
````bash la de
cd hackathon-meteo-france
````
3. Configuration des clés API Météo France. Créez un fichier `.env` à la racine du projet et ajoutez-y la clé API :
   - `VIGILENCE_API_KEY` : Clé API Météo France pour accéder aux données de vigilance. Vous pouvez obtenir une clé sur [ce site](https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesVigilance).

4. Installez les dépendances requises :
````bash
pip install -r requirements.txt
````

## Choix du Modèle de Langage

Lors de l'utilisation du chatbot, vous avez le choix entre deux modèles de langage différents. Pour sélectionner le modèle souhaité, il vous suffit de modifier la ligne appropriée dans le fichier `front.py` :

- Pour utiliser le modèle **GPT-3.5-turbo** d'OpenAI, assurez-vous d'ajouter la clé API `OPENAI_API_KEY` dans le fichier `.env`, puis définissez le modèle comme suit :
  
```python
from langchain_openai import ChatOpenAI 
from langchain_openai import OpenAIEmbeddings
model = ChatOpenAI(model_name="gpt-3.5-turbo")
embedding = OpenAIEmbeddings()
 ```

- Si vous préférez utiliser le modèle ```Mistral7B``` via Ollama, vous pouvez le faire en utilisant la ligne suivante : : 

```python
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
model = ChatOllama(model="mistral")
embedding = OllamaEmbeddings(model="mistral")
```
En choisissant entre ces deux options, vous pouvez adapter le fonctionnement du chatbot selon vos préférences et les besoins spécifiques de votre projet.
## Utilisation

1. Assurez-vous que toutes les dépendances sont installées.
2. Exécutez l'application avec Streamlit :
````bash
streamlit run app.py
````
3. L'application devrait s'ouvrir dans votre navigateur par défaut. Vous pouvez désormais interagir avec le chatbot pour obtenir des informations météorologiques.

## Auteurs

- [Jeanne Hoffmann](https://github.com/Jemaveh)
- [Marc Gloaguen](https://github.com/marcgloaguen)

