from model.model import *
from pattern.text.en import singularize


class Accounts:
    def __init__(self, transactions):
        self.owner = ''
        self.transactions = transactions
        self.account_names = ['cash']
        self.get_account_names()
        self.records = dict()
        self.bal_state = []
        self.make_records_on_tables()
        self.calculate_balance()

    def get_account_names(self):
        key_words = ['capital', 'bank', 'good', 'equipment', 'salary', 'commission', 'furniture', 'rent', 'telephone',
                     'electricity', 'water', 'chair', 'sale', 'BOC']

        for d in self.transactions:
            nouns = extract_nouns(d)
            nouns = [singularize(noun) for noun in nouns]
            print(nouns)

            if 'capital' in nouns:  # for capital account
                if 'capital' not in self.account_names:
                    self.account_names.append('capital')
                who = [noun for noun in nouns if noun[0].isupper()][0]
                self.account_names.append(who)
                if not self.owner:
                    self.owner = who

            elif len(nouns) == 1:
                if nouns[0] not in self.account_names:
                    self.account_names.append(nouns[0])

            else:
                nouns.reverse()
                for noun in nouns:
                    if noun in key_words:
                        self.account_names.append(noun)
                        break
                    else:
                        if noun[0].isupper() and noun not in self.account_names:
                            self.account_names.append(noun)
                            break
                else:
                    if 'unknown' not in self.account_names:
                        self.account_names.append("unknown")

    def make_records_on_tables(self):
        self.account_names.sort(reverse=True)
        print(self.account_names)

        for account_name in self.account_names:
            self.records[account_name] = []

        for i, transaction in enumerate(self.transactions):
            pred = predict(transaction)
            nouns = extract_nouns(transaction)
            nouns = [singularize(noun) for noun in nouns]
            phrase = ' '.join(nouns)
            nouns.sort(reverse=True)
            amount = extract_amount(transaction)[0]

            # ['as', 'eq', 'ex', 'in', 'li']
            if pred in ['as', 'ex']:  # credit side
                for noun in nouns:
                    if (noun in self.account_names) and (noun != 'cash'):
                        self.records[noun].append([phrase, amount, '', ''])
                        break

                if 'capital' in nouns:
                    self.records['capital'].append(['', '', phrase, amount])
                else:
                    self.records['cash'].append(['', '', phrase, amount])

            else:  # debit side
                if 'capital' in nouns:  # for capital account
                    who = [noun for noun in nouns if noun[0].isupper()][0]
                    self.records[who].append([phrase, amount, '', ''])
                    self.records['capital'].append(['', '', phrase, amount])

                else:
                    for noun in nouns:
                        if (noun in self.account_names) and (noun != 'cash'):
                            self.records[noun].append(['', '', phrase, amount])
                            self.records['cash'].append([phrase, amount, '', ''])
                            break

    def calculate_balance(self):

        parse = lambda x: 0 if x == '' else int(x)
        credit_side = []
        debit_side = []

        for key, value in self.records.items():
            left_bal, right_bal = 0, 0
            for v in value:
                left_bal += parse(v[1])
                right_bal += parse(v[3])

            diff_bal = left_bal - right_bal

            if diff_bal > 0:
                # low in debit side
                # goes to credit side on balance statement
                self.bal_state.append([key, abs(diff_bal), ''])
                credit_side.append(abs(diff_bal))

            elif diff_bal < 0:
                # low in credit side
                # goes to debit side on balance statement
                self.bal_state.append([key, '', abs(diff_bal)])
                debit_side.append(abs(diff_bal))

        credit_balance = sum(credit_side)
        debit_balance = sum(debit_side)

        self.bal_state.append(['*** balance ***', credit_balance, debit_balance])
