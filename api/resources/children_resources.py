# Importando a classe Resource do Flask-Restful
from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..schemas.learny_schemas import ChildrenSchema
from ..models import database
from ..services import children_service

class ChildrenResources(Resource):
    def get(self):
        # Buscando no banco
        children = children_service.login_children()
        # Validação do schema
        mv = ChildrenSchema(many=True)
        return make_response(mv.jsonify(children), 200)  
        # Código de status OK
    
    def post(self):
        mv = ChildrenSchema()
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
            
            new_children = database.Criancas(usuario=usuario, senha=senha, email=email, dataNasc=dataNasc)
            result = children_service.register_chilhen(new_children)
            res = mv.jsonify(result)
            return make_response(res, 201) # Código 201: CREATED
        
# class childrenDetail(Resource):
#     def delete(self, id):
#         children = children_service.get_movie_by_id(id)
#         if children is None:
#             return make_response(jsonify("Responsável não encontrado."), 404)
#         children_service.delete_children(id)
#         return make_response(jsonify("Filme excluído com sucesso!"), 204) # Código 204: No content
      
api.add_resource(ChildrenResources, '/childrens/register')
# api.add_resource(MovieDetail, '/movie/<id>')
