from django import forms

from store.models import Category


class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'