from django import forms
from .models import Category, ProductFood
from accounts.validators import image_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']



class ProductFoodForm(forms.ModelForm):
    image = forms.FileField(validators=[image_validator])
    image.widget.attrs.update({'class': 'btn btn-info w-100'}),
    class Meta:
        model = ProductFood
        fields = ['category','food_title', 'description', 'price', 'image', 'is_available']       