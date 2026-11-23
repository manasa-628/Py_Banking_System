from banking.db_setup import initialize_database

from banking.account import create_account, authenticate

from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance

from banking.history import (
    get_transaction_history,
    get_account_summary
)

from banking.display import (
    display_account,
    display_transactions,
    display_summary
)

from banking.exceptions import BankingError


# =========================================================
# CREATE NEW ACCOUNT
# =========================================================

def create_new_account():

    print("\n========== CREATE ACCOUNT ==========")

    holder_name = input("Enter holder name: ").strip()

    # Normal input is used so you can see and enter the PIN
    pin = input("Enter 4-digit PIN: ").strip()

    confirm_pin = input("Confirm 4-digit PIN: ").strip()

    if pin != confirm_pin:
        print("ERROR: PINs do not match.")
        return

    account_type = input(
        "Enter account type (SAVINGS/CURRENT): "
    ).strip()

    try:

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

    except ValueError:
        print("ERROR: Please enter a valid amount.")

    except BankingError as exc:
        print(f"ERROR: {exc}")

    except Exception as exc:
        print(f"ERROR: {exc}")


# =========================================================
# LOGIN
# =========================================================

def login():

    print("\n========== LOGIN ==========")

    account_no = input(
        "Enter account number: "
    ).strip()

    # Normal input so PIN can be entered in VS Code terminal
    pin = input(
        "Enter PIN: "
    ).strip()

    try:

        account = authenticate(
            account_no,
            pin
        )

        print(
            f"\nWelcome, {account['holder_name']}!"
        )

        account_menu(account_no)

    except BankingError as exc:

        print(f"\nERROR: {exc}")

    except Exception as exc:

        print(f"\nERROR: {exc}")


# =========================================================
# ACCOUNT MENU
# =========================================================

def account_menu(account_no):

    while True:

        print("\n====================================")
        print("           ACCOUNT MENU")
        print("====================================")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Account Summary")
        print("6. Logout")
        print("====================================")

        choice = input(
            "Enter your choice: "
        ).strip()

        try:

            # -------------------------------------------------
            # DEPOSIT
            # -------------------------------------------------

            if choice == "1":

                amount = float(
                    input(
                        "Enter deposit amount: ₹"
                    )
                )

                new_balance = deposit_money(
                    account_no,
                    amount
                )

                print("\nDeposit successful!")

                print(
                    f"New Balance: ₹{new_balance:.2f}"
                )

                print("\n---------- RECEIPT ----------")
                print("Transaction : DEPOSIT")
                print(f"Account     : {account_no}")
                print(f"Amount      : ₹{amount:.2f}")
                print(
                    f"Balance     : ₹{new_balance:.2f}"
                )
                print("------------------------------")


            # -------------------------------------------------
            # WITHDRAW
            # -------------------------------------------------

            elif choice == "2":

                amount = float(
                    input(
                        "Enter withdrawal amount: ₹"
                    )
                )

                new_balance = withdraw_money(
                    account_no,
                    amount
                )

                print("\nWithdrawal successful!")

                print(
                    f"New Balance: ₹{new_balance:.2f}"
                )

                print("\n---------- RECEIPT ----------")
                print("Transaction : WITHDRAWAL")
                print(f"Account     : {account_no}")
                print(f"Amount      : ₹{amount:.2f}")
                print(
                    f"Balance     : ₹{new_balance:.2f}"
                )
                print("------------------------------")


            # -------------------------------------------------
            # CHECK BALANCE
            # -------------------------------------------------

            elif choice == "3":

                account = check_balance(
                    account_no
                )

                display_account(account)


            # -------------------------------------------------
            # TRANSACTION HISTORY
            # -------------------------------------------------

            elif choice == "4":

                print("\nTransaction Type:")
                print("1. All")
                print("2. Deposit")
                print("3. Withdrawal")
                print("4. Balance Check")

                type_choice = input(
                    "Choose type: "
                ).strip()

                txn_type = None

                if type_choice == "2":

                    txn_type = "DEPOSIT"

                elif type_choice == "3":

                    txn_type = "WITHDRAWAL"

                elif type_choice == "4":

                    txn_type = "BALANCE_CHECK"

                elif type_choice != "1":

                    print(
                        "Invalid transaction type."
                    )

                    continue

                limit_input = input(
                    "How many transactions? "
                    "(default 10): "
                ).strip()

                if limit_input:

                    limit = int(limit_input)

                else:

                    limit = 10

                transactions = get_transaction_history(
                    account_no,
                    limit,
                    txn_type
                )

                display_transactions(
                    transactions
                )


            # -------------------------------------------------
            # ACCOUNT SUMMARY
            # -------------------------------------------------

            elif choice == "5":

                summary = get_account_summary(
                    account_no
                )

                display_summary(summary)


            # -------------------------------------------------
            # LOGOUT
            # -------------------------------------------------

            elif choice == "6":

                print(
                    "\nLogged out successfully."
                )

                break


            # -------------------------------------------------
            # INVALID CHOICE
            # -------------------------------------------------

            else:

                print(
                    "Invalid choice. "
                    "Please select 1-6."
                )


        except ValueError:

            print(
                "ERROR: Please enter a valid number."
            )

        except BankingError as exc:

            print(f"ERROR: {exc}")

        except Exception as exc:

            print(f"ERROR: {exc}")


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    try:

        initialize_database()

    except Exception as exc:

        print(
            "\nDatabase initialization failed."
        )

        print(f"ERROR: {exc}")

        return


    while True:

        print("\n====================================")
        print("        PYBANK BANKING SYSTEM")
        print("====================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("====================================")

        choice = input(
            "Enter your choice: "
        ).strip()


        if choice == "1":

            create_new_account()


        elif choice == "2":

            login()


        elif choice == "3":

            print(
                "\nThank you for using PyBank!"
            )

            break


        else:

            print(
                "Invalid choice. "
                "Please select 1-3."
            )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    main()