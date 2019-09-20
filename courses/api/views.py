from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Course
from ..serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['id', 'title', 'subtitle', 'price']
    ordering_fields = ['id','title', 'subtitle', 'price']
    ordering = ['id']

    def get_displayed_fields(self, pk=None):
        fields_string = self.request.query_params.get('fields')
        if fields_string is None:
            if pk is None:
                fields = self.search_fields
            else:
                fields = None
        else:
            fields_string = fields_string[1:-1]
            fields_list = fields_string.split(',')
            fields = tuple(fields_list)

        return fields

    def get_field_order(self):
        order_field = self.request.query_params.get('ordering')
        field = order_field.replace("-", "")
        order_field = order_field if (field in self.ordering_fields) else self.ordering[0]

        return order_field

    def list(self, request, **kwargs):
        fields = self.get_displayed_fields()
        queryset = self.queryset
        order_field = self.get_field_order()

        queryset = queryset.order_by(order_field)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, fields=fields)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        fields = self.get_displayed_fields(pk=pk)
        data = self.get_object()
        serializer = self.serializer_class(data, fields=fields)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
