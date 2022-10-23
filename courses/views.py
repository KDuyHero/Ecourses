
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Course, Lesson, User
from .serializers import CourseSerializer, LessonSerializer, UserSerializer
# Create your views here.

class UserViewset(viewsets.ViewSet,
                generics.CreateAPIView, 
                generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve': 
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset  = Course.objects.filter(active = True)
    #KHAI BÁO CLASS SERIALIZER
    serializer_class = CourseSerializer
    #YÊU CẦU ĐĂNG NHẬP TÀI KHOẢN MỚI CÓ THỂ SỬ DỤNG
    #permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        #cho phép ai cũng có thể xem danh sách (không cần đăng nhập)
        if (self.action == 'list'): 
            return [permissions.AllowAny()]
        
        #các quyền còn lại thì phải đăng nhập (ví dụ xem detail)
        return [permissions.IsAuthenticated()]

    #list = xem danh sách khóa học
    #detail = xem chi tiết 1 khóa học
    
class LessonViewset(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonSerializer
    
    @action(methods = ['post'], detail = True, url_path="hide-lesson")
    #=> tạo ra đường dẫn /lessons/{pk}/hide_lesson
    def hide_lesson(self, request, pk):
        try: 
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExist: 
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(data = LessonSerializer(l, context = { 'request': request}).data, status = status.HTTP_200_OK)

def index(request):
    return HttpResponse('E-courses app')

def welcome(request): 
    return HttpResponse("Hello")