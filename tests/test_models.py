from datetime import datetime

from bson import ObjectId

from api.models.child import Child
from api.models.game import Phase, Progress, World, WorldProgress
from api.models.parent import Parent


class TestBaseModelSerialization:
    def test_to_dict_serializes_datetime_to_isoformat(self):
        birth = datetime(2020, 1, 1, 12, 0, 0)
        parent = Parent(username="p1", name="Pai", email="p@e.com", birthDate=birth)

        data = parent.to_dict()

        assert data["birthDate"] == birth.isoformat()

    def test_to_dict_removes_none_id(self):
        parent = Parent(username="p1", name="Pai", email="p@e.com")

        data = parent.to_dict()

        assert "_id" not in data

    def test_to_dict_keeps_object_id(self):
        oid = ObjectId()
        parent = Parent(_id=oid, username="p1", name="Pai", email="p@e.com")

        data = parent.to_dict()

        assert data["_id"] == oid

    def test_child_defaults(self):
        child = Child(username="c1", name="Filho", password="x")

        data = child.to_dict()

        assert data["audioActive"] is True
        assert data["rankingActive"] is True
        assert data["parent"] is None


class TestGameModels:
    def test_world_with_phases(self):
        phases = [Phase(code="P1", name="Fase 1", order=1, type="common")]
        world = World(name="Mundo", description="desc", order=1, phases=phases)

        data = world.to_dict()

        assert data["phases"][0]["code"] == "P1"
        assert data["phases"][0]["order"] == 1

    def test_progress_defaults_have_empty_lists(self):
        progress = Progress(child=ObjectId())

        data = progress.to_dict()

        assert data["points"] == 0
        assert data["worlds"] == []
        assert data["characters"] == []
        assert data["dailyMissions"] == []

    def test_world_progress_unlocked_flag(self):
        wp = WorldProgress(worldCode="W1", percentage=10.0, unlocked=True)

        data = wp.to_dict()

        assert data["unlocked"] is True
        assert data["percentage"] == 10.0
