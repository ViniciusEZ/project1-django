from unittest import TestCase
from authors.forms import RegisterForm 
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase
from django.urls import reverse

class AuthorRegisterFormUnittest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username here'),
        ('first_name', 'Type your first name here'),
        ('last_name', 'Type your last name here'),
        ('email', 'Type your email here'),
        ('password', 'Type your password here'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)
        
    
    
    @parameterized.expand([
        ('password','Password must have at least: '
                'One uppercase letter, one lowercase letter '
                'and one number'),
        ('email', 'The e-mail must be valid.'),
        ('username', 'The length of Username should be between 3 and 150 characters.')
    ])   
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        
        
    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirmation Password')
    ])   
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
        
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@aemail.com',
            'password': 'Str0ngPassword',
            'password2': 'Str0ngPassword'
        }
        return super().setUp(*args, **kwargs)
    
    
    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
        
    def test_username_field_min_length_should_be_3(self):
        self.form_data['username'] = 'Vi'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have at least 3 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
        
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'V' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have at most 150 characters.'
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
        
    def test_password_field_match_with_strong_password(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = ('Password must have at least: '
        'One uppercase letter '
        'One number '
        'One lowercase letter and length should be at least 6 characters.')
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        
    def test_password_and_confirmation_password_are_equal(self):
        self.form_data['password'] = '@Aabc123'
        self.form_data['password2'] = '@Aabc1234'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = ('Password and confirmation password must be equal')
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        
    def test_if_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) 
        
        
    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User email is already in use'
        
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        