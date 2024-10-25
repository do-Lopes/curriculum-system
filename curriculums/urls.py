from django.urls import path
from . import views


app_name = 'curriculums'


urlpatterns = [
    path('curriculums/', views.curriculums_home, name='curriculums_home'),
    path('curriculums/<int:id>', views.curriculum_view, name='curriculum')
]