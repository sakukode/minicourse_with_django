from rest_framework import serializers

from courses.models import Course
from courses.serializers import CourseSerializer
from .models import Curriculum


class CurriculumSerializer(serializers.ModelSerializer):

    course = CourseSerializer(required=False,read_only=True)
    course_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Curriculum
        fields = ['title', 'attachment_url', 'file_type', 'course', 'course_id']

    def create(self, validated_data):
        # get relate course
        course_id = validated_data.pop('course_id')
        course = Course.objects.get(pk=course_id)

        # attach course & save
        curriculum = Curriculum(**validated_data)
        curriculum.course = course
        curriculum.save()

        return curriculum



