from database import conectar

def criar_tabela():
    def criar_tabela_produtos():

        banco = conectar()
        cursor = banco.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS produto(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            categoria VARCHAR(100),
            preco DECIMAL(10,2) NOT NULL,
            estoque INTEGER DEFAULT 0,
            data_criacao TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """)

        banco.commit()
        cursor.close()
        banco.close()

    criar_tabela_produtos()

    def criar_tabela_usuarios():

        banco = conectar()
        cursor = banco.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS usuarios(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            senha VARCHAR(255),
            data_criacao TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """)

        banco.commit()
        cursor.close()
        banco.close()

    criar_tabela_usuarios()

    def criar_tabela_pedidos():
    
        banco = conectar()
        cursor = banco.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS pedidos(
            id SERIAL PRIMARY KEY,
            usuarios_id INT,
            CONSTRAINT fk_usuarios
            FOREIGN KEY (usuarios_id)
            REFERENCES usuarios(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        );
        """)

        banco.commit()
        cursor.close()
        banco.close()

    criar_tabela_pedidos()

    def criar_tabela_itens_pedidos():
    
        banco = conectar()
        cursor = banco.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS itens_pedidos(
            id SERIAL PRIMARY KEY,
            quantidade INTEGER DEFAULT 0,
            pedidos_id INT,
            produto_id INT,
            CONSTRAINT fk_pedidos
            FOREIGN KEY (pedidos_id)
            REFERENCES pedidos(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
            CONSTRAINT fk_produto
            FOREIGN KEY (produto_id)
            REFERENCES produto(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
           );
           """)

        banco.commit()
        cursor.close()
        banco.close()

    criar_tabela_itens_pedidos()

criar_tabela()