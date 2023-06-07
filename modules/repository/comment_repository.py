from .base_repository import BaseRepository
from typing import Any, Dict, List
from django.db import models
from modules.entities.comment import CommentEntity
from typing import Optional

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
        comment = self.model_class.objects.filter(id=id).first()
        if comment is None:
            return None
        return self._get_comment_entity(comment)
    
    def filter(self, **kwargs) -> Optional[CommentEntity]:
        comments = self.model_class.objects.filter(**kwargs)
        if len(comments) > 1:
            return self._get_multi_comment_entity(comments)
        elif len(comments) == 1:
            comment = comments[0]
            return self._get_comment_entity(comment)
        else:
            return None

    def all(self) -> List[Optional[CommentEntity]]:
        comments = self.model_class.objects.all()
        if len(comments) > 1:
            return self._get_multi_comment_entity(comments)
        elif len(comments) == 1:
            comment = comments[0]
            return self._get_comment_entity(comment)
        else:
            return None

    def create(self, data: Dict[str, Any]) -> Optional[CommentEntity]:
        model = self.model_class(**data)
        model.save()
        return self._get_comment_entity(model)

    def update_one(self, data: Dict[str, Any]) -> Optional[CommentEntity]:
        model = self.model_class(**data)
        model.save()
        return self._get_comment_entity(model)

    def delete(self, id: str) -> None:
        model = self.model_class.objects.get(id=id)
        model.delete()

    def _get_comment_entity(self, model: models.Model) -> CommentEntity:
        return CommentEntity(
            id=model.id,
            relation=getattr(model, self.relation_property),
            user=model.user,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            parent_comment=model.parent_comment)
    
    def _get_multi_comment_entity(self, models: List[models.Model]) -> List[Optional[CommentEntity]]:
        return [self._get_comment_entity(model) for model in models]