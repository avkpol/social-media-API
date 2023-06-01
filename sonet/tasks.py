from datetime import datetime
from celery import shared_task

from user.models import User
from sonet.models import Post

@shared_task
def create_post(user_id, content, media=None):
    user = User.objects.get(id=user_id)
    post = Post.objects.create(user=user, content=content, media=media)
    return post

@shared_task
def schedule_post_creation(user_id, content, media=None, scheduled_time=None):
    if scheduled_time:
        eta = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
        create_post.apply_async(args=[user_id, content, media], eta=eta)
    else:
        create_post(user_id, content, media)
