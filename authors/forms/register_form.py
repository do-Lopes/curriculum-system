from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password
from django.core.validators import RegexValidator
from curriculums.models import PersonalData


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        add_placeholder(self.fields['cpf'], 'XXX.XXX.XXX-XX')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The E-mail must be valid',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password'
        },
        label='Password2'
    )

    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': 'Birthday is required'},
        label='Birthday'
    )
    
    cpf = forms.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF must be in the format XXX.XXX.XXX-XX'
            )
        ],
        error_messages={'required': 'CPF is required'},
        label='CPF'
    )
    
    marital_status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'auth-register-form__input-wrapper'}),  
        choices=[
            ('SINGLE', 'Single'),
            ('MARRIED', 'Married'),
            ('DIVORCED', 'Divorced'),
            ('WIDOWED', 'Widowed'),
        ],
        error_messages={'required': 'Marital status is required'},
        label='Marital Status',         
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',            
            'birthday',
            'cpf',
            'marital_status',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid'
            )

        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cpf_exists = PersonalData.objects.filter(cpf=cpf).exists()

        if cpf_exists:
            raise ValidationError(
                'CPF is already in use', code='invalid'
            )

        return cpf

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Passwords must be equal', 
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error, 
            })
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            personal_data = PersonalData(
                user=user,
                birthday=self.cleaned_data['birthday'],
                cpf=self.cleaned_data['cpf'],
                marital_status=self.cleaned_data['marital_status']
            )
            personal_data.save()
            
        return user
        

