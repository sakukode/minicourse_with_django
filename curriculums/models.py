from django.db import models


class Curriculum(models.Model):
    class Meta:
        db_table = "curriculums"

    AUDIO = 'audio'
    TEXT = 'text'
    VIDEO = 'video'

    FILE_TYPE_CHOICES = [
        (AUDIO, 'Audio'),
        (TEXT, 'Text'),
        (VIDEO, 'Video'),
    ]

    # main fields
    title = models.CharField(max_length=100)
    attachment_url = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # relationships fields
    course = models.ForeignKey('courses.Course', related_name='curriculums', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
