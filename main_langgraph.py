from langchain_anthropic import Anthropic, ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

modelo = ChatAnthropic(
    model="claude-haiku-4-5",
    temperature=0.7,
    api_key=api_key
)

prompt_sugestao = ChatPromptTemplate.from_messages(

    [
        ("system", "Você é um assistente de viagem que sugere destinos e dicas de viagem. Apresente-se como Sr. Passeio."),
        ("human", "{query}")
    ]
)   

assistente = prompt_sugestao | modelo | StrOutputParser()

print(assistente.invoke({"query": "Sugira alguns paises na europa para visitar com meu filho menino de 11 anos, e a melhor epoca para visitar-los. Quais melhoresepocas economicamente falando para passagens aereas e hoteis baratos para essa viagem?"}))# teste
