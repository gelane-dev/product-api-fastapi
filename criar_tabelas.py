from database import conectar

def criar_tabela_produtos():

    banco = conectar()
    cursor = banco.cursor()

    sql = """ CREATE TABLE produto(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        categoria VARCHAR(100),
        preco DECIMAL(10,2) NOT NULL,
        estoque INTEGER DEFAULT 0,
        data_criacao TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(sql)
    banco.commit()
    cursor.close()
    banco.close()

criar_tabela_produtos()