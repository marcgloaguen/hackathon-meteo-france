# Hackathon Météo France

## Chatbot d'Aide aux Intempéries et Vigilances Météo

Ce projet est un chatbot développé pour aider les utilisateurs pendant les intempéries et les vigilances météorologiques. Le chatbot utilise les données en temps réel de Météo France pour fournir des informations précises sur les conditions météorologiques et les alertes émises. Les utilisateurs peuvent poser des questions sur les prévisions météorologiques actuelles, les avertissements météo, ainsi que recevoir des conseils de sécurité en cas de vigilance.


## Fonctionnalités

- Fournit des informations en temps réel sur les conditions météorologiques et les vigilances émises par Météo France.
- Permet aux utilisateurs de poser des questions sur les prévisions météorologiques actuelles.
- Donne des alertes météo et des conseils pour rester en sécurité pendant les intempéries, en particulier en cas de vigilance.
## Installation

1. Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/marcgloaguen/hackathon-meteo-france.git
```
2. Accédez au répertoire du projet :
````bash
cd chatbot-aide-intemperies
````
3. Configuration des clés API. Créez un fichier `.env` à la racine du projet et ajoutez-y les clés API nécessaires :

   - `OPENAI_API_KEY` : Clé API OpenAI pour le modèle de langage.
   - `VIGILENCE_API_KEY` : Clé API Météo France pour accéder aux données de vigilance. Vous pouvez obtenir une clé sur [ce site](https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesVigilance).

4. Installez les dépendances requises :
````bash
pip install -r requirements.txt
````
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
