from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")



modelo_cidade = ChatPromptTemplate.from_template(
    template = """
    Sugira uma cidade dado o seu interesse por {interesse}.
    """,
   
)

modelo = ChatAnthropic(
    model="claude-haiku-4-5",
    temperature=0.7,
    api_key=api_key
)

cadeia = modelo_cidade | modelo | StrOutputParser

resposta = cadeia.invoke(
    {
        "interesse" : "praias"
    }
)

print(resposta)

