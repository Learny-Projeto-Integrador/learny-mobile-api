from bson import ObjectId

def convert_id(id_str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None
    
def mongo_to_dict(doc):
    if isinstance(doc, list):
        return [mongo_to_dict(item) for item in doc]
    elif isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                new_doc[key] = str(value)
            elif isinstance(value, (dict, list)):
                new_doc[key] = mongo_to_dict(value)
            else:
                new_doc[key] = value
        return new_doc
    else:
        return doc