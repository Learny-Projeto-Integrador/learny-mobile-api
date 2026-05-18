from bson import ObjectId

from api.services.base_service import convert_id, mongo_to_dict


class TestConvertId:
    def test_returns_objectid_when_valid(self):
        valid = "507f1f77bcf86cd799439011"
        result = convert_id(valid)
        assert isinstance(result, ObjectId)
        assert str(result) == valid

    def test_returns_none_when_invalid(self):
        assert convert_id("not-an-id") is None

    def test_returns_none_when_empty(self):
        assert convert_id("") is None


class TestMongoToDict:
    def test_converts_objectid_to_string(self):
        oid = ObjectId()
        doc = {"_id": oid, "name": "Test"}

        result = mongo_to_dict(doc)

        assert result["_id"] == str(oid)
        assert result["name"] == "Test"

    def test_converts_nested_objectid(self):
        oid = ObjectId()
        doc = {"parent": {"_id": oid}}

        result = mongo_to_dict(doc)

        assert result["parent"]["_id"] == str(oid)

    def test_converts_list_of_docs(self):
        oid1, oid2 = ObjectId(), ObjectId()
        docs = [{"_id": oid1}, {"_id": oid2}]

        result = mongo_to_dict(docs)

        assert result[0]["_id"] == str(oid1)
        assert result[1]["_id"] == str(oid2)

    def test_passes_through_scalars(self):
        assert mongo_to_dict("hello") == "hello"
        assert mongo_to_dict(42) == 42
        assert mongo_to_dict(None) is None
