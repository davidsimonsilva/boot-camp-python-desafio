# Desafios Python - DIO

Repositório criado para armazenar os desafios desenvolvidos durante meus estudos de Python e back-end.

Atualmente atuo mais na área de front-end, mas estou utilizando esses projetos para praticar lógica, orientação a objetos e desenvolvimento back-end.

## Tecnologias e ferramentas

- Python
- VSCode
- Git/GitHub
- Copilot
- Ollama
- Antigravity

## Desafios

### Desafio 01 - Sistema Bancário

Projeto de terminal simulando:

- depósito
- saque
- histórico
- conta corrente

Conceitos praticados:

- orientação a objetos
- herança
- abstração
- encapsulamento

📂 Pasta:

```bash
desafio-01-sistema-bancario/
```

---

### Desafio 02 - Sistema Bancário Assíncrono com FastAPI

Desenvolvimento de uma API RESTful moderna para gerenciamento de operações bancárias, utilizando autenticação e alta performance.

Conceitos praticados:

- Desenvolvimento de APIs RESTful com FastAPI
- Programação Assíncrona (I/O não-bloqueante)
- Modelagem de dados relacional assíncrona com SQLAlchemy 2.0
- Segurança e criptografia de senhas com Bcrypt
- Autenticação e autorização via Tokens JWT (JSON Web Tokens)
- Validação estrita de dados com Pydantic
- Documentação interativa automatizada (OpenAPI/Swagger)

📂 Pasta:

```bash
desafio-02-sistema-bancario-assincrono/
```

Para testar esse projeto siga os seguintes passos:

Navegue até a pasta do desafio e instale as dependências:

```
pip install fastapi uvicorn sqlalchemy aiosqlite python-jose[cryptography] "passlib[bcrypt]" python-multipart
```

Inicialize o servidor Uvicorn:

```
python -m uvicorn main:app --reload
```

Abra o navegador no endereço: http://127.0.0.1:8000/docs

Crie um usuário no endpoint POST /auth/register.

Clique no botão verde Authorize no topo da página, insira suas credenciais para liberar os endpoints protegidos e teste as funções de depósito (deposit), saque (withdraw) com validação de saldo e extrato.

---

### Desafio 03 - Miniguia de Estudos Ativos com NotebookLM

Construção de um ecossistema de aprendizagem e curadoria de conhecimento focado na **Guerra Fria e na Corrida Espacial (Do Sputnik à Era 2.0)**. O projeto exercita o uso de Inteligência Artificial para análise crítica de dados históricos e mitigação de alucinações de LLMs através de fontes controladas.

Conceitos praticados:

- Curadoria e ancoragem de fontes estruturadas (RAG)
- Engenharia de Prompts (Técnicas de _Role-Play_, _Few-Shot_ e Refinamento de Contexto)
- Análise de Geopolítica, Tecnologia de Natureza Dual e Legados Civis
- Documentação de processos de _Troubleshooting_ de IA ("Cicatrizes")

📖 **[CLIQUE AQUI PARA VER A DOCUMENTAÇÃO COMPLETA E O GUIA DE PROMPTS](desafio-03-miniguia-guerra-fria-notebooklm/README.md)**  
_(Acesse a pasta do projeto para visualizar o infográfico, o glossário de conceitos e o guia interativo de estudos)_

🧠 **[ACESSAR O CADERNO PÚBLICO NO NOTEBOOKLM](https://notebooklm.google.com/notebook/58cf7cdc-a164-44ea-a6e0-e1222f76308a)**

📂 Pasta do projeto:

```bash
desafio-03-miniguia-guerra-fria-notebooklm/
```
