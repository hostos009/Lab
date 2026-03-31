from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category
from django.db.models import Q, Sum

def budget_dashboard(request):
    total_debit = Transaction.objects.filter(transaction_type='DEBIT').aggregate(Sum('amount'))['amount__sum'] or 0

    total_credit = Transaction.objects.filter(transaction_type='CREDIT').aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_debit - total_credit

    context = {
        'total_debit': total_debit,
        'total_credit': total_credit,
        'balance': balance,
    }

    return render(request, 'transactions/budget.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'transactions/categories.html', {'categories': categories})

def transactins_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = category.transactions.all()
    return render(request, 'transactions/by_category.html',
                  {
                      'category': category,
                      'transactions': transactions
                  })
def transaction_list(request):
    transactions = Transaction.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        transactions = transactions.filter(description__icontains=query)

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