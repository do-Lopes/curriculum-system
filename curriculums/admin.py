from django.contrib import admin
from .models import PersonalData, Contact, ProfessionalExperience, Education
from utils.django_curriculums_admin import  UserDisplayMixin


@admin.register(PersonalData)
class PersonalDataAdmin(UserDisplayMixin, admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'birthday', 'cpf', 'marital_status']
    list_display_links = 'get_user_name',
    search_fields = 'get_user_name',
    list_filter = 'marital_status',
    list_per_page = 10
    ordering = '-id',

    
@admin.register(Contact)
class ContactAdmin(UserDisplayMixin, admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'phone', 'address', 'neighborhood', 'city', 'state', 'zip_code']
    list_display_links = 'get_user_name', 
    search_fields = 'get_user_name', 'city',
    list_filter = 'state',
    list_per_page = 10
    ordering = '-id',


@admin.register(ProfessionalExperience)
class ProfessionalExperienceAdmin(UserDisplayMixin, admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'position', 'company', 'start_date', 'end_date', 'current', 'description']
    list_display_links = 'get_user_name', 
    search_fields = 'get_user_name', 'position', 'company', 'description',
    list_filter = 'company', 'position', 'current',
    list_per_page = 10
    ordering = '-id',


@admin.register(Education)
class EducationAdmin(UserDisplayMixin, admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'institution', 'course', 'degree', 'start_date', 'completion_date', 'in_progress']
    list_display_links = 'get_user_name',
    search_fields = 'get_user_name', 'institution', 'course', 'degree',
    list_filter = 'institution', 'course', 'degree', 'in_progress',
    list_per_page = 10
    ordering = '-id',






