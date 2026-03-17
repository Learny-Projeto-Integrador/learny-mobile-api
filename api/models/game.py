from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId
from api.models.base_model import BaseModel

@dataclass
class Progress(BaseModel):
    _id: Optional[ObjectId] = None
    child: ObjectId = None

    completedPhases: int = 0
    worlds: List[Dict] = field(default_factory=list)

@dataclass
class Medal(BaseModel):
    _id: Optional[ObjectId] = None
    child: ObjectId = None

    medalId: str = ""
    unlockedAt: datetime = None
    selected: bool = False

@dataclass
class Mission(BaseModel):
    _id: Optional[ObjectId] = None
    child: ObjectId = None

    title: str = ""
    description: str = ""
    completed: bool = False
    date: datetime = None

@dataclass
class World(BaseModel):
    _id: Optional[ObjectId] = None
    name: str = ""
    description: str = ""
    order: int = 0
    phases: List[Dict] = field(default_factory=list)

@dataclass
class MedalDefinition(BaseModel):
    _id: Optional[ObjectId] = None
    name: str = ""
    icon: str = ""
    requirement: str = ""

@dataclass
class Activity(BaseModel):
    _id: Optional[ObjectId] = None
    child: ObjectId = None

    type: str = ""  # "mission_completed", "medal_unlocked"
    data: Dict = field(default_factory=dict)

    createdAt: datetime = datetime.utcnow()