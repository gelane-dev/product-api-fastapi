# API de E-commerce — FastAPI + PostgreSQL + SQLAlchemy
 
Projeto de estudo que começou como um CRUD simples de produtos e evoluiu para uma **API de e-commerce completa**, com cadastro e autenticação de usuários, controle de acesso (admin/cliente), pedidos com regras de negócio e persistência via **SQLAlchemy + Alembic**.
 
## 🚀 Funcionalidades
 
### Usuários e autenticação
| Método | Rota         | Descrição                                  | Acesso  |
|--------|--------------|---------------------------------------------|---------|
| POST   | `/cadastro/` | Cria um novo usuário (senha salva em hash)   | Público |
| POST   | `/login/`    | Autentica e retorna um token JWT             | Público |
 
### Produtos
| Método | Rota              | Descrição                          | Acesso  |
|--------|-------------------|-------------------------------------|---------|
| GET    | `/produtos/`      | Lista todos os produtos cadastrados | Público |
| POST   | `/produtos/`      | Cria um novo produto                | Admin   |
| PUT    | `/produtos/{id}`  | Atualiza um produto existente       | Admin   |
| DELETE | `/produtos/{id}`  | Remove um produto                   | Admin   |
 
### Pedidos
| Método | Rota                     | Descrição                                                        | Acesso           |
|--------|--------------------------|--------------------------------------------------------------------|------------------|
| POST   | `/pedidos/`              | Cria um pedido com um ou mais itens, valida estoque e calcula total | Usuário logado   |
| PUT    | `/pedidos/{id}/status`   | Atualiza o status do pedido (`pendente → pago → enviado`, com validação de transição; cancelamento devolve estoque) | Admin |
 
## 🛠️ Tecnologias utilizadas
 
- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
- [PostgreSQL](https://www.postgresql.org/) — banco de dados
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — migrations do banco
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [passlib (bcrypt)](https://passlib.readthedocs.io/) — hash de senha
- [python-jose](https://github.com/mpdavis/python-jose) — geração e validação de JWT
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente
## 📁 Estrutura do projeto
 
```
.
├── main.py             # Rotas da API (endpoints)
├── models.py            # Modelos SQLAlchemy (Produto, Usuario, Pedido, ItensPedido)
├── schemas.py           # Modelos Pydantic (validação dos dados)
├── auth.py               # Hash de senha, criação/validação de JWT, dependências de autorização
├── database.py           # Engine, Session e conexão com o PostgreSQL
├── alembic/                # Migrations do banco
├── alembic.ini              # Configuração do Alembic
├── requirements.txt          # Dependências do projeto
├── .env.example                # Exemplo de variáveis de ambiente
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
 
Edite o `.env` com as credenciais do seu banco e a chave usada para assinar o token:
 
```
DB_HOST=localhost
DB_NAME=primeiro_api
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_PORT=5432
 
SECRET_KEY=sua_chave_secreta_aqui
```
 
### 5. Crie o banco e aplique as migrations
 
No PostgreSQL, crie o banco (ex.: `primeiro_api`) e depois rode as migrations do Alembic:
 
```bash
alembic upgrade head
```
 
### 6. Suba a aplicação
 
```bash
uvicorn main:app --reload
```
 
A API estará disponível em `http://127.0.0.1:8000`.
 
A documentação interativa (Swagger) é gerada automaticamente em:
`http://127.0.0.1:8000/docs`
 
## 📌 Exemplo de uso
 
**Cadastro de usuário** — `POST /cadastro/`
```json
{
  "name": "Leonardo",
  "email": "leonardo@email.com",
  "senha": "senha123"
}
```
 
**Login** — `POST /login/`
```json
{
  "email": "leonardo@email.com",
  "senha": "senha123"
}
```
Retorna um `access_token` que deve ser enviado no header `Authorization: Bearer <token>` nas rotas protegidas.
 
**Criar pedido** — `POST /pedidos/`
```json
{
  "itens": [
    { "produto_id": 1, "quantidade": 2 },
    { "produto_id": 3, "quantidade": 1 }
  ]
}
```
 
## 🧠 Aprendizados deste projeto
 
- Modelagem de banco relacional com SQLAlchemy (relationships, foreign keys) e migrations com Alembic
- Autenticação com hash de senha (bcrypt) e tokens JWT
- Autorização por papel de usuário (admin x cliente) usando dependências do FastAPI
- Transações que envolvem múltiplas tabelas (pedido + itens do pedido) com controle de estoque
- Máquina de estados para status de pedido, com validação de transições permitidas
- Tratamento de erros de banco com `HTTPException` e rollback em caso de falha
## 🔜 Próximos passos
 
- [ ] Testes automatizados (pytest)
- [ ] Dockerizar a aplicação e subir `docker-compose.yml` (API + Postgres)
- [ ] Deploy público (Render ou Railway)
- [ ] Paginação no `GET /produtos/`
- [ ] Frontend consumindo essa API, formando um e-commerce completo de ponta a ponta
## 📄 Licença
 
Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.