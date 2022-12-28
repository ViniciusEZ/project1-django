from django.test import TestCase
from authors.forms import RegisterForm 
from parameterized import parameterized

class AuthorRegisterFormUnittest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username here'),
        ('first_name', 'Type your first name here'),
        ('last_name', 'Type your last name here'),
        ('email', 'Type your email here'),
        ('password', 'Type your password here'),
        ('password2', 'Repeat your password'),
    ])
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)