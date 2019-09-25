import django_filters
from django.db.models import Value
from django.db.models.functions import Concat

from courses.models import Course


class CourseFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(method='author_name_filter', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['title', 'author', 'price__gte', 'price__lte']


    def author_name_filter(self, queryset, name, value):
        queryset = Course.objects.annotate(fullname=Concat('author__first_name', Value(' '), 'author__last_name'))
        return queryset.filter(fullname__icontains=value)