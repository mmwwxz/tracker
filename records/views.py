from django.http import HttpResponse
import openpyxl
from .models import ProductionRecord
from .forms import ProductionRecordForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages


def record_list(request):
    name_filter = request.GET.get('name_filter', '').lower()
    model_filter = request.GET.get('model_filter', '').lower()
    date_filter_start = request.GET.get('date_filter_start', '')
    date_filter_end = request.GET.get('date_filter_end', '')

    records = ProductionRecord.objects.filter(user=request.user)

    if name_filter:
        records = records.filter(Q(name__icontains=name_filter))

    if model_filter:
        records = records.filter(Q(model__icontains=model_filter))

    if date_filter_start and date_filter_end:
        records = records.filter(date__range=[date_filter_start, date_filter_end])

    total_total = records.aggregate(total=Sum('total'))['total']

    return render(request, 'record_list.html', {
        'records': records,
        'name_filter': name_filter,
        'model_filter': model_filter,
        'date_filter_start': date_filter_start,
        'date_filter_end': date_filter_end,
        'total_total': total_total,
    })


class EditRecordView(FormView):
    template_name = 'records/edit_record.html'
    form_class = ProductionRecordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = ProductionRecord.objects.get(pk=self.kwargs['pk'], user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('record_list')

    def get_success_url(self):
        return reverse_lazy('record_list')


def edit_record(request, pk):
    record = get_object_or_404(ProductionRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProductionRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = ProductionRecordForm(instance=record)

    return render(request, 'edit_record.html', {'form': form})


def add_record(request):
    if request.method == 'POST':
        form = ProductionRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('record_list')
    else:
        form = ProductionRecordForm()
    return render(request, 'add_record.html', {'form': form})


def export_records(request):
    name_filter = request.GET.get('name_filter', '')
    model_filter = request.GET.get('model_filter', '')
    date_filter_start = request.GET.get('date_filter_start', '')
    date_filter_end = request.GET.get('date_filter_end', '')

    # Фильтрация записей
    records = ProductionRecord.objects.filter(user=request.user)

    if name_filter:
        records = records.filter(name__iexact=name_filter)

    if model_filter:
        records = records.filter(model__iexact=model_filter)

    if date_filter_start and date_filter_end:
        records = records.filter(date__range=[date_filter_start, date_filter_end])

    # Экспорт в Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = (f'attachment; filename="production_records_{name_filter}_{model_filter}_'
                                       f'{date_filter_start}_{date_filter_end}.xlsx"')

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Заголовки
    headers = ["Дата", "Модель", "Мастер", "Кол-во", "Принял", "Цена", "Итого"]
    for col_num, header in enumerate(headers, 1):
        col_letter = openpyxl.utils.get_column_letter(col_num)
        worksheet[f"{col_letter}1"] = header

    # Данные
    for row_num, record in enumerate(records, 2):
        worksheet[f"A{row_num}"] = record.date.strftime("%Y-%m-%d")
        worksheet[f"B{row_num}"] = record.model
        worksheet[f"C{row_num}"] = record.name
        worksheet[f"D{row_num}"] = record.quantity
        worksheet[f"E{row_num}"] = record.received_by
        worksheet[f"F{row_num}"] = record.price
        worksheet[f"G{row_num}"] = record.total

    workbook.save(response)
    return response


def delete_all_records(request):
    ProductionRecord.objects.all().delete()
    messages.success(request, "Все записи были успешно удалены.")
    return redirect('record_list')


def delete_record(request, pk):
    record = get_object_or_404(ProductionRecord, pk=pk)
    record.delete()
    return redirect('record_list')