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
    rewardCharacterCode: str = ""

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
    effect: str = ""
    tags: List[str] = field(default_factory=list)
    description: str = ""
    unlockDescription: str = ""
    moduleCode: str = ""

@dataclass
class CharacterUnlocked(BaseModel):
    characterCode: str = ""
    level: int = 0
    characterPoints: int = 0
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
    selectedCharacter: str = ""
    worlds: List[WorldProgress] = field(default_factory=list)
    dailyMissions: List[MissionProgress] = field(default_factory=list)
    characters: List[CharacterUnlocked] = field(default_factory=list)
    
@dataclass
class Notification(BaseModel):
    child: ObjectId
    type: bool = False
    message: str=""
    createdAt: datetime = None