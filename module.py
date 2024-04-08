import requests
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os


def extract_text_items(data):
    text_items = []
    infos = [
        region for region in data['product']['text_bloc_items']
        if len(region['bloc_items']) != 0 and region['bloc_id'] == 'BULLETIN_DEPARTEMENTAL'
    ]
    for info in infos:
        for bloc_item in info.get('bloc_items', []):
            for text_item in bloc_item.get('text_items', []):
                for subdivision in text_item.get('term_items', []):
                    for subdivision_text in subdivision.get('subdivision_text', []):
                        text_items.append("".join(subdivision_text.get('text', '')))
    return text_items


def extract_news(vigilence_api_key: str) -> list:
    url = 'https://public-api.meteofrance.fr/public/DPVigilance/v1/textesvigilance/encours'
    headers = {
        'accept': '*/*',
        'apikey': vigilence_api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    news = list(set(extract_text_items(data)))

    return news


def summarize_news(llm, news: list) -> str:
    template = """
    Write a concise summary in french of the following:
    "{informations}"
    CONCISE SUMMARY:
    """
    prompt = PromptTemplate.from_template(template)
    chain = (
            {'informations': RunnablePassthrough()}
            | prompt
            | llm
    )
    summary = chain.invoke(news)
    return summary
