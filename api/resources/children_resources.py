# Importando a classe Resource do Flask-Restful
from bson import ObjectId
from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.children_schemas import ChildrenSchema
from ..models import database
from ..services import children_service
from flask_jwt_extended import jwt_required, get_jwt_identity

class ChildrenResources(Resource):
    @jwt_required()
    def get(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        return make_response(jsonify(children), 200)
    
    def post(self):
        mv = ChildrenSchema()

        try:
            validated_data = mv.load(request.json)
        except ValidationError:
            # Se der erro de validação, responde mensagem única
            return make_response(jsonify({"error": "Preencha todos os campos obrigatórios."}), 400)

        # Se passou na validação:
        foto = validated_data["foto"]
        usuario = validated_data["usuario"]
        senha = validated_data["senha"]
        nome = validated_data["nome"]
        email = validated_data["email"]
        dataNasc = validated_data["dataNasc"]
        responsavel = validated_data["responsavel"]

        new_children = database.Criancas(foto=foto, 
                                         avatar="",
                                         usuario=usuario, 
                                         senha=senha, 
                                         nome=nome, 
                                         email=email, 
                                         dataNasc=dataNasc,
                                         pontos=0, 
                                         fasesConcluidas=0,
                                         medalhas=[{}],
                                         medalhaSelecionada={},
                                         rankingAtual=0,
                                         missoesDiarias=[{}],
                                         audio=True,
                                         mundos=[{}],
                                         responsavel=responsavel)
        result = children_service.register_children(new_children)

        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)

        return make_response(jsonify(result), 201)
        
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        new_data = request.json
        if children is None:
            return make_response(jsonify("Crianca não encontrada."), 404)
        result = children_service.edit_children(children_id, new_data)
        return make_response(jsonify(result), 200)
    
class GetByUserResources(Resource):
    @jwt_required()
    def get(self):
        new_data = request.json
        children = children_service.get_children_by_user(ObjectId(new_data))
        return make_response(jsonify(children), 200)
    
class ChildrenDetail(Resource):
    @jwt_required()
    def delete(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        if children is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        
        children_service.delete_children(id)
        return make_response(jsonify("Conta excluída com sucesso"), 204)
    
class UpdateChildrenScore(Resource): 
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        new_data = request.json
        tipo_fase = new_data.get("tipoFase")  # Tipo da fase enviado pelo front

        if children is None:
            return make_response(jsonify("Crianca não encontrada."), 404)

        result = children_service.edit_children_score(children_id, new_data, tipo_fase)
        return make_response(jsonify(result), 200)
     
class RankingChildrenResources(Resource):
    @jwt_required()
    def get(self):
        ranking = children_service.get_ranking()
        return make_response(jsonify(ranking), 200)

api.add_resource(ChildrenResources, '/criancas')
api.add_resource(ChildrenDetail, '/criancas/<id>')
api.add_resource(GetByUserResources, '/criancas/<user>')
api.add_resource(UpdateChildrenScore, '/criancas/faseconcluida')
api.add_resource(RankingChildrenResources, '/criancas/ranking')
