from django.contrib.auth.models import User

from django.db import models


class Course(models.Model):
    class Meta:
        db_table = "courses"

    # main fields
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    video_url = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(default=0)

    # relationship fields
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
