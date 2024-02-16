from django.db import models
from common.models import CommonModel

class Review(CommonModel):
    content = models.TextField()
    likes_num = models.PositiveIntegerField()

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    feed = models.ForeignKey("feeds.Feed", on_delete=models.CASCADE)