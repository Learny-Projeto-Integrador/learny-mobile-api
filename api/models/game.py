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
class MedalUnlocked(BaseModel):
    medalCode: ObjectId = ""
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
    completedPhases: int = 0
    ranking: Optional[int] = None
    selectedMedal: ObjectId = ""
    worlds: List[WorldProgress] = field(default_factory=list)
    dailyMissions: List[MissionProgress] = field(default_factory=list)
    medals: List[MedalUnlocked] = field(default_factory=list)