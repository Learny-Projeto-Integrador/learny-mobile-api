from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime
from bson import ObjectId
from api.models.base_model import BaseModel

@dataclass
class Child(BaseModel):
    _id: Optional[ObjectId] = None
    username: str = ""
    name: str = ""
    password: str = ""
    birthDate: Optional[datetime] = None
    profilePicture: str = ""
    avatar: str = ""
    points: float = 0
    ranking: int = 0
    audio: bool = True
    rankingActive: bool = True
    parent: Optional[ObjectId] = None
    