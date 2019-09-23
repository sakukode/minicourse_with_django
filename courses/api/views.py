from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.permissions import DjangoModelPermissions

from ..models import Course
from ..serializers import CourseSerializer
from courses.api.permissions import IsOwnerOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['id', 'title', 'subtitle', 'price']
    ordering_fields = ['id', 'title', 'subtitle', 'price']
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

        if order_field:
            field = order_field.replace("-", "")
            order_field = order_field if (field in self.ordering_fields) else self.ordering[0]
        else:
            order_field = self.ordering[0]

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

    @action(detail=True, methods=['put'])
    def join(self, request, pk=None):
        """ action to join class """
        course = self.get_object()
        user = request.user
        student = course.students.all().filter(id=user.id).first()
        serializer = self.serializer_class(course)

        if student:
            return Response({'status': False,
                            'message': 'You have joined Course, Please check your dashboard',
                            'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            course.students.add(user)
            return Response({'status': False,
                            'message': 'Success Join Course',
                            'data': serializer.data}, status=status.HTTP_200_OK)
