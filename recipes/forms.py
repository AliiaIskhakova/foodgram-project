from django.forms import CheckboxSelectMultiple, ModelForm

from .models import Recipe


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'cooking_time', 'description', 'image', 'ingredientsf')
        widgets = {
            'tag': CheckboxSelectMultiple(),
        }
