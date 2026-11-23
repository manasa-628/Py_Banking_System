def display_account(account):
    """Display account information."""

    print("\n========== ACCOUNT DETAILS ==========")

    print(
        f"Account Number : {account['account_no']}"
    )

    print(
        f"Holder Name    : {account['holder_name']}"
    )

    print(
        f"Account Type   : {account['account_type']}"
    )

    print(
        f"Balance        : ₹{float(account['balance']):.2f}"
    )

    print(
        f"Status         : {account['status']}"
    )

    print("======================================")


def display_transactions(transactions):
    """Display transaction history."""

    print("\n========== TRANSACTION HISTORY ==========")

    if not transactions:
        print("No transactions found.")
        return

    for txn in transactions:

        amount = txn["amount"]

        if amount is None:
            amount_text = "-"
        else:
            amount_text = f"₹{float(amount):.2f}"

        print(
            f"\nTransaction ID : {txn['txn_id']}"
        )

        print(
            f"Type           : {txn['txn_type']}"
        )

        print(
            f"Amount         : {amount_text}"
        )

        print(
            f"Balance After  : "
            f"₹{float(txn['balance_after']):.2f}"
        )

        print(
            f"Description    : {txn['description']}"
        )

        print(
            f"Date           : {txn['txn_date']}"
        )

    print("==========================================")


def display_summary(summary):
    """Display account summary."""

    print("\n========== ACCOUNT SUMMARY ==========")

    print(
        f"Total Deposits    : "
        f"₹{float(summary['total_deposits']):.2f}"
    )

    print(
        f"Total Withdrawals : "
        f"₹{float(summary['total_withdrawals']):.2f}"
    )

    print(
        f"Deposit Count     : {summary['deposit_count']}"
    )

    print(
        f"Withdrawal Count  : "
        f"{summary['withdrawal_count']}"
    )

    print("======================================")