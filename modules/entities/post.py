
class PostEntity:
    def __init__(self, id, title, user, content, created_at, updated_at):
        self.id = id
        self.user = user
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return "<PostEntity id:%s title:%s user:%s content:%s created_at:%s updated_at:%s>" % (
            self.id, self.title, self.user, self.content, self.created_at, self.updated_at)

    def __str__(self):
        return self.__repr__()
