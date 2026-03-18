# ledger/views.py
from django.shortcuts import render

def ledger_home(request):
    # This will look for: ledger/templates/ledger/ledger.html
    return render(request, 'ledger/ledger.html')