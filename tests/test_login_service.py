from api.services import login_service


class TestLogin:
    def test_login_parent_success(self, make_parent):
        make_parent(username="papai", email="p@e.com")

        result, status = login_service.login({"username": "papai", "password": "password123"})

        assert status == 200
        assert result["type"] == "parent"
        assert result["username"] == "papai"

    def test_login_child_success(self, make_child):
        make_child(username="kid")

        result, status = login_service.login({"username": "kid", "password": "kidpass"})

        assert status == 200
        assert result["type"] == "child"

    def test_login_wrong_password(self, make_parent):
        make_parent(username="papai")

        result, status = login_service.login({"username": "papai", "password": "wrong"})

        assert status == 400
        assert "Senha" in result["error"]

    def test_login_user_not_found(self):
        result, status = login_service.login({"username": "ghost", "password": "x"})

        assert status == 400
        assert "inválidos" in result["error"]
