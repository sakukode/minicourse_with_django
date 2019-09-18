from django.contrib.auth.models import User
from rest_framework import serializers

from components.serializers import DynamicFieldsModelSerializer
from curriculums.models import Curriculum
from .models import Course


class AuthorField(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CurriculumsField(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ['id', 'title', 'attachment_url', 'file_type']


class CourseSerializer(DynamicFieldsModelSerializer):
    author = AuthorField(required=False, read_only=True)
    author_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    curriculums = CurriculumsField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'description', 'video_url', 'price', 'image_url', 'author', 'author_id', 'curriculums']

    def create(self, validated_data):
        course = Course(**validated_data)
        course.save()

        return course