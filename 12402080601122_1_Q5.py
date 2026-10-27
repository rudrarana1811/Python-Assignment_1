class BankError(Exception):
    pass


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.history = []

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount <= 0:
            raise BankError("Invalid amount")

        self.balance += amount
        self.history.append(("DEPOSIT", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise BankError("Invalid amount")

        if amount > self.balance:
            raise BankError("Insufficient balance")

        self.balance -= amount
        self.history.append(("WITHDRAW", amount))


class Transaction:
    def __init__(self, kind, account_from, account_to, amount):
        self.kind = kind
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount


class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def deposit(self, account_id, amount):
        if account_id not in self.accounts:
            raise BankError("Account not found")

        self.accounts[account_id].deposit(amount)

    def withdraw(self, account_id, amount):
        if account_id not in self.accounts:
            raise BankError("Account not found")

        self.accounts[account_id].withdraw(amount)

    def transfer(self, source, target, amount):
        if source not in self.accounts or target not in self.accounts:
            raise BankError("Account not found")

        self.accounts[source].withdraw(amount)
        self.accounts[target].deposit(amount)

    def apply_transaction(self, transaction):
        if transaction.kind == "DEPOSIT":
            self.deposit(
                transaction.account_from,
                transaction.amount
            )

        elif transaction.kind == "WITHDRAW":
            self.withdraw(
                transaction.account_from,
                transaction.amount
            )

        else:
            self.transfer(
                transaction.account_from,
                transaction.account_to,
                transaction.amount
            )

# Convert the input operation into a transaction object
def make_transaction(parts):
    if parts[0] == "DEPOSIT":
        return Transaction(
            "DEPOSIT",
            parts[1],
            None,
            int(parts[2])
        )

    if parts[0] == "WITHDRAW":
        return Transaction(
            "WITHDRAW",
            parts[1],
            None,
            int(parts[2])
        )

    if parts[0] == "TRANSFER":
        return Transaction(
            "TRANSFER",
            parts[1],
            parts[2],
            int(parts[3])
        )

    raise BankError("Invalid operation")


def run_batch(bank, transactions):
    old_balances = {
        account_id: account.get_balance()
        for account_id, account in bank.accounts.items()
    }

    try:
        for transaction in transactions:
            bank.apply_transaction(transaction)

    except BankError:
        for account_id, balance in old_balances.items():
            bank.accounts[account_id].balance = balance

        return False

    return True


print("Object-Oriented Bank Settlement System")
print("Enter number of accounts:")
n = int(input())

bank = Bank()

print("Enter account id and initial balance:")

for i in range(n):
    print(f"Account {i + 1}:")
    account_id, balance = input().split()
    bank.add_account(Account(account_id, int(balance)))

print("Enter number of operations:")
q = int(input())

batch = None
batch_number = 0
failed_batches = []

print("Enter operations:")

for i in range(q):
    print(f"Operation {i + 1}:")
    parts = input().split()

    if parts[0] == "BATCH_BEGIN":
        batch_number += 1
        batch = []
        continue

    if parts[0] == "BATCH_END":
        if batch is None:
            print("Invalid batch")
            continue

        if not run_batch(bank, batch):
            failed_batches.append(batch_number)

        batch = None
        continue

    try:
        transaction = make_transaction(parts)

        if batch is not None:
            batch.append(transaction)
        else:
            bank.apply_transaction(transaction)

    except BankError:
        if batch is not None:
            batch.append(
                Transaction(
                    "WITHDRAW",
                    "__INVALID__",
                    None,
                    0
                )
            )
        else:
            pass

print()

for number in failed_batches:
    print("FAILED", number)

for account_id in sorted(bank.accounts):
    print(account_id, bank.accounts[account_id].get_balance())
