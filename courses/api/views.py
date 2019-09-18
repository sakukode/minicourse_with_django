from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Course
from ..serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['title', 'subtitle', 'price']

    def list(self, request, **kwargs):
        queryset = Course.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = CourseSerializer(page, many=True, fields=('id','title', 'subtitle', 'price', 'video_url', 'author'))
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
