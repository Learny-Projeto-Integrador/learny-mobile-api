from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from api.utils.validate_data import handle_schema
from ..schemas.parent_schema import ParentSchema
from ..schemas.children_schema import ChildrenSchema
from ..services import parent_service
from flask_jwt_extended import jwt_required, get_jwt_identity

parent_schema = ParentSchema()
child_schema = ChildrenSchema()

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
    
class ParentChildResources(Resource):
    @jwt_required()
    def get(self, id):
        result, status = parent_service.get_child_by_id(id)
        return make_response(jsonify(result), status)

    @jwt_required()
    def put(self, id):
        data, errors = handle_schema(child_schema, request.json)
        if errors:
            return {"error": errors}, 400

        result, status = parent_service.edit_child(id, data)
        return make_response(jsonify(result), status)

    @jwt_required()
    def delete(self, id):
        parent_id = get_jwt_identity()
        result, status = parent_service.delete_child(id, parent_id)
        return make_response(jsonify(result), status)
    
class ParentChildrenResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.get_all_children(parent_id)
        return make_response(jsonify(result), status)

    @jwt_required()
    def post(self):
        parent_id = get_jwt_identity()

        data, errors = handle_schema(child_schema, request.json)
        if errors:
            return {"error": errors}, 400
        
        result, status = parent_service.register_children(parent_id, data)
        return make_response(jsonify(result), status)
    
class SelectedChildResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        result, status = parent_service.get_selected_child(parent_id)
        return make_response(jsonify(result), status)
    
class ParentChildActivityResources(Resource):
    @jwt_required()
    def get(self, id):

        result, status = parent_service.get_child_activity(id)

        return make_response(jsonify(result), status)
    
class ParentChildNotificationResources(Resource): 
    @jwt_required()
    def post(self, id):
        parent_id = get_jwt_identity()
        result, status = parent_service.send_notification(id, parent_id, request.json)

        return make_response(jsonify(result), status)

api.add_resource(ParentResources, '/parents')
api.add_resource(ParentChildResources, '/parents/child/<string:id>')
api.add_resource(ParentChildActivityResources, '/parents/child/<string:id>/activity')
api.add_resource(ParentChildNotificationResources, '/parents/child/<string:id>/notifications')
api.add_resource(ParentChildrenResources, '/parents/children')
api.add_resource(SelectedChildResources, '/parents/child/selected')
