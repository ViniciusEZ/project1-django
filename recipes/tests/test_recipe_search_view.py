from django.urls import resolve, reverse
from unittest import skip
from .. import views
from .test_recipe_base import RecipeTestBase



class RecipeSearchViewTest(RecipeTestBase): 
    def test_recipe_search_loads_correct_view_function(self):
        url = reverse("recipes:search")
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
        
        
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + '?q=testando')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
    
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + '?q=testando'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;testando&quot;',
            response.content.decode('utf-8'))