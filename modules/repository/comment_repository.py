from .base_repository import BaseRepository
from typing import Any, Dict, List
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from modules.entities.comment import CommentEntity
from typing import Optional, Union

class CommentRepository(BaseRepository):
    relation_property_map = {
        'VideoComment': 'video',
        'ImageSlideComment': 'slide',
        'PostComment': 'post',
        'ProfileComment': 'profile',
    }

    def __init__(self, model_class: models.Model) -> None:
        self.model_class = model_class
        self.relation_property = self.relation_property_map[model_class.__name__.lower()]

    def get(self, id: str) -> Optional[CommentEntity]:
        try:
            model = self.model_class.objects.filter(id=id).first()
        except ObjectDoesNotExist:
            return None

        return self._get_entity_item(model)
    
    def filter(self, order: str = 'created_at', **filter_kwargs) -> List[Optional[CommentEntity]]:
        models = self.model_class.objects.filter(**filter_kwargs).order_by(order)
        return self._get_entity_items(models)

    def all(self, order: str = 'created_at') -> List[Optional[CommentEntity]]:
        models = self.model_class.objects.all().order_by(order)
        return self._get_entity_items(models)

    def create(self, data: Dict[str, Any]) -> Optional[CommentEntity]:
        model = self.model_class.objects.create(**data)
        model.save()
        return self._get_entity_item(model)

    def update_one(self, data: Dict[str, Any]) -> Optional[CommentEntity]:
        model = self.model_class.objects.update(**data)
        model.save()
        return self._get_entity_item(model)

    def delete(self, id: str) -> None:
        model = self.model_class.objects.delete(id=id)

    def _get_entity_item(self, model: models.Model) -> CommentEntity:
        return CommentEntity(
            id=model.id,
            relation=getattr(model, self.relation_property),
            user=model.user,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            parent_comment=model.parent_comment)
    
    def _get_entity_items(self, models: List[models.Model]) -> List[Optional[CommentEntity]]:
        return [self._get_entity_item(model) for model in models]