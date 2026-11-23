from .config import get_connection

from .exceptions import (
    AccountNotFoundError,
    AccountLockedError,
    ValidationError
)


def check_balance(account_no):
    """Check current account balance."""

    account_no = str(account_no).strip()

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                account_no,
                holder_name,
                balance,
                account_type,
                status
            FROM accounts
            WHERE account_no = %s
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

        # Log balance check
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
                'BALANCE_CHECK',
                NULL,
                %s,
                'Balance enquiry'
            )
            """,
            (
                account_no,
                account["balance"]
            )
        )

        # Audit
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
                'BALANCE_CHECK',
                'Balance checked'
            )
            """,
            (account_no,)
        )

        conn.commit()

        return account

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        conn.close()