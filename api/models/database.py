from dataclasses import asdict, dataclass, field
from typing import Any, List, Dict, Optional
from datetime import datetime
from bson import ObjectId

@dataclass
class Pai:
    _id: Optional[ObjectId] = None
    foto: str = ""
    usuario: str = ""
    nome: str = ""
    senha: str = ""
    email: str = ""
    dataNasc: datetime = None
    filhos: List[ObjectId] = field(default_factory=list)
    filhoSelecionado: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Converte a dataclass para dict serializável (pronto para o MongoDB ou JSON)."""
        data = asdict(self)

        # Converte ObjectId e datetime automaticamente
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = value
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, list):
                # Trata listas de dicionários (recursivamente)
                data[key] = [
                    {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in i.items()}
                    if isinstance(i, dict) else i
                    for i in value
                ]
            elif isinstance(value, dict):
                # Trata dicionários internos
                data[key] = {
                    k: (v.isoformat() if isinstance(v, datetime) else v)
                    for k, v in value.items()
                }

        if data.get("_id") is None:
            data.pop("_id", None)

        if not data.get("senha"):
            data.pop("senha", None)

        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Crianca":
        """Cria uma instância da dataclass a partir de um dicionário (por exemplo, vindo do MongoDB)."""
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        if "responsavel" in data and isinstance(data["responsavel"], str):
            data["responsavel"] = ObjectId(data["responsavel"])
        if "dataNasc" in data and isinstance(data["dataNasc"], str):
            data["dataNasc"] = datetime.fromisoformat(data["dataNasc"])
        return Crianca(**data)
        
@dataclass
class Crianca:
    _id: Optional[ObjectId] = None
    foto: str = ""
    avatar: str = ""
    usuario: str = ""
    nome: str = ""
    senha: str = ""
    dataNasc: Optional[datetime] = None
    pontos: float = 0
    fasesConcluidas: int = 0
    medalhas: List[Dict] = field(default_factory=list)
    medalhaSelecionada: Dict = field(default_factory=dict)
    rankingAtual: int = 0
    missoesDiarias: List[Dict] = field(default_factory=list)
    audio: bool = True
    ranking: bool = True
    mundos: List[Dict] = field(default_factory=list)
    responsavel: Optional[ObjectId] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a dataclass para dict serializável (pronto para o MongoDB ou JSON)."""
        data = asdict(self)

        # Converte ObjectId e datetime automaticamente
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = value
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, list):
                # Trata listas de dicionários (recursivamente)
                data[key] = [
                    {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in i.items()}
                    if isinstance(i, dict) else i
                    for i in value
                ]
            elif isinstance(value, dict):
                # Trata dicionários internos
                data[key] = {
                    k: (v.isoformat() if isinstance(v, datetime) else v)
                    for k, v in value.items()
                }

        if data.get("_id") is None:
            data.pop("_id", None)

        if not data.get("senha"):
            data.pop("senha", None)

        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Crianca":
        """Cria uma instância da dataclass a partir de um dicionário (por exemplo, vindo do MongoDB)."""
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        if "responsavel" in data and isinstance(data["responsavel"], str):
            data["responsavel"] = ObjectId(data["responsavel"])
        if "dataNasc" in data and isinstance(data["dataNasc"], str):
            data["dataNasc"] = datetime.fromisoformat(data["dataNasc"])
        return Crianca(**data)
    