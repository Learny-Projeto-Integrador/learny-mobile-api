from marshmallow import ValidationError

def handle_schema(schema, data):
    try:
        return schema.load(data), None
    except ValidationError as err:
        return None, err.messages