from langchain_anthropic import ChatAnthropic
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
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
        ("placeholder", "{historico}"),
        ("human", "{query}")
    ]
)

cadeia = prompt_sugestao | modelo | StrOutputParser()

menoria = {}

sessao = "sessao_langchain"

def historico_por_sessao(sessao : str):
    if sessao not in menoria:
        menoria[sessao] = InMemoryChatMessageHistory()
    return menoria[sessao]

perguntas = [
    "Sugira alguns paises na europa para visitar com meu filho "
    "menino de 11 anos, e a melhor epoca para visitar-los."
    "Quais melhoresepocas economicamente falando para passagens aereas e hoteis baratos para essa viagem?"
]

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=historico_por_sessao,
    input_messages_key="query",
    history_messages_key="historico"
)

for uma_pergunta in perguntas:
    resposta = cadeia_com_memoria.invoke(
        {
        "query": uma_pergunta,
        },
        config={"session_id": sessao}
    )
    print("Usuario: ", uma_pergunta),
    print("Assistente: ", resposta )

