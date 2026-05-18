class TestWorldsResource:
    def test_requires_auth(self, client):
        resp = client.get("/game/worlds")
        assert resp.status_code == 401

    def test_returns_worlds(self, client, child_token, auth_header, db):
        token, _ = child_token
        db.world_definitions.insert_one({"code": "WORLD_1", "name": "Mundo 1"})
        resp = client.get("/game/worlds", headers=auth_header(token))
        assert resp.status_code == 200


class TestWorldInfoResource:
    def test_returns_world_info(self, client, child_token, auth_header, db):
        token, _ = child_token
        db.world_definitions.insert_one(
            {"code": "WORLD_1", "name": "Mundo 1", "order": 1}
        )
        db.module_definitions.insert_one(
            {"code": "W1_M1", "worldCode": "WORLD_1", "name": "Módulo", "order": 1}
        )

        resp = client.get("/game/worlds/WORLD_1", headers=auth_header(token))
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["code"] == "WORLD_1"
        assert "modules" in data

    def test_not_found(self, client, child_token, auth_header):
        token, _ = child_token
        resp = client.get("/game/worlds/NOPE", headers=auth_header(token))
        assert resp.status_code == 404


class TestCharactersResource:
    def test_returns_characters(self, client, child_token, auth_header, db):
        token, _ = child_token
        db.character_definitions.insert_one({"code": "ANGRY", "name": "Angryssaur"})
        resp = client.get("/game/characters", headers=auth_header(token))
        assert resp.status_code == 200
