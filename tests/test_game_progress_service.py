from bson import ObjectId

from api.services import game_progress_service


class TestUpdateProgress:
    def test_creates_new_world_entry_when_missing(self, db, make_child):
        """Quando o mundo ainda não existe no progresso, deve fazer push de um novo world."""
        child = make_child()
        db.progress.insert_one(
            {
                "child": child["_id"],
                "points": 0,
                "coins": 0,
                "streak": 0,
                "worlds": [],
            }
        )

        game_progress_service.update_progress(
            child["_id"],
            {
                "worldCode": "WORLD_NEW",
                "phaseCode": "P1",
                "moduleCode": "M1",
                "points": 50,
                "coins": 10,
                "percentage": 100,
                "time": "00:30",
            },
        )

        progress = db.progress.find_one({"child": child["_id"]})
        assert progress["points"] == 50
        assert progress["coins"] == 10
        worlds = progress["worlds"]
        assert len(worlds) == 1
        assert worlds[0]["worldCode"] == "WORLD_NEW"
        assert worlds[0]["completedPhases"][0]["phaseCode"] == "P1"

    def test_increments_streak_when_flag_set(self, db, make_child):
        child = make_child()
        db.progress.insert_one(
            {
                "child": child["_id"],
                "points": 0,
                "coins": 0,
                "streak": 2,
                "worlds": [],
            }
        )

        game_progress_service.update_progress(
            child["_id"],
            {
                "worldCode": "WORLD_1",
                "phaseCode": "P1",
                "moduleCode": "M1",
                "points": 10,
                "coins": 0,
                "percentage": 100,
                "time": "00:30",
            },
            increment_streak=True,
        )

        progress = db.progress.find_one({"child": child["_id"]})
        assert progress["streak"] == 3

    def test_returns_404_when_progress_missing(self):
        result, status = game_progress_service.update_progress(
            ObjectId(), {"worldCode": "WORLD_1"}
        )
        assert status == 404


class TestCreateActivity:
    def test_inserts_activity_with_timestamp(self, db, make_child):
        child = make_child()
        game_progress_service.create_activity(
            child["_id"], "phase_completed", {"phaseCode": "P1"}
        )
        activity = db.activities.find_one({"child": child["_id"]})
        assert activity is not None
        assert activity["type"] == "phase_completed"
        assert activity["data"]["phaseCode"] == "P1"
        assert "createdAt" in activity


class TestCheckMissions:
    def test_completes_matching_mission(self, db, make_child):
        child = make_child()
        db.missions.insert_one(
            {"child": child["_id"], "title": "Conclua P1", "completed": False}
        )

        result, bonus = game_progress_service.check_missions(child["_id"], "P1")

        assert bonus == 50
        assert result["mission"] == "Conclua P1"
        assert db.missions.find_one({"child": child["_id"]})["completed"] is True

    def test_returns_none_when_no_match(self, make_child):
        child = make_child()
        result, bonus = game_progress_service.check_missions(child["_id"], "P1")
        assert result is None
        assert bonus == 0
