
def get_posts(repo):
    posts = repo.all()
    return posts

def get_post(repo, id):
    post = repo.get(id)
    if post is None:
        raise Exception('Post not found')
    return post