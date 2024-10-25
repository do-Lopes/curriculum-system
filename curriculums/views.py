from django.shortcuts import render
from django.contrib.auth.models import User
from .models import PersonalData, Contact

# Create your views here.

def curriculums_home(request):
    curriculums = PersonalData.objects.select_related('user', 'contact').prefetch_related(
    'experiences', 
    'education'
).order_by('-id')
    return render(request, 'curriculums/pages/curriculum_home.html',
    context={
        'curriculums': curriculums,
    })

def curriculum_view(request, id):
    curriculum = PersonalData.objects.select_related('user', 'contact').prefetch_related(
    'experiences', 
    'education'
    ).filter(pk=id).first()
    return render(request, 'curriculums/pages/curriculum_view.html',{
        'curriculum': curriculum,
        'detail_page': True,
    })