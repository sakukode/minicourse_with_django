from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Course
from ..serializers import CourseSerializer
from courses.api.permissions import CoursePermission

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [CoursePermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['id', 'title', 'subtitle', 'price']
    ordering_fields = ['id', 'title', 'subtitle', 'price']
    ordering = ['id']

    # def get_queryset(self):
    #     """
    #     This view should return a list of all
    #     for the currently authenticated user.
    #     """
    #     page = self.request.query_params.get('page')
    #
    #     if page:
    #         if page == 'my_course':
    #             user = self.request.user
    #             return Course.objects.filter(author=user)
    #         elif page == 'my_class':
    #             user = self.request.user
    #             return Course.objects.filter(members__id = user.id)
    #
    #     return super().queryset

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None, *args, **kwargs):
        """ action to join class """
        course = self.get_object()
        user = request.user
        serializer = self.serializer_class(course)
        res = Course.objects.join(course.id, user)

        if res:
            return Response({'status': True,
                             'message': 'Success Join Course',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,
                             'message': 'You have joined Course, Please check your dashboard',
                             'data': serializer.data},
                            status=status.HTTP_200_OK)

    @action(detail=False)
    def me(self, request, **kwargs):
        fields = self.get_displayed_fields()
        queryset = super().get_queryset().filter(author=request.user)
        order_field = self.get_field_order()

        queryset = queryset.order_by(order_field)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, fields=fields)

        return self.get_paginated_response(serializer.data)

    @action(detail=False)
    def my_class(self, request, **kwargs):
        fields = self.get_displayed_fields()
        user = request.user
        queryset = super().get_queryset().filter(members__id=user.id)
        order_field = self.get_field_order()

        queryset = queryset.order_by(order_field)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, fields=fields)

        return self.get_paginated_response(serializer.data)

