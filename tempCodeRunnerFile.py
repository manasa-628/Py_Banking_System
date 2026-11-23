from banking.db_setup import initialize_database
from banking.account import create_account, authenticate
from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance
from banking.history import (
    get_transaction_history,
    get_transaction_summary
)
from banking.display import (
    display_account,
    display_transactions,
    display_summary,
    display_message,
    display_error
)

from banking.exceptions import BankingError


def create_new_account():
    """Create a new bank account."""

    print("\n========== CREATE ACCOUNT ==========")

    try:
        holder_name = input("Enter holder name: ")
        pin = input("Enter 4-digit PIN: ")
        account_type = input(
            "Enter account type (SAVINGS/CURRENT): "
        )
        opening_deposit = float(
            input("Enter opening deposit: ")
        )

        account_no = create_account(
            holder_name,
            pin,
            account_type,
            opening_deposit
        )

        print("\nAccount created successfully!")
        print(f"Your Account Number is: {account_no}")

    except BankingError as error:
        display_error(str(error))

    except ValueError:
        display_error(
            "Please enter a valid amount."
        )


def login():
    """Login to a bank account."""

    print("\n========== LOGIN ==========")

    account_no = input("Enter account number: ")
    pin = input("Enter PIN: ")

    try:
        authenticate(account_no, pin)

        print("\nLogin successful!")

        return account_no

    except BankingError as error:
        display_error(str(error))
        return None


def deposit_menu(account_no):
    """Deposit money."""

    print("\n========== DEPOSIT ==========")

    try:
        amount = float(
            input("Enter deposit amount: ")
        )

        new_balance = deposit_money(
            account_no,
            amount
        )

        print("\nDeposit successful!")
        print(f"New Balance: ₹{new_balance}")

    except BankingError as error:
        display_error(str(error))

    except ValueError:
        display_error(
            "Please enter a valid amount."
        )


def withdraw_menu(account_no):
    """Withdraw money."""

    print("\n========== WITHDRAW ==========")

    try:
        amount = float(
            input("Enter withdrawal amount: ")
        )

        new_balance = withdraw_money(
            account_no,
            amount
        )

        print("\nWithdrawal successful!")
        print(f"New Balance: ₹{new_balance}")

    except BankingError as error:
        display_error(str(error))

    except ValueError:
        display_error(
            "Please enter a valid amount."
        )


def balance_menu(account_no):
    """Show account balance."""

    try:
        account = check_balance(account_no)

        display_account(account)

    except BankingError as error:
        display_error(str(error))


def history_menu(account_no):
    """Show transaction history."""

    try:
        transactions = get_transaction_history(
            account_no,
            10
        )

        display_transactions(transactions)

    except BankingError as error:
        display_error(str(error))


def summary_menu(account_no):
    """Show transaction summary."""

    try:
        summary = get_transaction_summary(
            account_no
        )

        display_summary(summary)

    except BankingError as error:
        display_error(str(error))


def account_menu(account_no):
    """Display menu after login."""

    while True:

        print("\n========== ACCOUNT MENU ==========")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Transaction Summary")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            deposit_menu(account_no)

        elif choice == "2":
            withdraw_menu(account_no)

        elif choice == "3":
            balance_menu(account_no)

        elif choice == "4":
            history_menu(account_no)

        elif choice == "5":
            summary_menu(account_no)

        elif choice == "6":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice. Please try again.")


def main():
    """Main banking application."""

    try:
        # Initialize database and tables
        initialize_database()

    except Exception as error:
        print(f"\nDatabase setup error: {error}")
        return

    while True:

        print("\n")
        print("====================================")
        print("       PYBANK BANKING SYSTEM")
        print("====================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_new_account()

        elif choice == "2":
            account_no = login()

            if account_no:
                account_menu(account_no)

        elif choice == "3":
            print("\nThank you for using PyBank!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()