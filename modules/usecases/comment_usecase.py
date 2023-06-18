from modules.exceptions import QueryObjectDoesNotExist

def get_comments(repo):
    comments = repo.all()
    return comments

def get_comments_by_post_id_and_parent_comment_id(post_repo, comment_repo, post_id, parent_comment_id):
    post = post_repo.get(post_id)
    if post is None:
        raise QueryObjectDoesNotExist('Post not found')

    if parent_comment_id is None:
        comments = comment_repo.filter(post=post)
    else:
        parent_comment = comment_repo.get(parent_comment_id)
        if parent_comment is None:
            raise QueryObjectDoesNotExist('Parent comment not found')
        
        comments = comment_repo.filter(post=post, parent_comment=parent_comment_id)
    return comments