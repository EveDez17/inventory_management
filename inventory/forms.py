from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import SKU, Inventory, Category, Address, Supplier

from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit, Layout, Field


class SKuForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = [
            "name",
            "description",
            "category",
            "weight",
            "dimensions",
            "bbe",
            "batch",
            "manufacturing_date",
            "shelf_life_end",
            "supplier",
        ]


class AddSKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = [
            "name",
            "description",
            "category",
            "weight",
            "dimensions",
            "bbe",
            "batch",
            "manufacturing_date",
            "shelf_life_end",
            "supplier",
        ]


class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SKUForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name", css_class="my-class"),
            "description",
            "category",
            "weight",
            "dimensions",
            "bbe",  # Best Before End Date, I assume?
            "batch",
            "manufacturing_date",
            "shelf_life_end",
            "supplier",
            Submit("submit", "Submit", css_class="btn-success"),
        )


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"  # Include all fields from the Inventory model


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CategoryForm(
    forms.Form
):  # Using Form if you don't need to directly create/update Category model instances
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select Category"
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"  # Include all fields from the Address model


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"  # Include all fields from the Supplier model
        widgets = {
            "supplier_email": forms.EmailInput(attrs={"type": "email"}),
        }
