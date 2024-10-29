from authors.forms import RegisterForm
from unittest import TestCase
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([ 
        ('username', 'Your username'),       
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([  
        ('username', (
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        )),
        ('email', 'The E-mail must be valid'),   
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].help_text
        self.assertEqual(current, needed)

    @parameterized.expand([  
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].label
        self.assertEqual(current, needed)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'fist',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Abc12345678',
            'password2': 'Abc12345678',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([        
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'E-mail is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'leo'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_upper_lower_case_letters_and_numbers(self):
        self.form_data['password'] = 'ab12'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Abc123456'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context['form'].errors.get('password'))


    def test_password_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Passwords must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password2'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_send_request(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_email_are_not_equal(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is alredy in use'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_author_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'lazabisc',
            'password': 'Abc12345678',
            'password2': 'Abc12345678',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='lazabisc',
            password='Abc12345678'
        )

        self.assertTrue(is_authenticated)