from .base_repository import BaseRepository
from typing import Any, Dict, List
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from modules.entities.post import PostEntity
from typing import Optional, Union

class PostRepository(BaseRepository):

    def __init__(self, model_class: models.Model) -> None:
        self.model_class = model_class

    def get(self, id: str) -> Optional[PostEntity]:
        try:
            post = self.model_class.objects.filter(id=id).first()
        except ObjectDoesNotExist:
            return None

        return self._get_entity_item(post)
    
    def filter(self, order: str = '-created_at', **filter_kwargs) -> List[Optional[PostEntity]]:
        posts = self.model_class.objects.filter(**filter_kwargs).order_by(order)
        return self._get_entity_items(posts)

    def all(self, order: str = '-created_at') -> List[Optional[PostEntity]]:
        posts = self.model_class.objects.all().order_by(order)
        return self._get_entity_items(posts)

    def create(self, data: Dict[str, Any]) -> Optional[PostEntity]:
        model = self.model_class.objects.create(**data)
        model.save()
        return self._get_entity_item(model)

    def update_one(self, data: Dict[str, Any]) -> Optional[PostEntity]:
        model = self.model_class.objects.update(**data)
        model.save()
        return self._get_entity_item(model)

    def delete(self, id: str) -> None:
        model = self.model_class.objects.delete(id=id)

    def _get_entity_item(self, model: models.Model) -> PostEntity:
        return PostEntity(
            id=model.id,
            title=model.title,
            user=model.user,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at)
    
    def _get_entity_items(self, models: List[models.Model]) -> List[Optional[PostEntity]]:
        return [self._get_entity_item(model) for model in models]