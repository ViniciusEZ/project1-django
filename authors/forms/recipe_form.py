from django import forms
from recipes.models import Recipe
from utils.recipes.django_forms import add_attr
from utils.recipes.vstrings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._merrors = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        
        
        
    class Meta:
        model = Recipe
        fields = (
            'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover',
        )
        
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }
        
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        
        cd = self.cleaned_data
        title = cd.get('title')
        description = cd.get('description')
        
        if len(title) < 5:
            self._merrors['title'].append('Title must have at least 5 characters.')
        
        if title == description:
            self._merrors['title'].append('Title can not be equal to description.')
            self._merrors['description'].append('Description can not be equal to title.')
            
            
            
        if self._merrors:
            raise ValidationError(self._merrors)
        
            
        return super_clean
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        
        if not is_positive_number(preparation_time):
            self._merrors['preparation_time'].append('Must be a positive number.')
            
        return preparation_time
            
            