from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ContactForm, EducationForm, ProfessionalExperienceForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from curriculums.models import PersonalData, Education, Contact, ProfessionalExperience

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save()
        
        messages.success(request, 'User created')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login_view.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    curriculum = PersonalData.objects.select_related('user', 'contact').prefetch_related(
        'experiences', 
        'education'
    ).filter(
        user=request.user,
    ).first()
    
    return render(request, 'authors/pages/dashboard.html',
    context={
        'curriculum': curriculum,
        'detail_page': True,
        'dashboard_page_view': True
   })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_curriculum_edit(request, id, form_type):
    if(form_type == "ContactForm"):
        curriculum = Contact.objects.filter(
            person__user=request.user,
            pk=id
            ).first()
    
        form = ContactForm(
            request.POST or None,
            instance=curriculum
        )

    if(form_type == "EducationForm"):
        curriculum = Education.objects.filter(
            person__user=request.user,
            pk=id
        ).first()


        form = EducationForm(
            request.POST or None,
            instance=curriculum
        )

    if(form_type == "ProfessionalExperienceForm"):   
        curriculum = ProfessionalExperience.objects.filter(
            person__user=request.user,
            pk=id
        ).first()


        form = ProfessionalExperienceForm(
            request.POST or None,
            instance=curriculum
        )          
    
    if not curriculum:
        raise Http404
    
    if form.is_valid():
        curriculum = form.save(commit=False)
        curriculum.person__user = request.user
        curriculum.save() 

        messages.success(request, 'Data updated')
        return redirect(reverse('authors:dashboard_curriculum_edit', args=(curriculum.id, form_type)))

    return render(request, 'authors/pages/dashboard_curriculum.html',
    context={
        'form': form,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_curriculum_new(request, form_type):
    personalData = PersonalData.objects.filter(user=request.user.id).first()

    if(form_type == "ContactForm"):
        form = ContactForm(
            request.POST or None,
        )

    if(form_type == "EducationForm"):
        form = EducationForm(
            request.POST or None,
        )

    if(form_type == "ProfessionalExperienceForm"):   
        form = ProfessionalExperienceForm(
            request.POST or None,
        )          
    
    if form.is_valid():
        curriculum = form.save(commit=False)
        curriculum.person = personalData
        curriculum.save() 

        messages.success(request, 'Data created')
        return redirect(reverse('authors:dashboard_curriculum_edit', args=(curriculum.id, form_type)))

    return render(request, 'authors/pages/dashboard_curriculum.html',
    context={
        'form': form,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_curriculum_delete(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    
    id = POST.get('id')
    form_type   = POST.get('type')

    if(form_type == "ContactForm"):
        curriculum = Contact.objects.filter(
            person__user=request.user,
            pk=id
        ).first()

    if(form_type == "EducationForm"):
        curriculum = Education.objects.filter(
            person__user=request.user,
            pk=id
        ).first()

    if(form_type == "ProfessionalExperienceForm"):   
        curriculum = ProfessionalExperience.objects.filter(
            person__user=request.user,
            pk=id
        ).first()

    if not curriculum:
        raise Http404
    
    curriculum.delete()
    messages.success(request, 'Delete successfully')
    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_curriculum_publish(request, id):
    curriculum = PersonalData.objects.filter(
        pk=id
    ).first()

    if not curriculum:
        raise Http404
    if curriculum.is_published:
        curriculum.is_published = False
    else:
        curriculum.is_published = True
    curriculum.save()
    messages.success(request, 'Status updated')
    return redirect(reverse('authors:dashboard'))
