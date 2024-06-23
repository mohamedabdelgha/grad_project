from django.shortcuts import render, redirect, get_object_or_404
from user.views import management_send_data
from .models import *
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime,timedelta

def management(request):
    current_date = timezone.now()

    # Current month start and end
    start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

    # Year start and end
    start_of_year = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = current_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # January start and end
    start_of_january = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_january = current_date.replace(month=1, day=31, hour=23, minute=59, second=59, microsecond=999999)

    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    workers_num = Employee.objects.filter(job="worker").count()
    supervisors_num = Employee.objects.filter(job="supervisor").count()

    total_salaries = Employee.objects.all().aggregate(Sum('salary'))['salary__sum'] or 0
    total_incomes = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_profit = total_incomes - total_expenses

    month_incomes = Income.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_expenses = Expense.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_profit = month_incomes - month_expenses

    year_incomes = Income.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_expenses = Expense.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_profit = year_incomes - year_expenses

    january_incomes = Income.objects.filter(date__gte=start_of_january, date__lte=end_of_january).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        "total_salaries": total_salaries,
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "month_incomes": month_incomes,
        "month_expenses": month_expenses,
        "month_profit": month_profit,
        "year_incomes": year_incomes,
        "year_expenses": year_expenses,
        "year_profit": year_profit,
        "january_incomes": january_incomes,
        "workers_num": workers_num,
        "supervisors_num": supervisors_num,
    }

    return render(request, "management/management.html", context)

def incomes(request):
    incomes = Income.objects.all().order_by("-date")
    if "addIncome" in request.POST:
        site  = request.POST.get("site")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Income.objects.create(site = site, amount = amount, date = date)
        messages.success(request, "income added succesfully")
        return redirect("incomes")
    context = {"incomes" : incomes}
    return render(request, "management/incomes.html", context)

def expenses(request):
    expenses = Expense.objects.all().order_by("-date")
    if "addExpense" in request.POST:
        expense_type  = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Expense.objects.create(expense_type = expense_type, amount = amount, date = date)
        messages.success(request, "Expense added succesfully")
        return redirect("expenses")
    context = {"expenses" : expenses}
    return render(request, "management/expenses.html", context)

def purchases(request):
    purchases = Purchase.objects.all().order_by("-date")
    if "addPurchase" in request.POST:
        site  = request.POST.get("site")
        purchase_type  = request.POST.get("purchase_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Purchase.objects.create(site=site , purchase_type = purchase_type, amount = amount, date = date)
        messages.success(request, "Purchase added succesfully")
        return redirect("purchases")
    context = {"purchases" : purchases}
    return render(request, "management/purchases.html", context)

def employees(request):
    employees = Employee.objects.all()
    if "addEmployee" in request.POST:
        name  = request.POST.get("name")
        salary  = request.POST.get("salary")
        job = request.POST.get("job")
        Employee.objects.create(name=name , salary = salary, job = job , remain_salary = salary)
        messages.success(request, "Employee added succesfully")
        return redirect("employees")
    context = {"employees" : employees}
    return render(request, "management/employees.html", context)

def analytics(request):

    tax_expenses = Expense.objects.filter(expense_type = "taxes").aggregate(Sum('amount'))['amount__sum'] or 0
    rent_expenses = Expense.objects.filter(expense_type = "rent").aggregate(Sum('amount'))['amount__sum'] or 0
    assurance_expenses = Expense.objects.filter(expense_type = "assurance").aggregate(Sum('amount'))['amount__sum'] or 0
    maintenance_expenses = Expense.objects.filter(expense_type = "maintenance").aggregate(Sum('amount'))['amount__sum'] or 0
    other_expenses = Expense.objects.filter(expense_type = "other").aggregate(Sum('amount'))['amount__sum'] or 0

    current_date = timezone.now()

    # Current month start and end
    start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

    # Year start and end
    start_of_year = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = current_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # January start and end
    start_of_january = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_january = current_date.replace(month=1, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # February start and end (accounting for leap years)
    start_of_feb = current_date.replace(month=2, day=1, hour=0, minute=0, second=0, microsecond=0)
    if current_date.year % 4 == 0 and (current_date.year % 100 != 0 or current_date.year % 400 == 0):
        end_of_feb = current_date.replace(month=2, day=29, hour=23, minute=59, second=59, microsecond=999999)
    else:
        end_of_feb = current_date.replace(month=2, day=28, hour=23, minute=59, second=59, microsecond=999999)

    # March start and end
    start_of_mar = current_date.replace(month=3, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_mar = current_date.replace(month=3, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # April start and end
    start_of_apr = current_date.replace(month=4, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_apr = current_date.replace(month=4, day=30, hour=23, minute=59, second=59, microsecond=999999)

    # May start and end
    start_of_may = current_date.replace(month=5, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_may = current_date.replace(month=5, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # June start and end
    start_of_jun = current_date.replace(month=6, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_jun = current_date.replace(month=6, day=30, hour=23, minute=59, second=59, microsecond=999999)

    # July start and end
    start_of_jul = current_date.replace(month=7, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_jul = current_date.replace(month=7, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # August start and end
    start_of_aug = current_date.replace(month=8, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_aug = current_date.replace(month=8, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # September start and end
    start_of_sep = current_date.replace(month=9, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_sep = current_date.replace(month=9, day=30, hour=23, minute=59, second=59, microsecond=999999)

    # October start and end
    start_of_oct = current_date.replace(month=10, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_oct = current_date.replace(month=10, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # November start and end
    start_of_nov = current_date.replace(month=11, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_nov = current_date.replace(month=11, day=30, hour=23, minute=59, second=59, microsecond=999999)

    # December start and end
    start_of_dec = current_date.replace(month=12, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_dec = current_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    jan_incomes = Income.objects.filter(date__gte=start_of_january, date__lte=end_of_january).aggregate(Sum('amount'))['amount__sum'] or 0
    feb_incomes = Income.objects.filter(date__gte=start_of_feb, date__lte=end_of_feb).aggregate(Sum('amount'))['amount__sum'] or 0
    mar_incomes = Income.objects.filter(date__gte=start_of_mar, date__lte=end_of_mar).aggregate(Sum('amount'))['amount__sum'] or 0
    apr_incomes = Income.objects.filter(date__gte=start_of_apr, date__lte=end_of_apr).aggregate(Sum('amount'))['amount__sum'] or 0
    may_incomes = Income.objects.filter(date__gte=start_of_may, date__lte=end_of_may).aggregate(Sum('amount'))['amount__sum'] or 0
    jun_incomes = Income.objects.filter(date__gte=start_of_jun, date__lte=end_of_jun).aggregate(Sum('amount'))['amount__sum'] or 0
    jul_incomes = Income.objects.filter(date__gte=start_of_jul, date__lte=end_of_jul).aggregate(Sum('amount'))['amount__sum'] or 0
    aug_incomes = Income.objects.filter(date__gte=start_of_aug, date__lte=end_of_aug).aggregate(Sum('amount'))['amount__sum'] or 0
    sep_incomes = Income.objects.filter(date__gte=start_of_sep, date__lte=end_of_sep).aggregate(Sum('amount'))['amount__sum'] or 0
    oct_incomes = Income.objects.filter(date__gte=start_of_oct, date__lte=end_of_oct).aggregate(Sum('amount'))['amount__sum'] or 0
    nov_incomes = Income.objects.filter(date__gte=start_of_nov, date__lte=end_of_nov).aggregate(Sum('amount'))['amount__sum'] or 0
    dec_incomes = Income.objects.filter(date__gte=start_of_dec, date__lte=end_of_dec).aggregate(Sum('amount'))['amount__sum'] or 0




    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    workers_num = Employee.objects.filter(job="worker").count()
    supervisors_num = Employee.objects.filter(job="supervisor").count()

    total_salaries = Employee.objects.all().aggregate(Sum('salary'))['salary__sum'] or 0
    total_incomes = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_profit = total_incomes - total_expenses

    month_incomes = Income.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_expenses = Expense.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_profit = month_incomes - month_expenses

    year_incomes = Income.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_expenses = Expense.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_profit = year_incomes - year_expenses

    context = {
        "jan_incomes": jan_incomes,
        "feb_incomes": feb_incomes,
        "mar_incomes": mar_incomes,
        "apr_incomes": apr_incomes,
        "may_incomes": may_incomes,
        "jun_incomes": jun_incomes,
        "jul_incomes": jul_incomes,
        "aug_incomes": aug_incomes,
        "sep_incomes": sep_incomes,
        "oct_incomes": oct_incomes,
        "nov_incomes": nov_incomes,
        "dec_incomes": dec_incomes,
        "tax_expenses": tax_expenses,
        "rent_expenses": rent_expenses,
        "assurance_expenses": assurance_expenses,
        "maintenance_expenses": maintenance_expenses,
        "other_expenses": other_expenses,
        "total_salaries": total_salaries,
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "month_incomes": month_incomes,
        "month_expenses": month_expenses,
        "month_profit": month_profit,
        "year_incomes": year_incomes,
        "year_expenses": year_expenses,
        "year_profit": year_profit,
        "workers_num": workers_num,
        "supervisors_num": supervisors_num,

    }
    return render(request, "management/analytics.html", context)

# ==============================================================================
def update_employee(request, id):
    if "updateEmployee" in request.POST:
        name = request.POST.get("name")
        salary = request.POST.get("salary")
        remain_salary = request.POST.get("remain_salary")
        job = request.POST.get("job")

        employee = Employee.objects.get(id=id)
        employee.name=name
        employee.salary=salary
        employee.remain_salary = remain_salary
        employee.job=job
        employee.save()

        messages.success(request, "Employee Updated successfully")
        return redirect("employees")
# ==============================================================================
def update_expense(request, id):
    if "updateExpense" in request.POST:
        expense_type = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        employee = Expense.objects.get(id=id)
        employee.expense_type=expense_type
        employee.amount=amount
        employee.date = date
        employee.save()

        messages.success(request, "Expense Updated successfully")
        return redirect("expenses")
# ==============================================================================
def update_income(request, id):
    if "updateIncome" in request.POST:
        site = request.POST.get("site")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        employee = Income.objects.get(id=id)
        employee.site=site
        employee.amount=amount
        employee.date = date
        employee.save()

        messages.success(request, "Income Updated successfully")
        return redirect("incomes")
# ==============================================================================
def update_purchase(request, id):
    if "updatePurchase" in request.POST:
        purchase_type = request.POST.get("purchase_type")
        site = request.POST.get("site")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        employee = Purchase.objects.get(id=id)
        employee.purchase_type=purchase_type
        employee.site=site
        employee.amount=amount
        employee.date = date
        employee.save()

        messages.success(request, "purchase Updated successfully")
        return redirect("purchases")
# ==============================================================================
def delete_income(request, id):
    income_to_delete = get_object_or_404(Income, id =id )
    income_to_delete.delete()
    messages.success(request, "Income deleted successfully")
    return redirect("incomes")

def delete_expense(request, id):
    expense_to_delete = get_object_or_404(Expense, id =id )
    expense_to_delete.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("expenses")

def delete_purchase(request, id):
    purchase_to_delete = get_object_or_404(Purchase, id =id )
    purchase_to_delete.delete()
    messages.success(request, "purchase deleted successfully")
    return redirect("purchases")

def delete_employee(request, id):
    employee_to_delete = get_object_or_404(Employee, id =id )
    employee_to_delete.delete()
    messages.success(request, "employee deleted successfully")
    return redirect("employees")
    
