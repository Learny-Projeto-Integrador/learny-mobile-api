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
    pontos = fields.Float(required=False, validate=Length(min=1))
    medalhas = fields.List(fields.Dict(fields.Str()), required=False)
    fasesConluidas = fields.Integer(required=False, validate=Length(min=1))
    rankingAtual = fields.Integer(required=False, validate=Length(min=1))
    audio = fields.Boolean(required=False)
    missoesDiarias = fields.List(fields.Dict(fields.Str()), required=False)
    responsavel = fields.Str(required=True)

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        skip_fields = ["nome"]
        
        for key, value in data.items():
            if key in skip_fields:
                continue
            if isinstance(value, str):
                data[key] = value.strip()
        return data