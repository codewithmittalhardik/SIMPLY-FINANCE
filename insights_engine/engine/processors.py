import pandas as pd
from ledger.models import JournalEntry
from django.db.models import F

def get_insights_dataframe():
    # 1. Fetch data with related names (Joins)
    # We use F() expressions to pull the related fields directly
    data = JournalEntry.objects.annotate(
        date=F('transaction__date'),
        account_name=F('account__name'),
        category=F('account__account_type')
    ).values('date', 'account_name', 'category', 'debit', 'credit')

    df = pd.DataFrame(list(data))

    if not df.empty:
        # Convert to proper types
        df['date'] = pd.to_datetime(df['date'])
        df['debit'] = df['debit'].astype(float)
        df['credit'] = df['credit'].astype(float)
        
        # Add a 'Net' column for easier plotting
        df['amount'] = df['debit'] - df['credit']
        
        # Sort by date
        df = df.sort_values('date')
        
    return df