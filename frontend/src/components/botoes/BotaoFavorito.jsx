import { useState } from 'react'
import './BotaoFavorito.css'

export function BotaoFavorito() {
    const [favoritado, setFavoritado] = useState(false)
    const handleClick = () => {
        setFavoritado(!favoritado)
    }
    
    return (
        <button className="botao-favoritar" onClick={handleClick} aria-label="Favoritar produto">
            <span className="icone-favorito">
                {favoritado ? "❤️" : "🤍"}
            </span>
            <span className="texto-favorito">
                {favoritado ? "Favoritado" : "Favoritar"}
            </span>
        </button>
    )
}
