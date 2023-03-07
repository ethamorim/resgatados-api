from ..database.db import db
import sqlalchemy as sql

class Usuario(db.Model):
    cpf = sql.Column(sql.String, primary_key=True)
    nome = sql.Column(sql.String, nullable=False)
    email = sql.Column(sql.String, nullable=False)
    descricao = sql.Column(sql.Text)
    endereco = sql.Column(sql.Text)