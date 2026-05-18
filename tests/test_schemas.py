import pytest
from marshmallow import ValidationError

from api.models.child import Child
from api.models.parent import Parent
from api.schemas.children_schema import ChildrenPhaseSchema, ChildrenSchema
from api.schemas.login_schema import LoginSchema
from api.schemas.parent_schema import ParentSchema


class TestParentSchema:
    def test_valid_payload_returns_parent_instance(self):
        schema = ParentSchema()
        payload = {
            "username": "papai",
            "password": "secret",
            "name": "Pai Teste",
            "email": "papai@ex.com",
        }
        result = schema.load(payload)
        assert isinstance(result, Parent)
        assert result.username == "papai"

    def test_missing_required_fields_raises(self):
        schema = ParentSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load({"username": "u"})
        assert "password" in exc.value.messages
        assert "name" in exc.value.messages
        assert "email" in exc.value.messages

    def test_strips_whitespace(self):
        schema = ParentSchema()
        result = schema.load(
            {
                "username": "  papai  ",
                "password": " secret ",
                "name": " Pai ",
                "email": " papai@ex.com ",
            }
        )
        assert result.username == "papai"
        assert result.name == "Pai"

    def test_password_is_load_only(self):
        schema = ParentSchema()
        parent = Parent(username="u", password="secret", name="n", email="e@e.com")
        dumped = schema.dump(parent)
        assert "password" not in dumped


class TestChildrenSchema:
    def test_valid_payload(self):
        schema = ChildrenSchema()
        result = schema.load(
            {"username": "kid", "password": "p", "name": "Filho"}
        )
        assert isinstance(result, Child)
        assert result.audioActive is True
        assert result.rankingActive is True

    def test_missing_username_fails(self):
        schema = ChildrenSchema()
        with pytest.raises(ValidationError):
            schema.load({"password": "p", "name": "Filho"})


class TestChildrenPhaseSchema:
    def test_requires_phase_fields(self):
        schema = ChildrenPhaseSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load({})
        for field in ("points", "coins", "percentage", "time", "worldCode", "moduleCode", "phaseCode"):
            assert field in exc.value.messages

    def test_valid_phase_payload(self):
        schema = ChildrenPhaseSchema()
        data = schema.load(
            {
                "points": 10.0,
                "coins": 5,
                "percentage": 75,
                "time": "00:30",
                "worldCode": "WORLD_1",
                "moduleCode": "W1_MODULE_1",
                "phaseCode": "W1_M1_PHASE_1",
            }
        )
        assert data["points"] == 10.0
        assert data["phaseCode"] == "W1_M1_PHASE_1"


class TestLoginSchema:
    def test_valid_login(self):
        schema = LoginSchema()
        data = schema.load({"username": "u", "password": "p"})
        assert data == {"username": "u", "password": "p"}

    def test_empty_username_fails(self):
        schema = LoginSchema()
        with pytest.raises(ValidationError):
            schema.load({"username": "", "password": "p"})
