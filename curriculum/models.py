from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



class PersonalData(models.Model):    
    birthday = models.DateField()
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF must be in the format XXX.XXX.XXX-XX'
            )
        ]
    )
    marital_status = models.CharField(
        max_length=20,
        choices=[
            ('SINGLE', 'Single'),
            ('MARRIED', 'Married'),
            ('DIVORCED', 'Divorced'),
            ('WIDOWED', 'Widowed'),
        ]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Contact(models.Model):
    person = models.OneToOneField(
        PersonalData,
        on_delete=models.CASCADE,
        related_name='contact'
    )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
                message='Phone must be in the format (XX) XXXXX-XXXX'
            )
        ]
    )
    address = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='ZIP code must be in the format XXXXX-XXX'
            )
        ]
    )

    def __str__(self):
        return f"Contact of {self.person.user.email}"


class ProfessionalExperience(models.Model):
    person = models.ForeignKey(
        PersonalData,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.company}"

class Education(models.Model):
    person = models.ForeignKey(
        PersonalData,
        on_delete=models.CASCADE,
        related_name='education'
    )
    institution = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    degree = models.CharField(
        max_length=30,
        choices=[
            ('TECHNICAL', 'Technical'),
            ('BACHELOR', 'Bachelor'),
            ('SPECIALIZATION', 'Specialization'),
            ('MASTERS', 'Masters'),
            ('DOCTORATE', 'Doctorate'),
        ]
    )
    start_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    in_progress = models.BooleanField(default=False)

    ordering = ['-start_date']

    def __str__(self):
        return f"{self.course} at {self.institution}"
