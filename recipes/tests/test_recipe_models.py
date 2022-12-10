from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
            
            
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Categoria'),
            author=self.make_author(username='Avidotia'),
            title='Recipe Title',
            description = 'Recipe description',  
            slug = 'avidotia-slug',
            preparation_time = 10,
            preparation_time_unit ='Minutos',     
            servings =5, 
            servings_unit = 'Porções',    
            preparation_steps ='Recipe preparation steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
            
    @parameterized.expand([
            ('title', 70),
            ('description', 170),
            ('preparation_time_unit', 70),
            ('servings_unit', 70),
        ])     
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
            
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html isnt false',
        )
        
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published isnt false',
        )
        
        
    def test_recipe_string_representation(self):
        needed = 'Testing repr'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
            msg=f'Recipe String representation must be "{needed}"')
        
    
        