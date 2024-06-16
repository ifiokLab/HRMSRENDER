from django.db import models
from django.conf import settings
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
# Create your models here.


class myuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40,blank=False)
    last_name = models.CharField(max_length=40,blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False,null = True)
    is_employee = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Organization(models.Model):
    ORGANIZATION_TYPE_CHOICES = [
        ('TECH', 'Technology Company'),
        ('RECRUITMENT', 'Recruitment Agency'),
        ('HEALTH', 'Healthcare Organization'),
        ('NGO', 'Non-Governmental Organization'),
        ('CORP', 'Corporation'),
        ('EDU', 'Educational Institution'),
        ('GOV', 'Government Agency'),
        ('SMALLBIZ', 'Small Business'),
        ('STARTUP', 'Startup'),
        ('NONPROFIT', 'Non-Profit Organization'),
        ('OTHER', 'Other'),
        # Add more choices as needed
    ]

    name = models.CharField(max_length=100)
    organization_type = models.CharField(max_length=100, choices=ORGANIZATION_TYPE_CHOICES, default='CORP')
    overview = models.TextField(blank=True,null=True)
    logo = models.ImageField(upload_to='org-logo/',blank=True,null=True)
    employer =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='employees',blank=True)
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='client_organizations', blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('SALES', 'Sales'),
        ('MKT', 'Marketing'),
        ('ENG', 'Engineering'),
        ('OPS', 'Operations'),
        ('ADMIN', 'Administration'),
        ('SUPPORT', 'Customer Support'),
        ('LEGAL', 'Legal'),
        ('QA', 'Quality Assurance'),
        ('RD', 'Research and Development'),
        ('PR', 'Public Relations'),
        ('LOG', 'Logistics'),
        # Add more choices as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null= True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True,null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Profile/',blank=True,null=True)
   
    def __str__(self):
        return self.user


class Membership(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Inactive', 'Inctive'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    date_joined = models.DateTimeField(auto_now_add=True,null=True)

class Employer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null= True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True,null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Profile/',blank=True,null=True)
    # Other fields

    def __str__(self):
        return self.user

from django.utils.crypto import get_random_string
def generate_invitation_code():
    return get_random_string(12)

class Invitation(models.Model):
    
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_sent')
    invited_user = models.EmailField()
    organization =  models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    invitation_code = models.CharField(max_length=50, default=generate_invitation_code, unique=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation from {self.invited_by.email} to {self.invited_user}"



class ClientInvitation(models.Model):
    
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_invitations_sent')
    invited_user = models.EmailField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    organization =  models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    invitation_code = models.CharField(max_length=50, default=generate_invitation_code, unique=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation from {self.invited_by.email} to {self.invited_user}"



class EmployeeNotification(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Inactive', 'Inctive'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    reason = models.TextField()



"""
class TimeSheet(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    activity_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def formatted_start_date(self):
        return self.start_date.strftime('%Y-%m-%d %H:%M:%S')

    def formatted_end_date(self):
        return self.end_date.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"{self.user.first_name}'s TimeSheet - {self.start_date}"

    class Meta:
        ordering = ['-id']

"""

class Payroll(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) 
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')

    class Meta:
        ordering = ['-id']


class Invoice(models.Model):
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  

class PaymentSchedule(models.Model):
    PAYMENT_SCHEDULE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Bi-Weekly', 'Bi-Weekly'),
        ('Weekly', 'Weekly'),
    ]

    payment_schedule = models.CharField(max_length=20,choices=PAYMENT_SCHEDULE_CHOICES,default='Monthly')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization.name}"



class Request(models.Model):
    REQUEST_CHOICES = [
        ('Vacation', 'Vacation'),
        ('Sick Leave', 'Sick Leave'),
        ('Work from Home', 'Work from Home'),
        ('Business Travel', 'Business Travel'),
        ('Training', 'Training'),
        ('Maternity Leave', 'Maternity Leave'),
        ('Paternity Leave', 'Paternity Leave'),
        ('Unpaid Leave', 'Unpaid Leave'),
        ('Remote Work', 'Remote Work'),
        ('Conference Attendance', 'Conference Attendance'),
        ('Family Emergency', 'Family Emergency'),
        ('Personal Development', 'Personal Development'),
        ('Community Service', 'Community Service'),
        ('Study Leave', 'Study Leave'),
        ('Flex Time', 'Flex Time'),
        ('Sabbatical', 'Sabbatical'),
        ('Resignation', 'Resignation'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True,blank=True)
    request_type = models.CharField(max_length=100, choices=REQUEST_CHOICES, default='Vacation')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # You can define your own status choices if needed

    def __str__(self):
        return f"{self.user.first_name}'s Request - {self.request_type} - {self.start_date} to {self.end_date}"






class Categories(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.title


class Course(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to ='thumbnail')
    preview_video = models.FileField(upload_to='course-preview-video/', null=True, blank=True)
    overview = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True,null=True)
    #price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this line for the price field

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title



class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    biography = models.TextField()
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    picture = models.ImageField(upload_to ='profile/')

    def __str__(self):
        return f'{self.title}'



class Section(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Content(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        # Add more content types as needed
    ]

    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_file = models.FileField(upload_to='content_files/', null=True, blank=True)
    content = models.TextField(null=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.title} - {self.content_type} - {self.section.title}"





class Requirements(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='requirements')

    def __str__(self):
        return f"{self.title} - {self.course.title}"



class Objectives(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='objectives')

    def __str__(self):
        return f"{self.title} - {self.course.title}"




class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    enrolled_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrollments', blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)



class Client(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.organization.name}'s clients"


class Assignment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assignments')

    def __str__(self):
        return f"Assignments for {self.client}"

from datetime import datetime
class TimeSheet(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Processed', 'Processed'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True)  # Assuming you have a Client model
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    hours_worked_sat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_sun = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_mon = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_tue = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_wed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_thur = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hours_worked_fri = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    allowance_sat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_sun = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_mon = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_tue = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_wed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_thur = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    allowance_fri = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    activity_description_sat = models.TextField(null=True, blank=True)
    activity_description_sun = models.TextField(null=True, blank=True)
    activity_description_mon = models.TextField(null=True, blank=True)
    activity_description_tue = models.TextField(null=True, blank=True)
    activity_description_wed = models.TextField(null=True, blank=True)
    activity_description_thur = models.TextField(null=True, blank=True)
    activity_description_fri = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    client_approved = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    organization_approved = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    final_approval = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate total hours before saving
        total_hours = sum([getattr(self, f'hours_worked_{day.lower()}') or 0 for day in ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri']])
        self.total_hours = total_hours
        super().save(*args, **kwargs)
    
    def formatted_start_date(self):
        return self.start_date.strftime('%Y-%m-%d %H:%M:%S')

    def formatted_end_date(self):
        return self.end_date.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"{self.user.first_name}'s TimeSheet - {self.start_date}"

    class Meta:
        ordering = ['-id']





class ClientProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null= True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True,null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Profile/',blank=True,null=True)
   
    def __str__(self):
        return f"{self.user.first_name}"



class OrganizationRate(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    #clients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.organization.name}'s clients"