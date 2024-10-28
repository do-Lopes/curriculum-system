from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder
from curriculums.models import Contact, ProfessionalExperience, Education
from utils.verify_datetime import is_start_date_greater_than_end_date


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['phone'], '(12) 34567-8901')
        add_placeholder(self.fields['address'], 'Street name, number')
        add_placeholder(self.fields['neighborhood'], 'Your neighborhood')
        add_placeholder(self.fields['city'], 'Your city')
        add_placeholder(self.fields['state'], 'ST')
        add_placeholder(self.fields['zip_code'], '12345-678')

    class Meta:
        model = Contact
        fields = ['phone', 'address', 'neighborhood', 'city', 'state', 'zip_code']

    phone = forms.CharField(
        error_messages={'required': 'Phone number is required'},
        label='Phone',
        help_text='Enter your phone number in the format (XX) XXXXX-XXXX'
    )

    address = forms.CharField(
        error_messages={'required': 'Address is required'},
        label='Address',
        max_length=200
    )

    neighborhood = forms.CharField(
        error_messages={'required': 'Neighborhood is required'},
        label='Neighborhood',
        max_length=100
    )

    city = forms.CharField(
        error_messages={'required': 'City is required'},
        label='City',
        max_length=100
    )

    state = forms.CharField(
        error_messages={'required': 'State is required'},
        label='State',
        max_length=2
    )

    zip_code = forms.CharField(
        error_messages={'required': 'ZIP code is required'},
        label='ZIP Code',
        help_text='Enter your ZIP code in the format XXXXX-XXX'
    )


class ProfessionalExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['position'], 'Your position')
        add_placeholder(self.fields['company'], 'Company name')
        add_placeholder(self.fields['description'], 'Describe your responsibilities')

    class Meta:
        model = ProfessionalExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'current', 'description']

    position = forms.CharField(
        error_messages={'required': 'Position is required'},
        label='Position',
        max_length=100
    )

    company = forms.CharField(
        error_messages={'required': 'Company is required'},
        label='Company',
        max_length=100
    )

    start_date = forms.DateField(
        error_messages={'required': 'Start date is required'},
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    current = forms.BooleanField(
        required=False,
        label='Current Job',
        widget=forms.CheckboxInput(attrs={'class': 'auth-register-form__current-job-field'})
    )

    description = forms.CharField(
        error_messages={'required': 'Description is required'},
        label='Description',
        widget=forms.Textarea(attrs={'class': 'auth-register-form__description-field'})
    )

    def clean(self):
        cleaned_data = super().clean()
        current = cleaned_data.get('current')
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')

        if is_start_date_greater_than_end_date(start_date, end_date):
            raise ValidationError(
                'The end date cannot be greater than the start date',
                code='invalid'
            )   
        
        elif current and end_date:
            raise ValidationError(
                'Cannot have end date if this is your current job',
                code='invalid'
            )
        elif not current and not end_date:
            raise ValidationError(
                'End date is required for past jobs',
                code='invalid'
            )

        return cleaned_data


class EducationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['institution'], 'Institution name')
        add_placeholder(self.fields['course'], 'Course name')


    class Meta:
        model = Education
        fields = ['institution', 'course', 'degree', 'start_date', 
                 'completion_date', 'in_progress']    

    institution = forms.CharField(
        error_messages={'required': 'Institution is required'},
        label='Institution',
        max_length=100
    )

    course = forms.CharField(
        error_messages={'required': 'Course is required'},
        label='Course',
        max_length=100
    )

    degree = forms.ChoiceField(
        choices=Education._meta.get_field('degree').choices,
        error_messages={'required': 'Degree is required'},
        label='Degree'
    )

    start_date = forms.DateField(
        error_messages={'required': 'Start date is required'},
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    completion_date = forms.DateField(
        required=False,
        label='Completion Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    in_progress = forms.BooleanField(
        required=False,
        label='In Progress',
    )

    def clean(self):
        cleaned_data = super().clean()
        in_progress = cleaned_data.get('in_progress')
        completion_date = cleaned_data.get('completion_date')
        start_date = cleaned_data.get('start_date')
        
        if is_start_date_greater_than_end_date(start_date, completion_date):            
            raise ValidationError(
                'The end date cannot be greater than the start date',
                code='invalid'
            )            

        elif in_progress and completion_date:            
            raise ValidationError(
                'Cannot have completion date if course is in progress',
                code='invalid'
            )
        
        elif not in_progress and not completion_date:
            raise ValidationError(
                'Completion date is required for completed courses',
                code='invalid'
            )

        return cleaned_data    