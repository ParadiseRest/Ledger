from django.urls import path
from Ledger import views

app_name = 'Ledger'

urlpatterns = [
    path('', views.index, name='index'),
    path('printme/', views.printme, name='printme'),
    path('thank_you/', views.thank_you, name='thank_you'),
]

