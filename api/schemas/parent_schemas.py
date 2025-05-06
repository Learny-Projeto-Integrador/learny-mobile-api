# Importando o Marshmallow
from api import ma
# Importando Schema e Fields
from marshmallow import fields, pre_load
from marshmallow.validate import Length
from .children_schemas import ChildrenSchema

class ParentSchema(ma.Schema):
    _id = fields.Str()
    foto = fields.Str(required=False)
    usuario = fields.Str(required=True, validate=Length(min=1))
    senha = fields.Str(required=True, validate=Length(min=1))
    nome = fields.Str(required=True, validate=Length(min=1))
    email = fields.Str(required=True, validate=Length(min=1))
    dataNasc = fields.Str(required=True, validate=Length(min=1))
    filhos = fields.List(fields.Nested(ChildrenSchema), required=False)
    filhoSelecionado = fields.Dict(fields.Str(), required=False)

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        skip_fields = ["nome"]
        
        for key, value in data.items():
            if key in skip_fields:
                continue
            if isinstance(value, str):
                data[key] = value.strip()
        return data