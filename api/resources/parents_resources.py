from bson import ObjectId
from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.parent_schemas import ParentSchema
from ..schemas.children_schemas import ChildrenSchema
from ..models import database
from ..services import parent_service
from flask_jwt_extended import jwt_required, get_jwt_identity

parent_schema = ParentSchema()
children_schema = ChildrenSchema()

class ParentResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.get_parent_by_id(ObjectId(parent_id))
        return make_response(jsonify(result), status)
    
    def post(self):
        try:
            validated_data = parent_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": f"Erro ao validar os dados recebidos, {err}."}), 400)

        result, status = parent_service.register_parent(validated_data)
        return make_response(jsonify(result), status)

    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()
        try:
            validated_data = parent_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": f"Erro ao validar os dados recebidos, {err}."}), 400)

        result, status = parent_service.edit_parent(parent_id, validated_data)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def delete(self):
        parent_id = get_jwt_identity()

        result, status = parent_service.delete_parent(ObjectId(parent_id))
        return make_response(jsonify(result), status)  
    
class ChildrenResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.get_all_children(parent_id)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def post(self):
        parent_id = get_jwt_identity()
        try:
            validated_data = children_schema.load(request.json)
        except ValidationError:
            return make_response(jsonify({"error": "Erro ao validar os dados recebidos."}), 400)

        result, status = parent_service.register_children(parent_id, validated_data)
        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)

        return make_response(jsonify(result), status)

class ChildrenDetailResources(Resource):
    @jwt_required()
    def get(self, id):
        result, status = parent_service.get_child_by_id(id)
        return make_response(jsonify(result), status)
        
    @jwt_required()
    def put(self, id):
        try:
            validated_data = children_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": f"Erro ao validar os dados recebidos. {err}"}), 400)
        
        result,status = parent_service.edit_child(id, validated_data)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def delete(self, id):
        parent_id = get_jwt_identity()
        result, status = parent_service.delete_child(id, parent_id)
        return make_response(jsonify(result), status)
    
class EditStatusResources(Resource):
    @jwt_required()
    def put(self, id):
        data = request.json
        
        result,status = parent_service.edit_child_status(id, data)
        return make_response(jsonify(result), status)

class SelectedChildrenResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()

        result, status = parent_service.get_selected_child(parent_id)
        return make_response(jsonify(result), status)
    
    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()
        new_child = request.json
        child_id = new_child["id"]

        result, status = parent_service.edit_selected_children(parent_id, child_id)
        return make_response(jsonify(result), status)

      
api.add_resource(ParentResources, '/pais')
api.add_resource(ChildrenResources, '/pais/criancas')
api.add_resource(ChildrenDetailResources, '/pais/crianca/<string:id>')
api.add_resource(EditStatusResources, '/pais/crianca/status/<string:id>')
api.add_resource(SelectedChildrenResources, '/pais/filhoSelecionado')
