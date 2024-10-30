from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from shared.database import *
from shared.dependencies import get_db

router = APIRouter(prefix="/jarvis")
 
class ProdutoResponse(BaseModel):
    id_produto: int
    nm_produto: str
    ds_categoria: str
    nr_preco: float
    st_produto: str
    ds_produto: str
    nr_tamanho: str

class ProdutoRequest(BaseModel):
    nm_produto: str
    ds_categoria: str
    nr_preco: float
    st_produto: str
    ds_produto: str
    nr_tamanho: str

class ClienteResponse(BaseModel):
    id_cliente: int
    nm_cliente: str
    nr_cpf: int
    nr_rg: int
    dt_nascimento: str
    cd_senha: str

class ClienteRequest(BaseModel):
    nm_cliente: str
    nr_cpf: int
    nr_rg: int
    dt_nascimento: str
    cd_senha: str

class TelefoneResponse(BaseModel):
    id_telefone: int
    id_cliente: int
    nr_telefone: int
    nr_ddd: int
    ds_telefone: str

class TelefoneRequest(BaseModel):
    id_cliente: int
    nr_telefone: int
    nr_ddd: int
    ds_telefone: str

# --------------------------------------------------------------------------------------------------------------

@router.get("/")
def api_working():
    return "API está rodando."

@router.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()  
    return produtos  

@router.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    
    clientes_response = []
    for cliente in clientes:
        cliente_dict = cliente.__dict__.copy()
        cliente_dict['dt_nascimento'] = str(cliente.dt_nascimento)  
        clientes_response.append(ClienteResponse(**cliente_dict))
    
    return clientes_response

@router.get("/telefones", response_model=List[TelefoneResponse])
def listar_telefones(db: Session = Depends(get_db)):
    telefones = db.query(Telefone).all()  
    print(f"Telefones encontrados: {telefones}")  
    return telefones

# --------------------------------------------------------------------------------------------------------------

@router.post("/produtos", response_model=ProdutoResponse, status_code=201)
def cadastrar_produto(produto_request: ProdutoRequest, db: Session = Depends(get_db)) -> ProdutoResponse:
    produto = Produto(
        nm_produto = produto_request.nm_produto,
        ds_categoria = produto_request.ds_categoria,
        nr_preco = produto_request.nr_preco,
        st_produto = produto_request.st_produto,
        ds_produto = produto_request.ds_produto,
        nr_tamanho = produto_request.nr_tamanho
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return ProdutoResponse(
        **produto.__dict__
    )

@router.post("/clientes", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(cliente_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    cliente = Cliente(
        nm_cliente=cliente_request.nm_cliente,
        nr_cpf=cliente_request.nr_cpf,
        nr_rg=cliente_request.nr_rg,
        dt_nascimento=cliente_request.dt_nascimento,  
        cd_senha=cliente_request.cd_senha
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    cliente_dict = cliente.__dict__.copy()
    cliente_dict['dt_nascimento'] = str(cliente.dt_nascimento)  

    return ClienteResponse(**cliente_dict)

@router.post("/telefones", response_model=TelefoneResponse, status_code=201)
def cadastrar_telefone(telefone_request: TelefoneRequest, db: Session = Depends(get_db)) -> TelefoneResponse:
    telefone = Telefone(
        id_cliente = telefone_request.id_cliente,
        nr_telefone = telefone_request.nr_telefone,
        nr_ddd = telefone_request.nr_ddd,
        ds_telefone = telefone_request.ds_telefone
    )

    db.add(telefone)
    db.commit()
    db.refresh(telefone)

    return TelefoneResponse(
        **telefone.__dict__
    )

# --------------------------------------------------------------------------------------------------------------

@router.put("/produtos/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(id_produto: int, produto_request: ProdutoRequest, db: Session = Depends(get_db)) -> ProdutoResponse:
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto.nm_produto = produto_request.nm_produto
    produto.ds_categoria = produto_request.ds_categoria
    produto.nr_preco = produto_request.nr_preco
    produto.st_produto = produto_request.st_produto
    produto.ds_produto = produto_request.ds_produto
    produto.nr_tamanho = produto_request.nr_tamanho

    db.commit()
    db.refresh(produto)

    return ProdutoResponse(**produto.__dict__)

@router.put("/clientes/{id_cliente}", response_model=ClienteResponse)
def atualizar_cliente(id_cliente: int, cliente_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nm_cliente = cliente_request.nm_cliente
    cliente.nr_cpf = cliente_request.nr_cpf
    cliente.nr_rg = cliente_request.nr_rg
    cliente.dt_nascimento = cliente_request.dt_nascimento
    cliente.cd_senha = cliente_request.cd_senha

    db.commit()
    db.refresh(cliente)

    cliente_dict = cliente.__dict__.copy()
    cliente_dict['dt_nascimento'] = str(cliente.dt_nascimento)

    return ClienteResponse(**cliente_dict)

@router.put("/telefones/{id_telefone}", response_model=TelefoneResponse)
def atualizar_telefone(id_telefone: int, telefone_request: TelefoneRequest, db: Session = Depends(get_db)) -> TelefoneResponse:
    telefone = db.query(Telefone).filter(Telefone.id_telefone == id_telefone).first()
    if not telefone:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")

    telefone.id_cliente = telefone_request.id_cliente
    telefone.nr_telefone = telefone_request.nr_telefone
    telefone.nr_ddd = telefone_request.nr_ddd
    telefone.ds_telefone = telefone_request.ds_telefone

    db.commit()
    db.refresh(telefone)

    return TelefoneResponse(**telefone.__dict__)

# --------------------------------------------------------------------------------------------------------------

@router.delete("/produtos/{id_produto}", status_code=204)
def deletar_produto(id_produto: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}

@router.delete("/clientes/{id_cliente}", status_code=204)
def deletar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}

@router.delete("/telefones/{id_telefone}", status_code=204)
def deletar_telefone(id_telefone: int, db: Session = Depends(get_db)):
    telefone = db.query(Telefone).filter(Telefone.id_telefone == id_telefone).first()
    if not telefone:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")

    db.delete(telefone)
    db.commit()
    return {"message": "Telefone deletado com sucesso"}