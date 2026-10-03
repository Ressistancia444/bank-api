
## BankError(Exception) — общий предок для всех ошибок банка;
## InvalidAmountError, InsufficientFundsError, EmailAlreadyExistsError — его наследники.





class BankAccount: ## Чертеж счета
    
    def __init__(self, account_id, owner_email, balance=0):
        self.account_id = account_id
        self.owner_email = owner_email
        self._balance = balance

    def deposit(self, amount): #  def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("wrong amount")
        self._balance += amount
        return True
        
    def withdraw(self, amount): # def withdraw(self, amount: float):   
        if amount <= 0 or amount > self._balance:
            raise ValueError("wrong amount")
        self._balance = self._balance - amount
        return True

    def get_balance(self):
        return self._balance

class Bank: # счертеж банка
    def __init__(self):
        self.accounts = {}
        self.emails = set()
        self._next_id = 1          # следующий свободный id

    def open_account(self, owner_email):
        if owner_email in self.emails:
            raise ValueError("Email booked")         
        account_id = self._next_id
        self._next_id += 1
        account = BankAccount(account_id, owner_email)
        self.accounts[account_id] = account
        self.emails.add(owner_email)
        return account
        
        



bank = Bank()
a = bank.open_account("a@b.com")
print(a.account_id)                    # 1
try:
    bank.open_account("a@b.com")
except ValueError as e:
    print("ошибка:", e)    # None -> почта занята
a.deposit(100)
print(a.withdraw(30), a.get_balance()) # True 70