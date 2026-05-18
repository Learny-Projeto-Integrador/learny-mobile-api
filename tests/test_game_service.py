from api.services import game_service


class TestGetWorlds:
    def test_returns_worlds_from_db(self, db):
        db.world_definitions.insert_many(
            [
                {"code": "WORLD_1", "name": "Mundo 1"},
                {"code": "WORLD_2", "name": "Mundo 2"},
            ]
        )
        worlds, status = game_service.get_worlds()
        assert status == 200
        codes = {w["code"] for w in worlds}
        assert codes == {"WORLD_1", "WORLD_2"}


class TestGetWorldInfo:
    def test_returns_world_with_modules_and_phases(self, db):
        db.world_definitions.insert_one(
            {"code": "WORLD_1", "name": "Mundo 1", "order": 1}
        )
        db.module_definitions.insert_one(
            {"code": "W1_M1", "worldCode": "WORLD_1", "name": "Módulo", "order": 1}
        )
        db.phase_definitions.insert_one(
            {"code": "P1", "moduleCode": "W1_M1", "name": "Fase 1", "order": 1, "type": "common"}
        )

        world, status = game_service.get_world_info("WORLD_1")

        assert status == 200
        assert world["code"] == "WORLD_1"
        assert len(world["modules"]) == 1
        assert world["modules"][0]["phases"][0]["code"] == "P1"

    def test_not_found(self):
        result, status = game_service.get_world_info("NOPE")
        assert status == 404


class TestGetCharacters:
    def test_returns_characters(self, db):
        db.character_definitions.insert_many(
            [{"code": "A", "name": "A"}, {"code": "B", "name": "B"}]
        )
        characters, status = game_service.get_characters()
        assert status == 200
        assert len(list(characters)) == 2


class TestGetCharacterInfo:
    def test_returns_character(self, db):
        db.character_definitions.insert_one(
            {"code": "ANGRY", "name": "Angryssaur", "effect": "2x"}
        )
        char, status = game_service.get_character_info("ANGRY")
        assert status == 200
        assert char["name"] == "Angryssaur"

    def test_not_found(self):
        result, status = game_service.get_character_info("NOPE")
        assert status == 404
