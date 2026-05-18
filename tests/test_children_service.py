from bson import ObjectId

from api.services import children_service


class TestGetChildById:
    def test_returns_child(self, make_child):
        child = make_child()
        result, status = children_service.get_child_by_id(str(child["_id"]))
        assert status == 200
        assert result["username"] == child["username"]

    def test_invalid_id(self):
        result, status = children_service.get_child_by_id("bad")
        assert status == 400

    def test_not_found(self):
        result, status = children_service.get_child_by_id(str(ObjectId()))
        assert status == 404


class TestEditChild:
    def test_updates_existing_child(self, db, make_child):
        child = make_child()
        result, status = children_service.edit_child(str(child["_id"]), {"name": "Novo Nome"})
        assert status == 200
        updated = db.children.find_one({"_id": child["_id"]})
        assert updated["name"] == "Novo Nome"

    def test_returns_message_when_no_changes(self, make_child):
        child = make_child(name="Same")
        result, status = children_service.edit_child(str(child["_id"]), {"name": "Same"})
        assert status == 200
        assert "Nenhuma alteração" in result["message"]

    def test_not_found(self):
        result, status = children_service.edit_child(str(ObjectId()), {"name": "x"})
        assert status == 404


class TestEditChildProgress:
    def test_increments_points_and_coins(self, db, make_child):
        child = make_child()
        db.progress.insert_one({"child": child["_id"], "points": 10, "coins": 5})

        result, status = children_service.edit_child_progress(
            str(child["_id"]), {"points": 20, "coins": 3}
        )

        assert status == 200
        updated = db.progress.find_one({"child": child["_id"]})
        assert updated["points"] == 30
        assert updated["coins"] == 8

    def test_rejects_negative_coins_when_insufficient(self, db, make_child):
        child = make_child()
        db.progress.insert_one({"child": child["_id"], "coins": 5})

        result, status = children_service.edit_child_progress(
            str(child["_id"]), {"coins": -10}
        )

        assert status == 400
        assert "insuficientes" in result["error"]

    def test_allows_negative_coins_when_sufficient(self, db, make_child):
        child = make_child()
        db.progress.insert_one({"child": child["_id"], "coins": 20})

        result, status = children_service.edit_child_progress(
            str(child["_id"]), {"coins": -10}
        )

        assert status == 200
        updated = db.progress.find_one({"child": child["_id"]})
        assert updated["coins"] == 10

    def test_progress_not_found(self, make_child):
        child = make_child()
        result, status = children_service.edit_child_progress(
            str(child["_id"]), {"points": 1}
        )
        assert status == 404


class TestGetRanking:
    def test_returns_sorted_ranking(self, db, make_child):
        c1 = make_child(username="a", name="Alice")
        c2 = make_child(username="b", name="Bob")
        db.progress.insert_one({"child": c1["_id"], "points": 50})
        db.progress.insert_one({"child": c2["_id"], "points": 100})

        ranking = children_service.get_ranking()

        assert ranking[0]["name"] == "Bob"
        assert ranking[1]["name"] == "Alice"
        assert ranking[0]["points"] == 100

    def test_returns_error_when_empty(self):
        result = children_service.get_ranking()
        assert isinstance(result, tuple)
        assert result[1] == 404


class TestGetNotifications:
    def test_returns_notifications(self, db, make_child):
        child = make_child()
        db.notifications.insert_many(
            [
                {"child": child["_id"], "type": True, "description": "msg1"},
                {"child": child["_id"], "type": False, "description": "msg2"},
            ]
        )
        result, status = children_service.get_notifications(str(child["_id"]))
        assert status == 200
        assert isinstance(result, list)
        assert len(result) == 2
        assert {n["description"] for n in result} == {"msg1", "msg2"}

    def test_returns_404_when_no_notifications(self, make_child):
        child = make_child()
        result, status = children_service.get_notifications(str(child["_id"]))
        assert status == 404

    def test_invalid_id(self):
        result, status = children_service.get_notifications("bad")
        assert status == 400
