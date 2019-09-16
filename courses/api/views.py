from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Course
from ..serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['title', 'subtitle', 'price']
