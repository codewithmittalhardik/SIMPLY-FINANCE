from django.shortcuts import render
from .engine.processors import get_insights_dataframe
import json

def dashboard(request):
    df = get_insights_dataframe()
    
    # Calculate some quick stats for the dashboard cards
    total_spent = df[df['debit'] > 0]['debit'].sum()
    total_income = df[df['credit'] > 0]['credit'].sum()
    
    # Prepare data for a simple Chart.js/Plotly bar chart
    # Total spent per category
    category_summary = df[df['category'] == 'Expense'].groupby('account_name')['debit'].sum().to_dict()

    context = {
        'total_spent': f"{total_spent:,.2f}",
        'total_income': f"{total_income:,.2f}",
        'category_data': json.dumps(category_summary),
    }
    return render(request, 'insights_engine/dashboard.html', context)