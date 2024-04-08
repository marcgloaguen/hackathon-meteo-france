import requests
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv
import time
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

with open("contextualize_system_prompt.txt", "r") as files:
    contextualize_system_prompt = files.read()

with open("instruct.txt", "r") as files:
    instruct = files.read()


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


def create_retriever(path: str = "data/Vigilance Table.csv"):
    loader = CSVLoader(file_path=path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(data)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    return retriever


def contextualize_chain(llm):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm | StrOutputParser()
    return chain


def rag_chain_with_history(llm, retriever):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruct),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    def contextualized_question(input: dict):
        if input.get("chat_history"):
            return contextualize_chain(llm)
        else:
            return input["question"]

    chain = (
            RunnablePassthrough.assign(context=contextualized_question | retriever)
            | prompt
            | llm
    )

    return chain
