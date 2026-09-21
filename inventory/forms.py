from django import forms
from .models import StockItem, StockMovement


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['name', 'unit', 'quantity', 'reorder_level']


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['change', 'reason', 'note']
        widgets = {'note': forms.TextInput(attrs={'placeholder': 'Optional note'})}
