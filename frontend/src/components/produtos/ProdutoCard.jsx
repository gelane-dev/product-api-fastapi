import { BotaoFavorito } from '../botoes/BotaoFavorito'
import './ProdutoCard.css'

export function ProdutoCard({ produtos }) {
    return (
        <div className="card-container">
            {produtos.map(produto => (
                <div key={produto.id} className="card-produto">
                    <img 
                        src={produto.imagem_url} 
                        alt={produto.name} 
                        className="card-imagem"
                    />
                    <div className="card-conteudo">
                        <h2 className="card-titulo">{produto.name}</h2>
                        <p className="card-preco">R$ {produto.preco}</p>
                    </div>
                    <div className="card-favorito-posicionador">
                        <BotaoFavorito />
                    </div>
                </div>
            ))}
        </div>
    )
}


