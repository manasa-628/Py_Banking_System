from .config import get_connection

from .validators import validate_deposit

from .exceptions import (
    AccountNotFoundError,
    AccountLockedError,
    ValidationError
)


def deposit_money(account_no, amount):
    """Deposit money into an account."""

    account_no = str(account_no).strip()

    if amount <= 0:
        raise ValidationError(
            "Deposit amount must be greater than zero."
        )

    validate_deposit(amount)

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        # Lock account row
        cursor.execute(
            """
            SELECT account_no, balance, status
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        if account is None:
            raise AccountNotFoundError(
                "Account not found."
            )

        if account["status"] == "LOCKED":
            raise AccountLockedError(
                "Account is locked."
            )

        if account["status"] == "INACTIVE":
            raise ValidationError(
                "Account is inactive."
            )

        new_balance = (
            float(account["balance"]) + amount
        )

        # Update balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_balance,
                account_no
            )
        )

        # Record transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_no,
                txn_type,
                amount,
                balance_after,
                description
            )
            VALUES (
                %s,
                'DEPOSIT',
                %s,
                %s,
                'Cash deposit'
            )
            """,
            (
                account_no,
                amount,
                new_balance
            )
        )

        # Audit log
        cursor.execute(
            """
            INSERT INTO audit_log
            (
                account_no,
                event_type,
                details
            )
            VALUES (
                %s,
                'DEPOSIT',
                %s
            )
            """,
            (
                account_no,
                f"Deposited ₹{amount:.2f}"
            )
        )

        conn.commit()

        return new_balance

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        conn.close()