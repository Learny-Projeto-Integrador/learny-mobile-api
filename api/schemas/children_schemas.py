# Importando o Marshmallow
from api import ma
# Importando Schema e Fields
from marshmallow import fields, pre_load
from marshmallow.validate import Length

class ChildrenSchema(ma.Schema):
    _id = fields.Str()
    usuario = fields.Str(required=True, validate=Length(min=1))
    senha = fields.Str(required=True, validate=Length(min=1))
    nome = fields.Str(required=True, validate=Length(min=1))
    foto = fields.Str(required=False)
    email = fields.Str(required=True, validate=Length(min=1))
    dataNasc = fields.Str(required=True, validate=Length(min=1))
    responsavel = fields.Str(required=False)

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        skip_fields = ["nome"]
        
        for key, value in data.items():
            if key in skip_fields:
                continue
            if isinstance(value, str):
                data[key] = value.strip()
        return data

class ChildrenLoginSchema(ma.Schema):
    usuario = fields.Str(required=True, validate=Length(min=1))
    senha = fields.Str(required=True, validate=Length(min=1))

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data