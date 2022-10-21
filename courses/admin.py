from importlib.resources import path
from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import Category, Course, Lesson, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditorUploadingWidget)
    class Meta: 
        model: Lesson
        fields: '__all__'
    

class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through
# class TagAdmin(admin.ModelAdmin):
#     inlines = (LessonTagInline,)
class LessonAdmin(admin.ModelAdmin):
    class Media: 
        css = {
            'all': ('/static/css/main.css',)
        }
        js = ('/static/js/index.js',)
    form = LessonForm
    list_display = ['id', 'subject', 'created_date', 'active','course']
    search_fields = ['subject', 'created_date', 'course__subject']
    list_filter = ['subject', 'course__subject']
    readonly_fields = ['avatar']
    def avatar(self, lesson):
        return mark_safe(
            '<img src="/static/{img_url}" alt ="{alt}" width = "120px" />'
            .format(img_url = lesson.image.name, alt = lesson.subject)
        )
    inlines = (LessonTagInline,)

class LessonInline(admin.StackedInline):
    model = Lesson
    fk_name = 'course'

class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline,)
class CourseAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống quản trị khóa học"

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()
    def course_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects\
            .annotate(lesson_count = Count('lessons'))\
            .values('id', 'subject', 'lesson_count')
        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count, 
            'course_stats': stats
        })

admin_site = CourseAppAdminSite(name= "Khóa học")

# Register your models here.
admin_site.register(Category), 
admin_site.register(Course, CourseAdmin),
admin_site.register(Lesson, LessonAdmin), 
