from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>', views.transactins_by_category, name='transactions_by_category'),
    path('', views.transaction_list, name='transaction_list'),
    path('budget/', views.budget_dashboard, name='budget_dashboard'),
]