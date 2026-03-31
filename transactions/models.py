from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Назва категорії"
    )

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEBIT', 'Дебет'),
        ('CREDIT', 'Кредит')
    ]
    desc = models.TextField(
        max_length=500,
        verbose_name="Опис"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сума"
    )
    transaction_type = models.CharField(
        max_length=6,
        choices=TRANSACTION_TYPES,
        default='DEBIT',
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Категорія",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.desc} ({self.amount})"