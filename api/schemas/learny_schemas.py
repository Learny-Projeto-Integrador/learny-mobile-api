# Importando o Marshmallow
from api import ma
# Importando Schema e Fields
from marshmallow import Schema, fields

class ParentSchema(ma.Schema):
    # class Meta:
    #     fields = ("_id", "title", "description", "year")
        
    # Tipando os dados
    _id = fields.Str()
    usuario = fields.Str(required=True)
    senha = fields.Str(required=True)
    foto = fields.Str(required=False)
    email = fields.Str(required=True)
    dataNasc = fields.Str(required=True)
    
class ChildrenSchema(ma.Schema):
    # class Meta:
    #     fields = ("_id", "title", "description", "year")
        
    # Tipando os dados
    _id = fields.Str()
    usuario = fields.Str(required=True)
    senha = fields.Str(required=True)
    foto = fields.Str(required=False)
    email = fields.Str(required=True)
    dataNasc = fields.Str(required=True)