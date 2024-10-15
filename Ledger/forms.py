from django import forms

class TransactionsForm(forms.Form):
    transactions = forms.CharField(widget=forms.Textarea(attrs={"rows":"10", "cols":"200"}), label='')