from django.shortcuts import render
from .forms import TransactionsForm
from model.rules import *
from model.printer import *
from django.http import FileResponse


accounts = None

def index(request):
    global accounts
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['transactions']
            transactions = data.split('\r\n')
            print(transactions)
            accounts = Accounts(transactions)

            return render(request, 'index.html', context={'form': form,
                                                          'records': accounts.records,
                                                          'visibility': True,
                                                          'balstate': accounts.bal_state,
                                                          })
    else:
        form = TransactionsForm()
    return render(request, 'index.html', context={'form': form,
                                                  'records': range(0),
                                                  'visibility': False,
                                                  'balstate': range(0),
                                                  })


def printme(request):
    buf = printLedger(accounts)
    return FileResponse(buf, as_attachment=True, filename='ledger.pdf')


def thank_you(request):
    return render(request, 'thank_you.html')