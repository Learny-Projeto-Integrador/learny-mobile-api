from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..services import children_service
from flask_jwt_extended import jwt_required, get_jwt_identity

class ChildResources(Resource):
    @jwt_required()
    def get(self):
        children_id = get_jwt_identity()
        result, status = children_service.get_child_by_id(children_id)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        data = request.json
        result, status = children_service.edit_child(children_id, data)
        return make_response(jsonify(result), status)
    
class UpdateChildrenScore(Resource): 
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        new_data = request.json
        tipo_fase = new_data.get("tipoFase")

        result, status = children_service.edit_children_score(children_id, new_data, tipo_fase)
        return make_response(jsonify(result), status)
     
class RankingChildrenResources(Resource):
    @jwt_required()
    def get(self):
        ranking = children_service.get_ranking()
        return make_response(jsonify(ranking), 200)

api.add_resource(ChildResources, '/criancas')
api.add_resource(UpdateChildrenScore, '/criancas/faseconcluida')
api.add_resource(RankingChildrenResources, '/criancas/ranking')
