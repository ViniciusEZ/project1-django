from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest



@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):   
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
                
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('invalid@INVALIDO')
        
        callback(form)
        return form
    
    
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Type your first name here')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)
        
    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Type your last name here')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)
        
        
    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Type your username here')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()
            
            self.assertIn('This field must not be empty.', form.text)
        self.form_field_test_with_callback(callback)
        
    
    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Type your email here')
            email_field.send_keys('invalidemail')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()
            
            self.assertIn('Enter a valid email address.', form.text)
        self.form_field_test_with_callback(callback)
        
    def test_password_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password here')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('aBC123@')
            password2.send_keys('aBC123@_diferenciado')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()
            
            self.assertIn('Password and confirmation password must be equal', form.text)
        self.form_field_test_with_callback(callback)
        
        
    def test_user_valid_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.get_by_placeholder(form, 'Type your first name here').send_keys('First Name')
        self.get_by_placeholder(form, 'Type your last name here').send_keys('Last Name')
        self.get_by_placeholder(form, 'Type your username here').send_keys('Username')
        self.get_by_placeholder(form, 'Type your email here').send_keys('email@email.com')
        self.get_by_placeholder(form, 'Type your password here').send_keys('aBC123@')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('aBC123@')
        form.submit()
        self.assertIn(
            "Your user is created, please log in.", 
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        

        
        
    
        
    
    
        
    
    