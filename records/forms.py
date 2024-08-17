from django import forms
from .models import ProductionRecord


class ProductionRecordForm(forms.ModelForm):
    class Meta:
        model = ProductionRecord
        exclude = ['total', 'date']

        labels = {
            'model': 'Модель',
            'name': 'Мастер',
            'quantity': 'Количество',
            'received_by': 'Принял',
            'price': 'Цена',
        }

        property = {
            'Edit': 'Изменить'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['model'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['received_by'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
