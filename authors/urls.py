from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/curriculum/delete/', views.dashboard_curriculum_delete, name='dashboard_curriculum_delete'),
    path('dashboard/curriculum/publish/<int:id>', views.dashboard_curriculum_publish, name='dashboard_curriculum_publish'),
    path('dashboard/curriculum/new/<str:form_type>', views.dashboard_curriculum_new, name='dashboard_curriculum_new'),
    path('dashboard/curriculum/edit/<int:id>/<str:form_type>', views.dashboard_curriculum_edit, name='dashboard_curriculum_edit'),
]