import csv
from collections import defaultdict
from datetime import datetime


def process_file(filename):
    balances = defaultdict(float)

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_fields = {"tid", "acc", "type", "amount", "time"}

        if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
            raise ValueError("Invalid CSV header")
        # Create separate files for valid credits, debits and errors

        with open(
            "credit.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as credit_file, open(
            "debit.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as debit_file, open(
            "error.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as error_file:

            credit_writer = csv.DictWriter(
                credit_file,
                fieldnames=reader.fieldnames
            )

            debit_writer = csv.DictWriter(
                debit_file,
                fieldnames=reader.fieldnames
            )

            error_writer = csv.writer(error_file)

            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writerow(
                reader.fieldnames + ["reason"]
            )

            # Validate each transaction separately

            for row in reader:
                try:
                    if not row.get("tid") or not row.get("acc"):
                        raise ValueError("missing transaction or account id")

                    if row.get("type") not in ("CREDIT", "DEBIT"):
                        raise ValueError("invalid transaction type")

                    amount = float(row["amount"])

                    if amount <= 0:
                        raise ValueError("amount must be greater than zero")

                    datetime.strptime(
                        row["time"],
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    if row["type"] == "CREDIT":
                        credit_writer.writerow(row)
                        balances[row["acc"]] += amount
                    else:
                        debit_writer.writerow(row)
                        balances[row["acc"]] -= amount

                except Exception as error:
                    error_writer.writerow(
                        list(row.values()) + [str(error)]
                    )

    return balances


print("Exception-Safe CSV Transaction Splitter")
print("Enter input CSV file path:")
filename = input().strip()

try:
    balances = process_file(filename)

except Exception as error:
    print(error)
    raise SystemExit

print()
print("Account-wise balance changes:")

for account, balance in sorted(
    balances.items(),
    key=lambda item: (-abs(item[1]), item[0])
):
    if balance.is_integer():
        balance = int(balance)

    print(account, balance)

print("Files created: credit.csv, debit.csv, error.csv")
