import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ledger.models import Account, Transaction, JournalEntry

def seed():
    print("Seeding data...")
    # 1. Setup Accounts
    cash, _ = Account.objects.get_or_create(name="Cash", account_type="Asset")
    salary_inc, _ = Account.objects.get_or_create(name="Salary", account_type="Income")
    rent_exp, _ = Account.objects.get_or_create(name="Rent", account_type="Expense")
    food_exp, _ = Account.objects.get_or_create(name="Food", account_type="Expense")
    misc_exp, _ = Account.objects.get_or_create(name="Misc", account_type="Expense")

    # 2. Add a Salary (Income)
    tx_sal = Transaction.objects.create(description="Monthly Salary")
    JournalEntry.objects.create(transaction=tx_sal, account=cash, debit=5000.00)
    JournalEntry.objects.create(transaction=tx_sal, account=salary_inc, credit=5000.00)

    # 3. Add 30 days of random expenses
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        
        # Daily Coffee/Misc
        tx = Transaction.objects.create(description=f"Misc Expense Day {i}")
        tx.date = date # Overwrite auto_now_add for historical data
        tx.save()
        
        amt = random.uniform(5.00, 45.00)
        JournalEntry.objects.create(transaction=tx, account=misc_exp, debit=amt)
        JournalEntry.objects.create(transaction=tx, account=cash, credit=amt)

    print("Success: 30 days of data seeded!")

if __name__ == "__main__":
    seed()