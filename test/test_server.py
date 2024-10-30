import requests

BASE_URL = "http://127.0.0.1:8000/jarvis"

def test_listar_produtos():
    response = requests.get(f"{BASE_URL}/produtos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test_cadastrar_produto():
    novo_produto = {
        "nm_produto": "Produto Teste",
        "ds_categoria": "Categoria Teste",
        "nr_preco": 99.99,
        "st_produto": "D",
        "ds_produto": "Descrição do Produto Teste",
        "nr_tamanho": "M"
    }
    response = requests.post(f"{BASE_URL}/produtos", json=novo_produto)
    assert response.status_code == 201
    data = response.json()
    assert data["nm_produto"] == novo_produto["nm_produto"]
    assert data["nr_preco"] == novo_produto["nr_preco"]
