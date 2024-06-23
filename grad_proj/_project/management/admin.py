from django.contrib import admin
from .models import RecentAction, Income, Expense

admin.site.register(RecentAction)
admin.site.register(Income)
admin.site.register(Expense)