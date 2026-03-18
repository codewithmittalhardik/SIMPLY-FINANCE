import pandas as pd
from ledger.models import JournalEntry
from django.db.models import F

def get_insights_dataframe():
    # Fetch data using the exact field names from your models
    data = JournalEntry.objects.annotate(
        date=F('transaction__date'),
        account_name=F('account__name'),
        category=F('account__account_type')
    ).values('date', 'account_name', 'category', 'debit', 'credit')

    df = pd.DataFrame(list(data))

    # Fix: If the database is empty, create an empty DF with the right columns
    if df.empty:
        return pd.DataFrame(columns=['date', 'account_name', 'category', 'debit', 'credit', 'amount'])

    # Ensure numeric types (Decimal objects from Django can break Pandas math)
    df['debit'] = pd.to_numeric(df['debit'], errors='coerce').fillna(0)
    df['credit'] = pd.to_numeric(df['credit'], errors='coerce').fillna(0)
    
    # Calculate Net Amount
    df['amount'] = df['debit'] - df['credit']
    df['date'] = pd.to_datetime(df['date'])
    
    return df