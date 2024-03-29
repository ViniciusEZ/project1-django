from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_pass = "aBC123@"
        user = User.objects.create_user(username='my_user', password=string_pass)
        
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        
        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)
        
        # Usuário envia o formulário
        form.submit()
        
        self.assertIn(
            f'You are logged in with {user.username}.', 
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
    
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
    def test_form_login_has_invalid_values(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        
        # Usuário tenta enviar valores vazios.
        username_field.send_keys(' ')
        password_field.send_keys(' ')
        form.submit()
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
        
    def test_form_login_non_registered_user(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        
        # Usuário tenta enviar valores vazios.
        username_field.send_keys('NonRegistered')
        password_field.send_keys('aBC123@')
        form.submit()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
    
        
        
    
