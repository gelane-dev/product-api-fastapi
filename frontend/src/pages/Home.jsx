import { useState, useEffect } from 'react'
import { ProdutoCard } from '../components/produtos/ProdutoCard'

export const Home = () => {
    const [produtos, setProdutos] = useState([])
    
    useEffect(() => {
        fetch("http://localhost:8001/produtos/")
            .then(resposta => resposta.json())
            .then(dados => {
                setProdutos(dados)
            })
    }, [])
    
    return (
         <ProdutoCard produtos={produtos} />
    )
}
