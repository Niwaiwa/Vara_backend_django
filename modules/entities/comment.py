
class CommentEntity:
    def __init__(self, id, profile, user, content, created_at, updated_at, parent_comment):
        self.id = id
        self.profile = profile
        self.user = user
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.parent_comment = parent_comment

    def __repr__(self):
        return "<CommentEntity id:%s profile:%s user:%s content:%s created_at:%s updated_at:%s parent_comment:%s>" % (
            self.id, self.profile, self.user, self.content, self.created_at, self.updated_at, self.parent_comment)

    def __str__(self):
        return self.__repr__()
