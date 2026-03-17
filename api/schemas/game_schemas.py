from marshmallow import Schema, fields, post_load
from api.models.game import Activity, Medal, MedalDefinition, Mission, Progress, World
from api.schemas.base_schema import ObjectIdField, DateTimeField

class ProgressSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    child = ObjectIdField(required=True)

    completedPhases = fields.Int()
    worlds = fields.List(fields.Dict())

    @post_load
    def make_progress(self, data, **kwargs):
        return Progress(**data)
    
class MedalSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    child = ObjectIdField(required=True)

    medalId = fields.Str(required=True)
    unlockedAt = DateTimeField()
    selected = fields.Bool()

    @post_load
    def make_medal(self, data, **kwargs):
        return Medal(**data)
    
class MissionSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    child = ObjectIdField(required=True)

    title = fields.Str(required=True)
    description = fields.Str()
    completed = fields.Bool()
    date = DateTimeField()

    @post_load
    def make_mission(self, data, **kwargs):
        return Mission(**data)
    
class WorldSchema(Schema):
    _id = ObjectIdField(dump_only=True)

    name = fields.Str(required=True)
    description = fields.Str()
    order = fields.Int()
    phases = fields.List(fields.Dict())

    @post_load
    def make_world(self, data, **kwargs):
        return World(**data)
    
class MedalDefinitionSchema(Schema):
    _id = ObjectIdField(dump_only=True)

    code = fields.Str(required=True)
    name = fields.Str(required=True)
    icon = fields.Str()
    requirement = fields.Str()

    @post_load
    def make_medal_definition(self, data, **kwargs):
        return MedalDefinition(**data)
    
class ActivitySchema(Schema):
    _id = ObjectIdField(dump_only=True)
    child = ObjectIdField(required=True)

    type = fields.Str(required=True)
    data = fields.Dict()
    createdAt = DateTimeField()

    @post_load
    def make_activity(self, data, **kwargs):
        return Activity(**data)