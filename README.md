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

### Desafio 03
Em desenvolvimento.
