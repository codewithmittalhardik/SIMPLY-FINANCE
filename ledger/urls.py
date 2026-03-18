# ledger/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ledger_home, name='ledger_home'),
]