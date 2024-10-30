import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, BigInteger, CheckConstraint, DECIMAL
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session  
from fastapi import FastAPI, Depends

DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://azureadmin:rootpwSprint4@jarvisSprint4Server.database.windows.net/jarvisSprint4Banco?driver=ODBC+Driver+17+for+SQL+Server")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  

class Produto(Base):
    __tablename__ = 't_pl_produto'

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nm_produto = Column(String(150), nullable=False)
    ds_categoria = Column(String(150), nullable=False)
    nr_preco = Column(DECIMAL(25, 2), nullable=False)
    st_produto = Column(String(1), nullable=False)
    ds_produto = Column(String(250), nullable=False)
    nr_tamanho = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint("st_produto IN ('D', 'I')", name='check_st_produto'),
    )

class Cliente(Base):
    __tablename__ = 't_pl_cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nm_cliente = Column(String(50), nullable=False)
    nr_cpf = Column(BigInteger, nullable=False)
    nr_rg = Column(Integer, nullable=False)
    dt_nascimento = Column(Date, nullable=False)
    cd_senha = Column(String(150), nullable=False)

    __table_args__ = (
        CheckConstraint('nr_cpf >= 10000000000 AND nr_cpf <= 99999999999', name='chk_nr_cpf'),
        CheckConstraint('nr_rg >= 100000000 AND nr_rg <= 999999999', name='chk_nr_rg'),
    )

    telefones = relationship('Telefone', back_populates='cliente')
    produtos = relationship('ClienteProduto', back_populates='cliente')

class Telefone(Base):
    __tablename__ = 't_pl_telefone'

    id_telefone = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('t_pl_cliente.id_cliente'), nullable=False)
    nr_telefone = Column(BigInteger, nullable=False)
    nr_ddd = Column(Integer, nullable=False)
    ds_telefone = Column(String(50), nullable=False)

    cliente = relationship('Cliente', back_populates='telefones')

class ClienteProduto(Base):
    __tablename__ = 't_pl_cliente_produto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('t_pl_cliente.id_cliente'))
    id_produto = Column(Integer, ForeignKey('t_pl_produto.id_produto'))

    cliente = relationship('Cliente', back_populates='produtos')
    produto = relationship('Produto', back_populates='clientes')

Produto.clientes = relationship('ClienteProduto', back_populates='produto')

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
