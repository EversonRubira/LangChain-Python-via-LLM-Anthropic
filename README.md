# LangChain + Python via Anthropic API

Projeto desenvolvido durante o curso **"LangChain e Python: criando ferramentas com IA"** da [Alura](https://www.alura.com.br/), com adaptação para uso da **Anthropic API (Claude)** em vez da OpenAI.

---

## Sobre o projeto

O objetivo é aprender a usar o framework **LangChain** com Python para orquestrar modelos de linguagem, criar chatbots, agentes e sistemas de perguntas e respostas (RAG), substituindo os modelos GPT da OpenAI pelos modelos **Claude** da Anthropic.

### Módulos do curso

| Módulo | Conteúdo |
|---|---|
| Conectando à Anthropic | Configuração da API key, primeira chamada ao modelo Claude |
| Criando cadeias | Composição de prompts com `ChatPromptTemplate` e `StrOutputParser` |
| Interações com o chat | Histórico de conversa, contexto e memória |
| Orquestração | Encadeamento de múltiplas chains e lógica de decisão |
| Implementando RAG | Recuperação de documentos e respostas baseadas em arquivos próprios |

---

## Tecnologias utilizadas

- **Python 3.10+**
- **LangChain** — framework de orquestração de LLMs
- **langchain-anthropic** — integração LangChain com a API da Anthropic
- **FAISS** — busca por similaridade vetorial para RAG
- **PyPDF** — leitura de arquivos PDF
- **python-dotenv** — gerenciamento de variáveis de ambiente

---

## Pré-requisitos

- Python 3.10 ou superior instalado
- Conta na [Anthropic](https://console.anthropic.com/) com uma API key válida

---

## Configuração

**1. Clone o repositório**

```bash
git clone https://github.com/EversonRubira/LangChain-Python-via-LLM-Anthropic.git
cd LangChain-Python-via-LLM-Anthropic
```

**2. Crie e ative um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure a API key da Anthropic**

Crie um arquivo `.env` na raiz do projeto:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

> Nunca suba o arquivo `.env` para o repositório. Ele já está no `.gitignore`.

---

## Como executar

```bash
python main.py
```

O exemplo atual sugere uma cidade com base em um interesse informado, usando o modelo `claude-haiku-4-5` via LangChain.

---

## Estrutura do projeto

```
LangChain-Python-via-LLM-Anthropic/
├── main.py             # Ponto de entrada principal
├── requirements.txt    # Dependências do projeto
├── .env                # API key (não versionar)
└── README.md
```

---

## Diferenças em relação ao curso original (OpenAI → Anthropic)

| Curso original (OpenAI) | Este projeto (Anthropic) |
|---|---|
| `langchain-openai` | `langchain-anthropic` |
| `ChatOpenAI` | `ChatAnthropic` |
| `OPENAI_API_KEY` | `ANTHROPIC_API_KEY` |
| Modelos GPT-3.5 / GPT-4 | Modelos Claude (Haiku, Sonnet, Opus) |

---

## Referências

- [Documentação LangChain](https://python.langchain.com/)
- [Documentação Anthropic](https://docs.anthropic.com/)
- [langchain-anthropic no PyPI](https://pypi.org/project/langchain-anthropic/)
- [Curso original na Alura](https://www.alura.com.br/curso-online-langchain-python-criando-ferramentas-openai)
