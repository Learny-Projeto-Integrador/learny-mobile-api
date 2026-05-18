from api.schemas.login_schema import LoginSchema
from api.utils.validate_data import handle_schema


class TestHandleSchema:
    def test_returns_data_when_valid(self):
        schema = LoginSchema()
        data, errors = handle_schema(schema, {"username": "user1", "password": "pwd"})

        assert errors is None
        assert data == {"username": "user1", "password": "pwd"}

    def test_returns_errors_when_invalid(self):
        schema = LoginSchema()
        data, errors = handle_schema(schema, {"username": "user1"})

        assert data is None
        assert "password" in errors

    def test_strips_whitespace_before_validation(self):
        schema = LoginSchema()
        data, errors = handle_schema(schema, {"username": "  user  ", "password": " pwd "})

        assert errors is None
        assert data["username"] == "user"
        assert data["password"] == "pwd"
