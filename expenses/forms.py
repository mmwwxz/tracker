from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'model_name', 'name_fabric', 'fabric', 'accessories', 'threads', 'other', 'sewing', 'total']
        exclude = ['total', 'date']
        labels = {
            'model_name': 'Модель',
            'name_fabric': 'Назв. ткани',
            'fabric': 'Ткань',
            'accessories': 'Фурнитура',
            'threads': 'Нитки',
            'other': 'Другое',
            'sewing': 'Пошив',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name_fabric'].widget.attrs.update({'class': 'form-control'})
        self.fields['fabric'].widget.attrs.update({'class': 'form-control'})
        self.fields['sewing'].widget.attrs.update({'class': 'form-control'})
        self.fields['threads'].widget.attrs.update({'class': 'form-control'})
        self.fields['accessories'].widget.attrs.update({'class': 'form-control'})
        self.fields['other'].widget.attrs.update({'class': 'form-control'})
