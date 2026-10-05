
## BankError(Exception) — общий предок для всех ошибок банка;
## InvalidAmountError, InsufficientFundsError, EmailAlreadyExistsError — его наследники.
from contextlib import contextmanager

class BankError(Exception):
    pass

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class EmailAlreadyExistsError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass


class BankAccount: ## Чертеж счета
    
    def __init__(self, account_id, owner_email, balance=0):
        self.account_id = account_id
        self.owner_email = owner_email
        self._balance = balance

    def deposit(self, amount): #  def deposit(self, amount: float):
        if amount <= 0:
            raise  InvalidAmountError("Amount must be positive")
        self._balance += amount
        return True
        
    def withdraw(self, amount): # def withdraw(self, amount: float):   
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds in the account")
        self._balance -= amount
        return True

    def get_balance(self):
        return self._balance

class Bank: # счертеж банка
    def __init__(self):
        self.accounts = {}
        self.emails = set()
        self._next_id = 1          # некст свободный id

    def open_account(self, owner_email):
        if owner_email in self.emails:
            raise EmailAlreadyExistsError("Email booked")         
        account_id = self._next_id
        self._next_id += 1
        account = BankAccount(account_id, owner_email)
        self.accounts[account_id] = account
        self.emails.add(owner_email)
        return account
    
    def transfer(self, from_id, to_id, amount):
        with atomic(self):
            if from_id not in self.accounts:
                raise AccountNotFoundError
            sender = self.accounts[from_id]
            sender.withdraw(amount)
            if to_id not in self.accounts:
                raise AccountNotFoundError("Account not found")
            recipient = self.accounts[to_id]
            recipient.deposit(amount)



@contextmanager
def atomic(bank):
    #снимок для каждого счёта запоминаем баланс
    snapshot = {}
    for acc_id, acc in bank.accounts.items():
        snapshot[acc_id] = acc._balance

    try:
        yield                                  # тут выполняется блок with
    except Exception:
        # 3. упало - возвращаем всем счетам старые балансы
        for acc_id, old_balance in snapshot.items():
            bank.accounts[acc_id]._balance = old_balance
        raise                                  # сообщаем об ошибке выше
        







bank = Bank()
a = bank.open_account("a@b.com")
print(a.account_id)                    # 1
try:
    bank.open_account("a@b.com")
except EmailAlreadyExistsError as e:
    print("ошибка:", e)    # None -> почта занята
a.deposit(100)
print(a.withdraw(30), a.get_balance()) # True 70
try:
    bank.transfer(a.account_id, 999, 50)
except AccountNotFoundError as e:
    print("ошибка:", type(e).__name__)
print(a.get_balance())   # 70