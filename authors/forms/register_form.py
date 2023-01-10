from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.recipes.django_forms import add_placeholder, strong_password



class RegisterForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type your username here')
        add_placeholder(self.fields['first_name'], 'Type your first name here')
        add_placeholder(self.fields['last_name'], 'Type your last name here')
        add_placeholder(self.fields['email'], 'Type your email here')
    
    
    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'This field must not be empty.', 
            'min_length': 'Username must have at least 3 characters.',
            'max_length': 'Username must have at most 150 characters.'
        },
        help_text='The length of Username should be between 3 and 150 characters.',
        min_length=3,
        max_length=150,
    )
    
    
    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name'
            },
        label='First name'
    )
    
    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name'
            },
        label='Last name'
    )
    
    email = forms.EmailField(
        error_messages={
            'required': 'E-mail is required'
        },
        label='E-mail',
        help_text = ('The e-mail must be valid.')
    )
    
    
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
        label='Password',
    )
    
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repeat your password',
            },
        ),
        error_messages={'required': 'Please, repeat your password'},
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
        
        #widgets: dict = {
        #    'password': forms.PasswordInput(attrs={
        #        "placeholder": 'Type your password here.',
        #    })
        #}
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        existing_user = User.objects.filter(email=email).exists()
        
        if existing_user:
            raise ValidationError(
                'User email is already in use',
                code='invalid'
            )
        
        return email
    
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
        