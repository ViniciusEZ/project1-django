from django.urls import resolve, reverse
from unittest import skip
from .. import views
from .test_recipe_base import RecipeTestBase



class RecipeDetailViewTest(RecipeTestBase):   
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', 
                                        kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
        
        
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        title_test = 'Detail recipe'
        self.make_recipe(title=title_test)
        
        response = self.client.get(reverse('recipes:recipe', 
                                        kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        
        self.assertIn(title_test, content)
     
        
        
    def test_recipe_detail_template_doesnt_load_recipe_not_published(self):
        
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )
        
        self.assertEqual(response.status_code, 404)
        
        
    
   