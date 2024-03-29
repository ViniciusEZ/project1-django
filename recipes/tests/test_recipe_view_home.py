from django.urls import resolve, reverse
from unittest.mock import patch
from .. import views
from .test_recipe_base import RecipeTestBase



class RecipeHomeViewTest(RecipeTestBase): 
    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)
        
        
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
        
        
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")
        
       
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn('No recipes found here.', response.content.decode('utf-8'))
        
        
    def test_recipe_home_template_loads_recipes(self):
        
        self.make_recipe(category_data={'name': 'Salgado'}, 
                        author_data={'first_name': 'Joana'})
        
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        content = response.content.decode('utf-8')
        
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertIn('Joana', content)
        self.assertIn('Salgado', content)
        self.assertEqual(len(response_recipes), 1)

        
    def test_recipe_home_template_does_not_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        
        self.assertIn('No recipes found here.', content)
        
    def test_recipe_home_is_paginated(self):
        for i in range(15):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug':f'r{i}'}
            self.make_recipe(**kwargs)
            
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator
            
            self.assertEqual(paginator.num_pages, 5)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
            
            
    def test_invalid_page_query_uses_page_one(self):
        for i in range(15):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug':f'r{i}'}
            self.make_recipe(**kwargs)
            
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1')
            self.assertEqual(response.context['recipes'].number, 1)
            
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(response.context['recipes'].number, 2)
            
    