from abc import ABC, abstractmethod
from typing import Any, Dict, List
from django.db import models


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, model_class: models.Model) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get(self, id: str) -> models.Model:
        raise NotImplementedError()
    
    @abstractmethod
    def all(self) -> List[models.Model]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def update_one(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError()
