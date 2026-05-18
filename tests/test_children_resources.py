class TestChildResource:
    def test_get_requires_auth(self, client):
        resp = client.get("/child")
        assert resp.status_code == 401

    def test_get_returns_child(self, client, child_token, auth_header):
        token, child = child_token
        resp = client.get("/child", headers=auth_header(token))
        assert resp.status_code == 200
        assert resp.get_json()["username"] == child["username"]


class TestChildProgressResource:
    def test_get_progress(self, client, child_token, auth_header, db):
        token, child = child_token
        db.progress.insert_one({"child": child["_id"], "points": 99})
        resp = client.get("/child/progress", headers=auth_header(token))
        assert resp.status_code == 200

    def test_get_progress_not_found(self, client, child_token, auth_header):
        token, _ = child_token
        resp = client.get("/child/progress", headers=auth_header(token))
        assert resp.status_code == 404


class TestRankingResource:
    def test_returns_ranking(self, client, child_token, auth_header, make_child, db):
        token, child = child_token
        other = make_child(username="other", name="Outro")
        db.progress.insert_one({"child": child["_id"], "points": 10})
        db.progress.insert_one({"child": other["_id"], "points": 90})

        resp = client.get("/children/ranking", headers=auth_header(token))
        assert resp.status_code == 200
        ranking = resp.get_json()
        assert ranking[0]["points"] == 90
