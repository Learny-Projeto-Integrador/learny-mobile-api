from marshmallow import fields, pre_load, post_load, pre_dump, ValidationError
from api.models.database import Crianca, Pai
from bson import ObjectId
from datetime import datetime
from api import ma
from marshmallow.validate import Length

# Campo customizado para ObjectId
class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value) if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("ObjectId inválido.")

# Schema manual (em vez de class_schema pra controle fino)
class ParentSchema(ma.Schema):
    _id = fields.Str()
    foto = fields.Str()
    usuario = fields.Str(required=True, validate=Length(min=1))
    senha = fields.Str(required=True)
    nome = fields.Str(required=True, validate=Length(min=1))
    email = fields.Str(required=True, validate=Length(min=1))
    dataNasc = fields.DateTime()
    filhos = fields.List(fields.Str())
    filhoSelecionado = fields.Str()

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

    @post_load
    def make_parent(self, data, **kwargs):
        return Pai(**data)

    @pre_dump
    def prepare_dump(self, obj, **kwargs):
        if obj.dataNasc and isinstance(obj.dataNasc, datetime):
            obj.dataNasc = obj.dataNasc.isoformat()
        return obj