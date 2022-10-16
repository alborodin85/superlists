from django import forms
from lists.models import Item


class ItemForm(forms.models.ModelForm):
    """Форма для элемента списка"""

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }

    # item_text = forms.CharField(
    #     widget=forms.fields.TextInput(attrs={
    #         'placeholder': 'Enter a to-do item',
    #         'class': 'form-control input-lg',
    #     })
    # )
