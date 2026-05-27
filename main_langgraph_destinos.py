from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from dotenv import load_dotenv
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
import asyncio
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

modelo = ChatAnthropic(
    model="claude-haiku-4-5",
    temperature=0.7,
    api_key=api_key
)

prompt_consultor_praia = ChatPromptTemplate.from_messages(

    [
        ("system", "Apresente-se como Sra Praia, vc é uma especialista em sugestões de praias"
        " para visitar."),
        ("human", "{query}")
    ]
)   

prompt_consultor_montanha = ChatPromptTemplate.from_messages(

    [
        ("system", "Apresente-se como Sra Montanha, vc é uma especialista em sugestões"
        "de lugares no interior para visitar com atividades para familia"),
        ("human", "{query}")
    ]
)   
cadeia_praia = prompt_consultor_praia | modelo | StrOutputParser()
cadeia_montanha = prompt_consultor_montanha | modelo | StrOutputParser()



prompt_roteador = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda apenas com {{\"destino\": \"praia\"}} ou {{\"destino\": \"montanha\"}}"),
        ("human", "{query}")    
        
    ]
)

roteador = prompt_roteador | modelo | JsonOutputParser()

class Estado(TypedDict):
    query: str
    destino: Literal["praia", "montanha"]
    resposta: str

async def no_roteador(estado: Estado, config=RunnableConfig):
    return {"destino": await roteador.ainvoke({"query":estado["query"]}, config)}


async def no_praia(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_praia.ainvoke({"query":estado["query"]}, config)}

async def no_montanha(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_montanha.ainvoke({"query":estado["query"]}, config)}

def escolher_no(estado : Estado):
    if estado["destino"] == "praia":
        return "praia"
    else:
        return "montanha"
    
grafo = StateGraph(Estado)
grafo.add_node("no_roteador", no_roteador)
grafo.add_node("praia", no_praia)
grafo.add_node("montanha", no_montanha)

grafo.add_edge(START, "no_roteador")
grafo.add_conditional_edges("no_roteador", escolher_no)
grafo.add_edge("praia", END)
grafo.add_edge("montanha", END)

app = grafo.compile()

async def main():
    resposta = await app.ainvoke({"query": "Sugira um destino de viagem em Portugal para mim e minha familia, que tem interesse em atividades ao ar livre, como caminhadas e passeios na natureza. Estamos procurando um lugar que ofereça uma variedade de trilhas e paisagens naturais para explorar, além de opções de lazer para crianças."})
    print(resposta["resposta"])

asyncio.run(main())