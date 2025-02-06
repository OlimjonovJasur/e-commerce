from django import forms

from .models import ProductComment, Product, Customers


class ProductCommentForm(forms.ModelForm):

    class Meta:
        model = ProductComment
        fields = ['rating', 'name', 'email', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '5'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
