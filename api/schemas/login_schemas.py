from api import ma
from marshmallow import fields, pre_load
from marshmallow.validate import Length

class LoginSchema(ma.Schema):
    usuario = fields.Str(required=True, validate=Length(min=1))
    senha = fields.Str(required=True, validate=Length(min=1))

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data