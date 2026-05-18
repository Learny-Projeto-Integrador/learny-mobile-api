from bson import ObjectId

from api.models.child import Child
from api.models.parent import Parent
from api.services import parent_service


class TestGetParentById:
    def test_returns_parent_when_exists(self, make_parent):
        parent = make_parent()
        result, status = parent_service.get_parent_by_id(str(parent["_id"]))
        assert status == 200
        assert result["username"] == parent["username"]

    def test_returns_400_when_invalid_id(self):
        result, status = parent_service.get_parent_by_id("not-an-id")
        assert status == 400
        assert "ID inválido" in result["error"]

    def test_returns_404_when_not_found(self):
        result, status = parent_service.get_parent_by_id(str(ObjectId()))
        assert status == 404


class TestRegisterParent:
    def test_creates_parent(self, db):
        parent = Parent(username="novo", password="123456", name="Novo", email="n@e.com")
        result, status = parent_service.register_parent(parent)
        assert status == 201
        stored = db.parents.find_one({"username": "novo"})
        assert stored is not None
        assert stored["password"] != "123456"

    def test_rejects_duplicate_username(self, db, make_parent):
        make_parent(username="papai")
        new_parent = Parent(username="papai", password="x", name="P", email="e@e.com")
        result, status = parent_service.register_parent(new_parent)
        assert status == 400
        assert "existente" in result["error"]


class TestDeleteParent:
    def test_deletes_parent(self, db, make_parent):
        parent = make_parent()
        result, status = parent_service.delete_parent(str(parent["_id"]))
        assert status == 200
        assert db.parents.find_one({"_id": parent["_id"]}) is None

    def test_invalid_id_returns_400(self):
        result, status = parent_service.delete_parent("bad")
        assert status == 400

    def test_not_found_returns_404(self):
        result, status = parent_service.delete_parent(str(ObjectId()))
        assert status == 404


class TestEditParent:
    def test_updates_parent(self, make_parent):
        parent = make_parent()
        new_data = Parent(username="updated", password="", name="Updated", email="u@e.com")
        result, status = parent_service.edit_parent(str(parent["_id"]), new_data)
        assert status == 200

    def test_invalid_id_returns_400(self):
        new_data = Parent(username="u", password="", name="n", email="e@e.com")
        result, status = parent_service.edit_parent("bad", new_data)
        assert status == 400

    def test_not_found_returns_404(self):
        new_data = Parent(username="u", password="", name="n", email="e@e.com")
        result, status = parent_service.edit_parent(str(ObjectId()), new_data)
        assert status == 404


class TestGetAllChildren:
    def test_returns_children_of_parent(self, make_parent, make_child):
        parent = make_parent()
        make_child(parent_id=parent["_id"], username="c1")
        make_child(parent_id=parent["_id"], username="c2")
        make_child(parent_id=ObjectId(), username="other")

        children, status = parent_service.get_all_children(str(parent["_id"]))

        assert status == 200
        assert len(children) == 2

    def test_invalid_id_returns_400(self):
        result, status = parent_service.get_all_children("bad")
        assert status == 400


class TestRegisterChild:
    def test_creates_child_and_initial_progress(self, db, make_parent):
        parent = make_parent()
        db.world_definitions.insert_many(
            [
                {"code": "WORLD_1", "name": "W1", "order": 1},
                {"code": "WORLD_2", "name": "W2", "order": 2},
            ]
        )
        child = Child(username="filho", password="123", name="Filho")

        result, status = parent_service.register_child(str(parent["_id"]), child)

        assert status == 201
        stored = db.children.find_one({"username": "filho"})
        assert stored is not None
        assert stored["parent"] == parent["_id"]
        progress = db.progress.find_one({"child": stored["_id"]})
        assert progress is not None
        assert len(progress["worlds"]) == 2
        assert progress["worlds"][0]["unlocked"] is True
        assert progress["worlds"][1]["unlocked"] is False

    def test_rejects_duplicate_username(self, db, make_parent, make_child):
        parent = make_parent()
        make_child(username="filho")
        child = Child(username="filho", password="x", name="F")
        result, status = parent_service.register_child(str(parent["_id"]), child)
        assert status == 400


class TestDeleteChild:
    def test_deletes_child_belonging_to_parent(self, db, make_parent, make_child):
        parent = make_parent()
        child = make_child(parent_id=parent["_id"])

        result, status = parent_service.delete_child(str(child["_id"]), str(parent["_id"]))

        assert status == 200
        assert db.children.find_one({"_id": child["_id"]}) is None

    def test_does_not_delete_child_of_other_parent(self, db, make_parent, make_child):
        parent = make_parent()
        child = make_child(parent_id=ObjectId())
        result, status = parent_service.delete_child(str(child["_id"]), str(parent["_id"]))
        assert status == 404


class TestGetSelectedChild:
    def test_returns_merged_child_and_progress(self, db, make_parent, make_child):
        parent = make_parent()
        child = make_child(parent_id=parent["_id"])
        db.parents.update_one({"_id": parent["_id"]}, {"$set": {"selectedChild": child["_id"]}})
        db.progress.insert_one({"child": child["_id"], "points": 100, "coins": 50})

        result, status = parent_service.get_selected_child(str(parent["_id"]))

        assert status == 200
        assert result["points"] == 100
        assert result["coins"] == 50
        assert result["username"] == child["username"]
        assert "_id" in result

    def test_no_selected_child_returns_404(self, make_parent):
        parent = make_parent()
        result, status = parent_service.get_selected_child(str(parent["_id"]))
        assert status == 404
