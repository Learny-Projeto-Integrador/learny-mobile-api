from dataclasses import asdict
from datetime import datetime
from bson import ObjectId

class BaseModel:
    def to_dict(self):
        data = asdict(self)

        def serialize(value):
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, list):
                return [serialize(v) for v in value]
            if isinstance(value, dict):
                return {k: serialize(v) for k, v in value.items()}
            return value

        data = {k: serialize(v) for k, v in data.items()}

        if data.get("_id") is None:
            data.pop("_id", None)

        return data