from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from api.utils.validate_data import handle_schema
from ..services import children_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas.children_schema import ChildrenSchema

schema = ChildrenSchema()

class ChildResources(Resource):
    @jwt_required()
    def get(self):
        children_id = get_jwt_identity()
        result, status = children_service.get_child_by_id(children_id)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        
        data, errors = handle_schema(schema, request.json)
        if errors:
            return {"error": errors}, 400
        
        result, status = children_service.edit_child(children_id, data)
        return make_response(jsonify(result), status)
    
class ChildProgressResources(Resource):
    @jwt_required()
    def get(self):
        child_id = get_jwt_identity()

        result, status = children_service.get_child_progress(child_id)

        return make_response(jsonify(result), status)
    
class UpdateChildrenScore(Resource): 
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        data = request.json

        phase_code = data.get("phaseCode")
        world_code = data.get("worldCode")

        result, status = children_service.complete_phase(
            children_id,
            phase_code,
            world_code
        )

        return make_response(jsonify(result), status)
     
class RankingChildrenResources(Resource):
    @jwt_required()
    def get(self):
        ranking = children_service.get_ranking()
        return make_response(jsonify(ranking), 200)

api.add_resource(ChildResources, '/child')
api.add_resource(ChildProgressResources, '/child/progress')
api.add_resource(UpdateChildrenScore, '/progress/complete-phase')
api.add_resource(RankingChildrenResources, '/child/ranking')
