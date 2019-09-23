from django.contrib.auth.models import User
from django.db import models


class CourseManager(models.Manager):

    def join(self, id, user):
        course = super().get_queryset().get(pk=id)

        if course:
            check = course.members.all().filter(id=user.id).first()
            if check:
                return False
            else:
                course.members.add(user)
                return True

        return course


class Course(models.Model):
    class Meta:
        db_table = "courses"
        permissions = [
            ("join", "Can add user to join the course"),
        ]

    objects = CourseManager()

    # main fields
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    video_url = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(default=0)

    # relationship fields
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="author")
    members = models.ManyToManyField(User, through="Membership")

    def __str__(self):
        return self.title


class Membership(models.Model):
    class Meta:
        db_table = "course_members"

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField()
