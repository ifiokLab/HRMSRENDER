from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myuser
        fields = ('id', 'email', 'first_name', 'last_name',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'logo', 'overview','organization_type')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('invited_user', 'organization', 'department',)


class ClientInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInvitation
        fields = ('invited_user', 'organization','hourly_rate')

    
class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['organization','request_type','end_date','start_date','reason']





class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category','sub_category','title','thumbnail','overview','description','preview_video',]


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ['id', 'title']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['id', 'title', 'subcategories']


class InstructorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'



    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title', 'description']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'content_type', 'content_file','content']



class ContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'content_type', 'content_file','content']

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ['id', 'title', 'course']


class ObjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectives
        fields = ['id', 'title', 'course']

    
class ContentTypeCountSerializer(serializers.Serializer):
    content_type = serializers.CharField()
    count = serializers.IntegerField()


class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['organization','client','staff']



from rest_framework import serializers

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = myuser.objects.get(email=value)
        except myuser.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return value
