from django.http import HttpResponse
import openpyxl
from .models import Expense
from .forms import ExpenseForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages


def expenses_list(request):
    date_filter_start = request.GET.get('date_filter_start', '')
    date_filter_end = request.GET.get('date_filter_end', '')
    model_filter = request.GET.get('model_filter', '').lower()
    fabric_filter = request.GET.get('fabric_filter', '').lower()

    expenses = Expense.objects.filter(user=request.user)

    if date_filter_start and date_filter_end:
        expenses = expenses.filter(date__range=[date_filter_start, date_filter_end])

    if model_filter:
        expenses = expenses.filter(Q(model_name__icontains=model_filter))

    if fabric_filter:
        expenses = expenses.filter(Q(name_fabric__icontains=fabric_filter))

    total_total = expenses.aggregate(total=Sum('total'))['total']

    return render(request, 'expenses_list.html', {
        'expenses': expenses,
        'date_filter_start': date_filter_start,
        'date_filter_end': date_filter_end,
        'model_filter': model_filter,
        'fabric_filter': fabric_filter,
        'total_total': total_total,
    })


class EditExpenseView(FormView):
    template_name = 'edit_expense.html'
    form_class = ExpenseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Expense.objects.get(pk=self.kwargs['pk'], user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('expenses_list')

    def get_success_url(self):
        return reverse_lazy('expenses_list')


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form})


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


def export_expenses(request):
    date_filter_start = request.GET.get('date_filter_start', '')
    date_filter_end = request.GET.get('date_filter_end', '')
    model_filter = request.GET.get('model_filter', '')
    fabric_filter = request.GET.get('fabric_filter', '')

    # Фильтрация расходов
    expenses = Expense.objects.filter(user=request.user)

    if date_filter_start and date_filter_end:
        expenses = expenses.filter(date__range=[date_filter_start, date_filter_end])

    if model_filter:
        expenses = expenses.filter(model_name__iexact=model_filter)

    if fabric_filter:
        expenses = expenses.filter(name_fabric__iexact=fabric_filter)

    # Экспорт в Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = (f'attachment; filename="expenses_{date_filter_start}_{date_filter_end}_{model_filter}_{fabric_filter}.xlsx"')

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Заголовки
    headers = ["Дата", "Модель", 'Назв. ткани', "Ткань", "Фурнитура", "Нитки", "Другое", "Пошив", "Итого"]
    for col_num, header in enumerate(headers, 1):
        col_letter = openpyxl.utils.get_column_letter(col_num)
        worksheet[f"{col_letter}1"] = header

    # Данные
    for row_num, expense in enumerate(expenses, 2):
        worksheet[f"A{row_num}"] = expense.date.strftime("%d-%m-%Y")
        worksheet[f"B{row_num}"] = expense.model_name
        worksheet[f"C{row_num}"] = expense.name_fabric
        worksheet[f"D{row_num}"] = expense.fabric
        worksheet[f"E{row_num}"] = expense.accessories
        worksheet[f"F{row_num}"] = expense.threads
        worksheet[f"G{row_num}"] = expense.other
        worksheet[f"H{row_num}"] = expense.sewing
        worksheet[f"I{row_num}"] = expense.total

    try:
        workbook.save(response)
    except Exception as e:
        print(f"An error occurred: {e}")
    return response


def delete_all_expenses(request):
    Expense.objects.all().delete()
    messages.success(request, "Все записи были успешно удалены.")
    return redirect('expenses_list')


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('expenses_list')