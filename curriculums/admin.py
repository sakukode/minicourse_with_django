from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Curriculum


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_link', 'file_type', 'attachment_url')

    def course_link(self, curriculum):
        url = reverse("admin:courses_course_change", args=[curriculum.course.id])
        link = '<a href="%s">%s</a>' % (url, curriculum.course.title)
        return mark_safe(link)
    course_link.short_description = 'Course'
