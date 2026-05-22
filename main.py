```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import Field, BaseModel
from dotenv import load_dotenv
from langchain.globals import set_debug 
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

set_debug(True)

class Destino(BaseModel):
    cidade: str = Field(description="A cidade sugerida para o interesse do usuário.")
    motivo: str = Field(description="O motivo pelo qual a cidade é adequada para o interesse do usuário.")

class Estacionamento(BaseModel):
    cidade: str = Field(description="A cidade sugerida para o interesse do usuário.")
    motivo: str = Field(description="O motivo pelo qual a cidade é adequada para o interesse do usuário.")


parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_estacionamento = JsonOutputParser(pydantic_object=Estacionamento)


prompt_praia = ChatPromptTemplate.from_template(
    template="""
    Sugira uma cidade dado o seu interesse por {interesse}.
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}

)

prompt_estacionamento = ChatPromptTemplate.from_template(
    template="""
    Sugira lugares de mais facil acesso de carro para {interesse}.
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_estacionamento.get_format_instructions()}

)

prompt_localizacao = ChatPromptTemplate.from_template(
    template="Sugira uma praia para fazer snorkeling recreativo perto de {localizacao}, para {interesse}.",
    partial_variables={"localizacao": "Arrabida"}

)

modelo = ChatAnthropic(
    model="claude-haiku-4-5",
    temperature=0.7,
    api_key=api_key
)

cadeia = prompt_praia | modelo | parseador_destino
cadeia_2 = prompt_estacionamento | modelo | parseador_estacionamento
cadeia_3 = prompt_localizacao | modelo | StrOutputParser()

cadeia_final = (cadeia | (lambda x: {"interesse": x["cidade"]}) | cadeia_3)

resposta = cadeia_final.invoke(
    {
        "interesse" : "praias em Portugal (Arrabida)para fazer snorkeling"
    }
)

print(resposta)


