from django.urls import reverse
from django.test import TestCase

class AuthorURLsTest(TestCase):
    def test_author_register_url_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_author_register_create_url_is_correct(self):
        url = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')

    def test_author_login_url_is_correct(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_author_login_create_url_is_correct(self):
        url = reverse('authors:login_create')
        self.assertEqual(url, '/authors/login/create/')

    def test_author_logout_url_is_correct(self):
        url = reverse('authors:logout')
        self.assertEqual(url, '/authors/logout/')

    def test_author_dashboard_url_is_correct(self):
        url = reverse('authors:dashboard')
        self.assertEqual(url, '/authors/dashboard/')

    def test_author_dashboard_delete_url_is_correct(self):
        url = reverse('authors:dashboard_curriculum_delete')
        self.assertEqual(url, '/authors/dashboard/curriculum/delete/')

    def test_author_dashboard_publish_url_is_correct(self):
        url = reverse('authors:dashboard_curriculum_publish', kwargs={'id':1})
        self.assertEqual(url, '/authors/dashboard/curriculum/publish/1')

    def test_author_dashboard_new_url_is_correct(self):
        url = reverse('authors:dashboard_curriculum_new', kwargs={'form_type': 'CurriculoForm'})
        self.assertEqual(url, '/authors/dashboard/curriculum/new/CurriculoForm')

    def test_author_dashboard_edit_url_is_correct(self):
        url = reverse('authors:dashboard_curriculum_edit', kwargs={'id':1, 'form_type': 'CurriculoForm'})
        self.assertEqual(url, '/authors/dashboard/curriculum/edit/1/CurriculoForm')