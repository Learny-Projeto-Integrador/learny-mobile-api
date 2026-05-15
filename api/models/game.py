from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from api.models.base_model import BaseModel

@dataclass
class Phase(BaseModel):
    code: str
    name: str
    order: int
    type: str

@dataclass
class World(BaseModel):
    _id: Optional[ObjectId] = None
    name: str = ""
    description: str = ""
    order: int = 0
    phases: List[Phase] = field(default_factory=list)

@dataclass
class WorldProgress(BaseModel):
    worldCode: str
    percentage: float = 0.0
    completedPhases: List[str] = field(default_factory=list)
    unlocked: bool = False

@dataclass
class Character(BaseModel):
    code: str = ""
    name: str = ""
    image: str = ""
    description: str = ""
    unlockDescription: str = ""
    moduleCode: str = ""

@dataclass
class CharacterUnlocked(BaseModel):
    characterCode: ObjectId = ""
    unlockedAt: datetime = None

@dataclass
class MissionProgress(BaseModel):
    missionCode: ObjectId
    completed: bool = False
    assignedAt: datetime = None

@dataclass
class Progress(BaseModel):
    _id: Optional[ObjectId] = None
    child: ObjectId = None

    points: int = 0
    stellarPoints: int = 0
    coins: int = 0
    streak: int = 0
    selectedCharacter: ObjectId = ""
    worlds: List[WorldProgress] = field(default_factory=list)
    dailyMissions: List[MissionProgress] = field(default_factory=list)
    characters: List[CharacterUnlocked] = field(default_factory=list)