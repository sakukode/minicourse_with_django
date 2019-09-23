from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Course

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'subtitle', 'video_url' ,'description', 'price', 'author')
        widgets = {
          'subtitle':forms.Textarea
        }

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    form = CourseAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(Q(groups__name__in=["author","admin"]) | Q(is_staff = True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


