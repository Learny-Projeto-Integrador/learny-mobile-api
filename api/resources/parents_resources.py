# Importando a classe Resource do Flask-Restful
from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..schemas.learny_schemas import ParentSchema
from ..models import database
from ..services import parent_service

class ParentResources(Resource):
    def get(self):
        # Buscando no banco
        parent = parent_service.login_parent()
        # Validação do schema
        mv = ParentSchema(many=True)
        return make_response(mv.jsonify(parent), 200)  
        # Código de status OK
    
    def post(self):
        mv = ParentSchema()
        validate = mv.validate(request.json)
        # Tratando se a validação falhar
        if validate:
            return make_response(jsonify(validate), 400)
            # Código 400 : Bad request
        else:
            # Se validação bem-sucedida, irá cadastrar
            usuario = request.json["user"]
            senha = request.json["password"]
            # foto = request.json["foto"]
            email = request.json["email"]
            dataNasc = request.json["dataNasc"]
            
            new_parent = database.Pais(usuario=usuario, senha=senha, email=email, dataNasc=dataNasc)
            result = parent_service.register_parent(new_parent)
            res = mv.jsonify(result)
            return make_response(res, 201) # Código 201: CREATED
        
# class ParentDetail(Resource):
#     def delete(self, id):
#         parent = parent_service.get_movie_by_id(id)
#         if parent is None:
#             return make_response(jsonify("Responsável não encontrado."), 404)
#         parent_service.delete_parent(id)
#         return make_response(jsonify("Filme excluído com sucesso!"), 204) # Código 204: No content
      
api.add_resource(ParentResources, '/parents/register')
# api.add_resource(MovieDetail, '/movie/<id>')
