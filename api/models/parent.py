from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from api.models.base_model import BaseModel

@dataclass
class Parent(BaseModel):
    _id: Optional[ObjectId] = None
    profilePicture: str = ""
    username: str = ""
    name: str = ""
    password: str = ""
    email: str = ""
    selectedChild: str = ""
    birthDate: Optional[datetime] = None