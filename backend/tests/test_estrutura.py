import pytest
from pydantic import ValidationError

from app.core.database import Base
from app.main import app
from app.models import StatusPedido
from app.schemas import CriarPedido, ItemPedidoIn
from app.services.pedido_service import TRANSICOES_VALIDAS


def test_transicoes_validas_de_pedido():
    assert TRANSICOES_VALIDAS == {
        StatusPedido.PENDENTE: [StatusPedido.PAGO, StatusPedido.CANCELADO],
        StatusPedido.PAGO: [StatusPedido.ENVIADO, StatusPedido.CANCELADO],
        StatusPedido.ENVIADO: [],
        StatusPedido.CANCELADO: [],
    }


@pytest.mark.parametrize("quantidade", [0, -1])
def test_item_nao_aceita_quantidade_nao_positiva(quantidade):
    with pytest.raises(ValidationError):
        ItemPedidoIn(produto_id=1, quantidade=quantidade)


def test_pedido_nao_aceita_lista_de_itens_vazia():
    with pytest.raises(ValidationError):
        CriarPedido(itens=[])


def test_modelos_preservam_tabelas_e_colunas():
    colunas = {
        nome: set(tabela.columns.keys())
        for nome, tabela in Base.metadata.tables.items()
    }
    assert colunas == {
        "produto": {"id", "name", "categoria", "preco", "estoque", "data_criacao"},
        "usuarios": {"id", "role", "name", "email", "senha", "data_criacao"},
        "pedidos": {"id", "usuario_id", "total", "status", "data_criacao"},
        "itens_pedidos": {
            "id",
            "quantidade",
            "preco_unitario",
            "pedidos_id",
            "produto_id",
        },
    }


def test_openapi_mantem_tags_e_caminhos():
    schema = app.openapi()
    tags = {
        tag
        for path in schema["paths"].values()
        for operation in path.values()
        if isinstance(operation, dict)
        for tag in operation.get("tags", [])
    }
    assert tags == {"Autenticação", "Produtos", "Pedidos"}
    assert set(schema["paths"]) == {
        "/login/",
        "/cadastro/",
        "/produtos/",
        "/produtos/{id}",
        "/pedidos/",
        "/pedidos/{id}/status",
    }