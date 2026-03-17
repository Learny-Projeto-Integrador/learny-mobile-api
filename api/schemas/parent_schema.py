from marshmallow import fields, pre_load, post_load, pre_dump
from api.models.parent import Parent
from api import ma
from marshmallow.validate import Length

class ParentSchema(ma.Schema):
    _id = fields.Str()
    profilePicture = fields.Str()
    username = fields.Str(required=True, validate=Length(min=1))
    password = fields.Str(required=True, load_only=True)
    name = fields.Str(required=True, validate=Length(min=1))
    email = fields.Str(required=True, validate=Length(min=1))
    children = fields.List(fields.Str())
    selectedChild = fields.Str()

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        string_fields = ["username", "name", "email", "password"]

        for key in string_fields:
            if key in data and isinstance(data[key], str):
                data[key] = data[key].strip()

        return data
    
    @post_load
    def make_parent(self, data, **kwargs):
        return Parent(**data)