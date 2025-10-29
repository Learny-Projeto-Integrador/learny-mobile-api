from marshmallow import fields, pre_load, post_load, pre_dump, ValidationError
from api.models.database import Crianca
from bson import ObjectId
from datetime import datetime
from api import ma

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
class ChildrenSchema(ma.Schema):
    _id = ObjectIdField(dump_only=True)
    usuario = fields.Str(required=True)
    senha = fields.Str(required=True)
    nome = fields.Str(required=True)
    foto = fields.Str()
    avatar = fields.Str()
    dataNasc = fields.DateTime()
    pontos = fields.Float(load_default=0)
    fasesConcluidas = fields.Int(load_default=0)
    medalhas = fields.List(fields.Dict(), load_default=list)
    medalhaSelecionada = fields.Dict(load_default=dict)
    rankingAtual = fields.Int(load_default=0)
    missoesDiarias = fields.List(fields.Dict(), load_default=list)
    audio = fields.Bool(load_default=True)
    mundos = fields.List(fields.Dict(), load_default=list)
    responsavel = ObjectIdField()

    @pre_load
    def strip_whitespace(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

    @post_load
    def make_crianca(self, data, **kwargs):
        return Crianca(**data)

    @pre_dump
    def prepare_dump(self, obj, **kwargs):
        if obj.dataNasc and isinstance(obj.dataNasc, datetime):
            obj.dataNasc = obj.dataNasc.isoformat()
        return obj
