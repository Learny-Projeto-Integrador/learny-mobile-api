from dataclasses import dataclass, field
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
    children: List[ObjectId] = field(default_factory=list)
    selectedChild: str = ""