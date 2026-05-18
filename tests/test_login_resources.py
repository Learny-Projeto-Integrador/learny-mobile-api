class TestLoginEndpoint:
    def test_login_parent_returns_token(self, client, make_parent):
        make_parent(username="papai")
        resp = client.post("/auth/login", json={"username": "papai", "password": "password123"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "access_token" in data

    def test_login_invalid_credentials(self, client, make_parent):
        make_parent(username="papai")
        resp = client.post("/auth/login", json={"username": "papai", "password": "wrong"})
        assert resp.status_code == 400

    def test_login_missing_password_validation(self, client):
        resp = client.post("/auth/login", json={"username": "u"})
        assert resp.status_code == 400
        body = resp.get_json()
        assert "error" in body

    def test_login_user_not_found(self, client):
        resp = client.post("/auth/login", json={"username": "ghost", "password": "x"})
        assert resp.status_code == 400
