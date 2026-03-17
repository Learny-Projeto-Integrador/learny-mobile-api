from marshmallow import fields, ValidationError
from bson import ObjectId
from datetime import datetime

class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("Invalid ObjectId")

class DateTimeField(fields.DateTime):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()