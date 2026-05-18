from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..services import game_service
from flask_jwt_extended import jwt_required
from ..schemas.children_schema import ChildrenSchema

schema = ChildrenSchema()

class WorldsResource(Resource):
    @jwt_required()
    def get(self):
        result, status = game_service.get_worlds()
        return make_response(jsonify(result), status)
    
class WorldInfoResource(Resource):
    @jwt_required()
    def get(self, code):
        result, status = game_service.get_world_info(code)
        return make_response(jsonify(result), status)
    
class CharactersResource(Resource):
    @jwt_required()
    def get(self):
        result, status = game_service.get_characters()
        return make_response(jsonify(result), status)
    
class CharacterInfoResource(Resource):
    @jwt_required()
    def get(self, code):
        result, status = game_service.get_character_info(code)
        return make_response(jsonify(result), status)

api.add_resource(WorldsResource, '/game/worlds')
api.add_resource(WorldInfoResource, '/game/worlds/<string:code>')
api.add_resource(CharactersResource, '/game/characters')
