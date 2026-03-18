from marshmallow import fields, pre_load, post_load
from api.models.child import Child
from api import ma
from api.schemas.base_schema import ObjectIdField

class ChildrenSchema(ma.Schema):
    _id = ObjectIdField(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    name = fields.Str(required=True)
    profilePicture = fields.Str(allow_none=True)
    avatar = fields.Str()
    birthDate = fields.DateTime(allow_none=True)
    points = fields.Float(load_default=0)
    ranking = fields.Int(load_default=0)
    audio = fields.Bool(load_default=True)
    rankingActive = fields.Bool(load_default=True)
    parent = ObjectIdField(allow_none=True)

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        string_fields = ["username", "name", "email", "password"]

        for key in string_fields:
            if key in data and isinstance(data[key], str):
                data[key] = data[key].strip()

        return data

    @post_load
    def make_Child(self, data, **kwargs):
        return Child(**data)
