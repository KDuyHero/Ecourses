from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lesson', views.LessonViewset)
router.register('users', views.UserViewset)

#/courses/ - GET 
#/courses/ - POST
#/courses/{course_id}/ - GET
#/courses/{course_id}/ - PUT
#/courses/{coursse_id}/ - DELETE
urlpatterns = [
    path('', include(router.urls)),
    path('welcome/', views.welcome, name = "welcome"),



]
