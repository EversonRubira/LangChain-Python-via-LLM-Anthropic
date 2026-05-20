from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

numero_dias = 7
numero_criancas = 2
atividade = "musica" 

prompt = f"Crie um roteiro de viagem de {numero_dias}dias, para uma familia co {numero_criancas} criancas, que gosta de {atividade}"


cliente = Anthropic()

resposta = cliente.messages.create(
    model="claude-haiku-4-5",
    max_tokens = 1000,
    system="Voce é uma assitente de roteiro de viagens.",
    messages=[
       
        {
            "role" : "user",
            "content" : prompt
        }
    ]
)


resposta_em_texto = resposta.choice[0].message.content
print(resposta)