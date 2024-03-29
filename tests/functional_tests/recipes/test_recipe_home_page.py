from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch
import pytest

@pytest.mark.functional_test
class RecipeHomePageTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=5)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)
        
        
    @patch('recipes.views.PER_PAGE', new=5)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=20)
        title_needed = 'Recipe Title 0'
        
        self.browser.get(self.live_server_url)
        
        search_input = self.browser.find_element(
            By.XPATH, 
            '//input[@placeholder="Search for a recipe..."]'
        )
        
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        
        self.assertIn(
            title_needed, 
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )
        
        self.sleep()
        
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(qtd=20)
        
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        
        # Vê que tem uma paginação e clica na página dois
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'    
        )
        page2.click()
        
        # Vê que têm mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
    
    
        