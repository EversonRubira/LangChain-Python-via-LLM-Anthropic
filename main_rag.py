from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader as PdfLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

modelo = ChatAnthropic(
    model="claude-haiku-4-5",
    temperature=0.7,
    api_key=api_key
)

embeddings = HuggingFaceEmbeddings()

arquivos = [
    "/workspaces/LangChain-Python-via-LLM-Anthropic/GTB_gold_Nov23.pdf",
    "/workspaces/LangChain-Python-via-LLM-Anthropic/GTB_platinum_Nov23.pdf",
    "/workspaces/LangChain-Python-via-LLM-Anthropic/GTB_standard_Nov23.pdf"
]

documentos = sum(
    [PdfLoader(arquivo).load() for arquivo in arquivos],
    []  
)


pieces = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(documentos)

dados_recuperados = FAISS.from_documents(pieces, embeddings).as_retriever(search_kwargs={"k": 3})

prompt_consulta_seguro = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda a pergunta com base nas informações recuperadas do documento fornecido. Caso co"),
        ("human", "{query}\n\nContexto:\n{contexto}\n\nResposta:")
    ]
)   

cadeia = prompt_consulta_seguro | modelo | StrOutputParser()

def responder(pergunta: str):
    contexto = dados_recuperados.invoke(pergunta)
    print("Chunks recuperados:", len(contexto))
    contexto = "\n".join([item.page_content for item in contexto])
    return cadeia.invoke({
        "query": pergunta,
        "contexto": contexto
    })

print(responder("Como proceder caso tenha um item furtado?"))