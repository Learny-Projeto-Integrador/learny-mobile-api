# api/resources/button_resource.py
from flask_restful import Resource
from flask import jsonify
from ..serial_controller import get_last_button
from api import api

class ButtonResource(Resource):
    def get(self):
        btn = get_last_button()
        return jsonify({'button': btn})
    
api.add_resource(ButtonResource, '/button')