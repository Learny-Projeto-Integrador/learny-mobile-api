from unittest import result

from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from api.utils.validate_data import handle_schema
from ..schemas.parent_schema import ParentSchema
from ..schemas.children_schema import ChildrenSchema
from ..services import parent_service
from flask_jwt_extended import jwt_required, get_jwt_identity

parent_schema = ParentSchema()
children_schema = ChildrenSchema()

class ParentResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.get_parent_by_id(parent_id)
        return make_response(jsonify(result), status)

    def post(self):
        data, errors = handle_schema(parent_schema, request.json)
        if errors:
            return {"error": errors}, 400

        result, status = parent_service.register_parent(data)
        return make_response(jsonify(result), status)

    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()

        data, errors = handle_schema(parent_schema, request.json)
        if errors:
            return {"error": errors}, 400

        result, status = parent_service.edit_parent(parent_id, data)
        return make_response(jsonify(result), status)

    @jwt_required()
    def delete(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.delete_parent(parent_id)
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

        data, errors = handle_schema(children_schema, request.json)
        if errors:
            return {"error": errors}, 400
        
        result, status = parent_service.register_children(parent_id, data)
        return make_response(jsonify(result), status)
    
class ChildrenDetailResources(Resource):
    @jwt_required()
    def get(self, id):
        result, status = parent_service.get_child_by_id(id)
        return make_response(jsonify(result), status)

    @jwt_required()
    def put(self, id):
        data, errors = handle_schema(children_schema, request.json)
        if errors:
            return {"error": errors}, 400

        result, status = parent_service.edit_child(id, data)
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
        
        result, status = parent_service.edit_child_status(id, data)
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
        child_id = request.json.get("id")

        result, status = parent_service.edit_selected_children(parent_id, child_id)
        return make_response(jsonify(result), status)

api.add_resource(ParentResources, '/parents')
api.add_resource(ChildrenResources, '/parents/children')
api.add_resource(ChildrenDetailResources, '/parents/children/<string:id>')
api.add_resource(EditStatusResources, '/parents/children/<string:id>/status')
api.add_resource(SelectedChildrenResources, '/parents/selected-child')
