from celery import shared_task
from random import choice

from user.models import User
from sonet.models import Post


def create_post(user_id, content, media=None):
    user = User.objects.get(id=user_id).random()
    post = Post.objects.create(user=user, content=content, media=media).random
    return post


@shared_task
def create_random_post():
    user_ids = User.objects.values_list("id", flat=True)
    user_id = choice(user_ids)
    content = "Your random content here"
    media = None
    post = create_post(user_id, content, media)
    return post
