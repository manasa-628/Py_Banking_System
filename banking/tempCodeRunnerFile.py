def display_account(account):
    """Display account details."""

    print("\n========== ACCOUNT DETAILS ==========")
    print(f"Account Number : {account['account_no']}")
    print(f"Holder Name    : {account['holder_name']}")
    print(f"Balance        : ₹{account['balance']}")
    print(f"Account Type   : {account['account_type']}")
    print(f"Status         : {account['status']}")
    print("=====================================\n")


def display_transaction(transaction):
    """Display one transaction."""

    print("-------------------------------------")
    print(f"Transaction ID : {transaction['txn_id']}")
    print(f"Type           : {transaction['txn_type']}")
    print(f"Amount         : ₹{transaction['amount']}")
    print(f"Balance After  : ₹{transaction['balance_after']}")
    print(f"Description    : {transaction['description']}")
    print(f"Date           : {transaction['txn_date']}")
    print("-------------------------------------")


def display_transactions(transactions):
    """Display multiple transactions."""

    print("\n========== TRANSACTION HISTORY ==========")

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)

    print("=========================================\n")


def display_summary(summary):
    """Display transaction summary."""

    print("\n========== TRANSACTION SUMMARY ==========")
    print(
        f"Total Deposits    : ₹{summary['total_deposits']}"
    )
    print(
        f"Total Withdrawals : ₹{summary['total_withdrawals']}"
    )
    print("=========================================\n")


def display_message(message):
    """Display a normal message."""

    print(f"\n{message}\n")


def display_error(message):
    """Display an error message."""

    print(f"\nERROR: {message}\n")


