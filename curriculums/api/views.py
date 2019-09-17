from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Curriculum
from ..serializers import CurriculumSerializer


class CurriculumViewSet(viewsets.ModelViewSet):

    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']