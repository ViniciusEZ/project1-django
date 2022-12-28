from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
    
    
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z]+)(?=.*[A-Z]+)(?=.*[0-9]+).{6,}$')
    
    if not regex.match(password):
        raise ValidationError(('Password must have at least: '
                   'One uppercase letter '
                   'One number '
                   'One lowercase letter and length should be at least 6 characters.'),
                   code='invalid'
                )


class RegisterForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type your username here')
        add_placeholder(self.fields['first_name'], 'Type your first name here')
        add_placeholder(self.fields['last_name'], 'Type your last name here')
        add_placeholder(self.fields['email'], 'Type your email here')
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Type your password here',
            },
        ),
        error_messages={'required': 'Password must not be empty'},
        help_text=('Password must have at least: '
                   'One uppercase letter, one lowercase letter '
                   'and one number'),
        validators=[strong_password],
    )
    
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repeat your password',
            },
        ),
        label='Confirmation Password',
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username',
            'email',
            'password',
            ]
        
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        
        help_texts = {
            'email': 'The e-mail must be valid.'
        }
        
        
        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
            }
        }
        
        #widgets: dict = {
        #    'password': forms.PasswordInput(attrs={
        #        "placeholder": 'Type your password here.',
        #    })
        #}
        
        
    def clean_password(self):
        data = self.cleaned_data.get("password", '')
        
        if 'atencao' in data:
            raise ValidationError(
                'Não pode %(value)s no password',
                code='invalid',
                params={'value': '"atencao"'}
                )
        
        return data
    
    
    def clean_first_name(self):
        data = self.cleaned_data.get("first_name", '')
        
        if 'Vinicius' in data:
            raise ValidationError(
                'Não pode %(value)s no first name',
                code='invalid',
                params={'value': '"Vinicius"'}
                )
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and confirmation password must be equal',
                code='invalid'
            )
            
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            })
        