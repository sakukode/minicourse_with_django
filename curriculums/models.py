from django.db import models


class Curriculum(models.Model):
    class Meta:
        db_table = "curriculums"

    # main fields
    title = models.CharField(max_length=100)
    attachment_url = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50)

    # relationships fields
    course = models.ForeignKey('courses.Course', related_name='curriculums', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
