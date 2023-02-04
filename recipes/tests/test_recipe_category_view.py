from django.urls import resolve, reverse
from unittest import skip
from .. import views
from .test_recipe_base import RecipeTestBase



class RecipeCategoryViewTest(RecipeTestBase):   
    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)
             
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):  
        response = self.client.get(reverse('recipes:category', 
                                        kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)
        
        
    def test_recipe_category_template_loads_recipes(self):
        title_test = 'Category test'
        self.make_recipe(title=title_test)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        response_recipes = response.context['recipes']
        content = response.content.decode('utf-8')
        
        self.assertIn(title_test, content)
        
        
    def test_recipe_category_template_doesnt_load_recipes_not_published(self):
        
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse('recipes:category', kwargs={'pk': recipe.category_id})
        )
        
        self.assertEqual(response.status_code, 404)