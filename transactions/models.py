from django.db import models

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

    def __str__(self):
        return f"{self.desc} ({self.amount})"