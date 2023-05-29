import sqlalchemy as sql

from flask_restful import Resource
from flask import request
from ..database.db import db
from sqlalchemy import exc

from ..models.animal import Animal as AnimalModel
from ..models.usuario import Usuario as UsuarioModel

class Animais(Resource):
    
    def get(self):
        animais = db.session.execute(
            sql.select(AnimalModel)
        ).scalars().all()
        
        animais_json = [a.get_json() for a in animais]
        
        for animal in animais_json:
            divulgador = db.session.execute(
                sql.select(UsuarioModel).where(UsuarioModel.cpf.__eq__(animal['divulgador']))
            ).scalar()
            animal['divulgador'] = divulgador.get_json()
            
        return animais_json
    
    def post(self):
        try:
            req = request.get_json()
            print(req)
            
            novo_animal = AnimalModel(
                nome=req['nome'],
                data_nascimento=req['dataNascimento'],
                sexo=req['sexo'],
                especie=req['especie'],
                descricao=req['descricao'],
                divulgador=req['divulgador']
            )
            
            db.session.add(novo_animal)
            db.session.commit()
            
            return novo_animal.get_json()
        except KeyError as ke:
            return { "erro": f"Falta parâmetro obrigatório {str(ke)}" }, 400
        except exc.StatementError as se:
            return { "erro": str(se) }, 500