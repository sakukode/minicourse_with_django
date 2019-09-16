from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Course


class AuthorField(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):
    author = AuthorField(required=False, read_only=True)
    author_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'description', 'video_url', 'price', 'image_url', 'author', 'author_id']

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        course = Course(**validated_data)

        # relate author
        author = User.objects.get(pk=author_id)

        course.author = author
        course.save()

        return course