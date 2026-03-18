from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from api.utils.validate_data import handle_schema
from ..schemas.login_schema import LoginSchema
from ..services import login_service
from flask_jwt_extended import create_access_token

schema = LoginSchema()

class LoginResources(Resource):
    def post(self):   
        data, errors = handle_schema(schema, request.json)
        if errors:
            return {"error": errors}, 400
    
        result, status = login_service.login(data)
        if status != 200:
            return make_response(jsonify(result), status)
        
        access_token = create_access_token(
            identity=str(result["_id"]),
            additional_claims={
                "username": result["username"],
                "name": result["name"],
                "email": result["email"],
                "type": result["type"],
            }
        )

        return make_response(jsonify(
            access_token=access_token,
        ), status)
    
api.add_resource(LoginResources, '/auth/login')