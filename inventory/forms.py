from django import forms
from django.utils import timezone
from .models import SKU, Inventory, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

# Form for SKU
class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = ['name', 'description', 'category', 'weight', 'dimensions', 'bbe', 'batch', 'manufacturing_date', 'shelf_life_end']
        widgets = {
            'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
            'bbe': forms.DateInput(attrs={'type': 'date'}),
            'shelf_life_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_manufacturing_date(self):
        manufacturing_date = self.cleaned_data.get('manufacturing_date')
        if manufacturing_date and manufacturing_date > timezone.now().date():
            raise ValidationError("Manufacturing date cannot be in the future.")
        return manufacturing_date

# Form for Inventory
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['sku', 'category', 'user']
        widgets = {
            'category': forms.Select(),
            'user': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['user'].queryset = User.objects.filter(is_active=True).order_by('username')


# Form for Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']