class TestParentResource:
    def test_get_requires_auth(self, client):
        resp = client.get("/parents")
        assert resp.status_code == 401

    def test_get_returns_parent(self, client, parent_token, auth_header):
        token, parent = parent_token
        resp = client.get("/parents", headers=auth_header(token))
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["username"] == parent["username"]

    def test_post_creates_parent(self, client, db):
        resp = client.post(
            "/parents",
            json={
                "username": "novopai",
                "password": "abc12345",
                "name": "Novo Pai",
                "email": "novopai@ex.com",
            },
        )
        assert resp.status_code == 201
        assert db.parents.find_one({"username": "novopai"}) is not None

    def test_post_validation_error(self, client):
        resp = client.post("/parents", json={"username": ""})
        assert resp.status_code == 400

    def test_delete_removes_parent(self, client, parent_token, auth_header, db):
        token, parent = parent_token
        resp = client.delete("/parents", headers=auth_header(token))
        assert resp.status_code == 200
        assert db.parents.find_one({"_id": parent["_id"]}) is None


class TestParentChildrenResource:
    def test_list_children(self, client, parent_token, auth_header, make_child):
        token, parent = parent_token
        make_child(parent_id=parent["_id"], username="c1")
        make_child(parent_id=parent["_id"], username="c2")
        resp = client.get("/parents/children", headers=auth_header(token))
        assert resp.status_code == 200
        assert len(resp.get_json()) == 2

    def test_create_child(self, client, parent_token, auth_header, db):
        token, parent = parent_token
        db.world_definitions.insert_one({"code": "WORLD_1", "name": "W1", "order": 1})
        resp = client.post(
            "/parents/children",
            headers=auth_header(token),
            json={"username": "novofilho", "password": "p", "name": "Novo"},
        )
        assert resp.status_code == 201
        assert db.children.find_one({"username": "novofilho"}) is not None
