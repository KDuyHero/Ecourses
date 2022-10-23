from ast import Mod
from rest_framework.serializers import ModelSerializer
from .models import Course, Tag, Lesson, User

class CourseSerializer(ModelSerializer):
    class Meta: 

        model = Course
        
        fields = ['id', 'subject', 'image', 'created_date', 'category']

class TagSerializef(ModelSerializer):
    class Meta: 
        model = Tag
        fields = ['id', 'name']

class LessonSerializer(ModelSerializer):
    #custom serializer bằng cách thêm 1 serializer vào 1 trường của serializer khác
    tags = TagSerializef(many = True)
    class Meta: 
        #model cần serializer
        model = Lesson
        #các trường cần serializer
        fields = ['id', 'subject', 'content', 'created_date', 'course', 'image', 'tags']

    
class UserSerializer(ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'avatar']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user