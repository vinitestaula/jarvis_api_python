# Jarvis API - Challenge Sprints

- Pip's necessários: `pip install -r requirements.txt` 
- Para executar a API, inicie rodando o arquivo `main`
- Se API em execução
    - Acesso à documentação em `http://127.0.0.1:8000/docs`
    - Testes unitários com `pytest test_server.py` 

## Exemplos de Requisições JSON para Endpoints

### Tabela Cliente
- **POST**: Criação de Cliente  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/clientes`  
  - **Corpo**:
    ```json
    {
      "nm_cliente": "João da Silva",
      "nr_cpf": 12345678901,
      "nr_rg": 123456789,
      "dt_nascimento": "1990-05-15",
      "cd_senha": "senhaSegura123"
    }
    ```

- **PUT**: Atualização de Cliente  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/clientes/1`  
  - **Corpo**:
    ```json
    {
      "nm_cliente": "Carlos Mendes",
      "nr_cpf": 11223344556,
      "nr_rg": 223344556,
      "dt_nascimento": "1995-07-08",
      "cd_senha": "superSeguro789"
    }
    ```

### Tabela Telefone
- **POST**: Criação de Telefone  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/telefones`  
  - **Corpo**:
    ```json
    {
      "id_cliente": 1,
      "nr_telefone": 999888777,
      "nr_ddd": 11,
      "ds_telefone": "Residencial"
    }
    ```

- **PUT**: Atualização de Telefone  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/telefones/1`  
  - **Corpo**:
    ```json
    {
      "id_cliente": 1,
      "nr_telefone": 998877665,
      "nr_ddd": 21,
      "ds_telefone": "Comercial"
    }
    ```

### Tabela Produto
- **POST**: Criação de Produto  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/produtos`  
  - **Corpo**:
    ```json
    {
      "nm_produto": "Celular X",
      "ds_categoria": "Eletrônicos",
      "nr_preco": 1999.99,
      "st_produto": "D",
      "ds_produto": "Smartphone com 128GB e 6GB RAM",
      "nr_tamanho": "6.5 polegadas"
    }
    ```

- **PUT**: Atualização de Produto  
  - **Endpoint**: `http://127.0.0.1:8000/jarvis/produtos/1`  
  - **Corpo**:
    ```json
    {
      "nm_produto": "Notebook Y",
      "ds_categoria": "Eletrônicos",
      "nr_preco": 3500.00,
      "st_produto": "I",
      "ds_produto": "Notebook com 512GB SSD e 16GB RAM",
      "nr_tamanho": "14 polegadas"
    }
    ```

## Consultas
- **GET**: Listar todos os registros
  - **Clientes**: `http://127.0.0.1:8000/jarvis/clientes`
  - **Telefones**: `http://127.0.0.1:8000/jarvis/telefones`
  - **Produtos**: `http://127.0.0.1:8000/jarvis/produtos`

## Exclusões
- **DELETE**: Remover registro específico
  - **Telefone**: `http://127.0.0.1:8000/jarvis/telefones/1`
  - **Cliente**: `http://127.0.0.1:8000/jarvis/clientes/1`
  - **Produto**: `http://127.0.0.1:8000/jarvis/produtos/1`

## Estrutura de Código
- **Controller**: `controller/routers/jarvis_operacoes.py`  
  - Responsável pelos métodos GET, POST, PUT e DELETE das tabelas `Produto`, `Cliente` e `Telefone`.

- **Modelos e Conexão com o Banco**: `shared/database.py`
