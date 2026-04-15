from datetime import datetime

from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category
from django.db.models import Q, Sum

def budget_dashboard(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transactions = Transaction.objects.all()
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59)
            transactions = transactions.filter(created_at__range=(start, end))
        except ValueError:
            pass

    total_debit = Transaction.objects.filter(transaction_type='DEBIT').aggregate(Sum('amount'))['amount__sum'] or 0
    total_credit = Transaction.objects.filter(transaction_type='CREDIT').aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_debit - total_credit

    context = {
        'transactions': transactions,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'balance': balance,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'transactions/budget.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'transactions/categories.html', {'categories': categories})

#2
def transactins_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = category.transactions.all()
    return render(request, 'transactions/by_category.html',
                  {
                      'category': category,
                      'transactions': transactions
                  })
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        transactions = transactions.filter(desc__icontains=query)

    category_id = request.GET.get('category')
    if category_id:
        transactions = transactions.filter(category_id=category_id)

    sort = request.GET.get('sort', 'id')
    if sort in ['amount', '-amount', 'desc', '-desc']:
        transactions = transactions.order_by(sort)

    context = {
        'transactions': transactions,
        'categories': categories,
    }
    return render(request, 'transactions/transaction_list.html', context)