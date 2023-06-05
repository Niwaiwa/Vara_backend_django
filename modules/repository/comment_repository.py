from .base_repository import BaseRepository
from typing import Any, Dict, List
from django.db import models
from modules.entities.comment import CommentEntity

class CommentRepository(BaseRepository):
    def __init__(self, model_class: models.Model) -> None:
        self.model_class = model_class

    def get(self, id: str) -> models.Model:
        return self.model_class.objects.get(id=id)
    
    def filter(self, **kwargs) -> models.Model:
        return self.model_class.objects.filter(**kwargs)

    def all(self) -> List[models.Model]:
        return self.model_class.objects.all()

    def create(self, data: Dict[str, Any]) -> CommentEntity:
        model = self.model_class(**data)
        model.save()
        return CommentEntity(
            id=model.id,
            profile=model.profile,
            user=model.user,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            parent_comment=model.parent_comment)

    def update(self, data: Dict[str, Any]) -> None:
        model = self.model_class(**data)
        data.pop('id')
        self.model_class.objects.bulk_update([model], data.keys())

    def delete(self, id: str) -> None:
        model = self.model_class.objects.get(id=id)
        model.delete()
