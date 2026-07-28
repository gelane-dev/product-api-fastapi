# API de Produtos — FastAPI + PostgreSQL

Projeto de estudo criado para aprender os fundamentos de desenvolvimento de APIs REST com **FastAPI**, integração com banco de dados **PostgreSQL** (via `psycopg2`) e validação de dados com **Pydantic**.

## 🚀 Funcionalidades

A API implementa um CRUD completo de produtos:

| Método | Rota            | Descrição                          |
|--------|-----------------|-------------------------------------|
| GET    | `/produtos/`    | Lista todos os produtos cadastrados |
| POST   | `/produtos/`    | Cria um novo produto                |
| PUT    | `/produtos/{id}`| Atualiza um produto existente       |
| DELETE | `/produtos/{id}`| Remove um produto                   |

## 🛠️ Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
- [PostgreSQL](https://www.postgresql.org/) — banco de dados
- [psycopg2](https://www.psycopg2.org/) — driver de conexão com o Postgres
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente

## 📁 Estrutura do projeto

```
.
├── main.py             # Rotas da API (endpoints)
├── database.py         # Conexão com o PostgreSQL
├── schemas.py          # Modelos Pydantic (validação dos dados)
├── criar_tabelas.py    # Script para criar a tabela "produto"
├── requirements.txt    # Dependências do projeto
├── .env.example        # Exemplo de variáveis de ambiente
└── .gitignore
```

## ⚙️ Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/gelane-dev/product-api-fastapi.git
cd product-api-fastapi
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o `.env` com as credenciais do seu banco:

```
DB_HOST=localhost
DB_NAME=primeiro_api
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_PORT=5432
```

### 5. Crie o banco de dados e a tabela

No PostgreSQL, crie o banco (ex.: `primeiro_api`) e depois rode:

```bash
python criar_tabelas.py
```

### 6. Suba a aplicação

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger) é gerada automaticamente em:
`http://127.0.0.1:8000/docs`

## 📌 Exemplo de payload (POST/PUT)

```json
{
  "name": "Teclado mecânico",
  "categoria": "Periféricos",
  "preco": 250.90,
  "estoque": 15
}
```

## 🧠 Aprendizados deste projeto

- Criação de rotas REST com FastAPI
- Validação de entrada com Pydantic (`BaseModel`)
- Conexão e queries com PostgreSQL usando `psycopg2`
- Tratamento de erros com `HTTPException`
- Uso de variáveis de ambiente com `python-dotenv`

## 🔜 Possíveis melhorias futuras

- [ ] Usar um ORM (SQLAlchemy) em vez de SQL puro
- [ ] Adicionar testes automatizados (pytest)
- [ ] Adicionar paginação no GET `/produtos/`
- [ ] Usar Alembic para migrações de banco
- [ ] Adicionar autenticação (JWT)
- [ ] Dockerizar a aplicação

## 📄 Licença

Projeto de estudo, livre para uso e modificação.
