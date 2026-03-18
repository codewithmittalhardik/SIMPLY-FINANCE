from django.db import models

class Account(models.Model):
    # e.g., "Cash", "Rent Expense", "Sales Revenue"
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50) # Asset, Liability, Equity, Revenue, Expense
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    # This groups the debit and credit together
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.date.date()} - {self.description}"

class JournalEntry(models.Model):
    # The actual line items (The "Double" in Double-Entry)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}: D{self.debit} C{self.credit}"