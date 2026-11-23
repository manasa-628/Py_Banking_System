from .config import get_connection

from .exceptions import (
    AccountNotFoundError
)


def get_transaction_history(
    account_no,
    limit=10,
    txn_type=None
):
    """Get recent transaction history."""

    account_no = str(account_no).strip()

    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    if limit <= 0:
        limit = 10

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        # Check account
        cursor.execute(
            """
            SELECT account_no
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        if cursor.fetchone() is None:
            raise AccountNotFoundError(
                "Account not found."
            )

        if txn_type:
            txn_type = txn_type.strip().upper()

            if txn_type not in (
                "DEPOSIT",
                "WITHDRAWAL",
                "BALANCE_CHECK"
            ):
                raise ValueError(
                    "Invalid transaction type."
                )

            query = """
                SELECT
                    txn_id,
                    txn_type,
                    amount,
                    balance_after,
                    description,
                    txn_date
                FROM transactions
                WHERE account_no = %s
                AND txn_type = %s
                ORDER BY txn_date DESC
                LIMIT %s
            """

            cursor.execute(
                query,
                (
                    account_no,
                    txn_type,
                    limit
                )
            )

        else:

            query = """
                SELECT
                    txn_id,
                    txn_type,
                    amount,
                    balance_after,
                    description,
                    txn_date
                FROM transactions
                WHERE account_no = %s
                ORDER BY txn_date DESC
                LIMIT %s
            """

            cursor.execute(
                query,
                (
                    account_no,
                    limit
                )
            )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        conn.close()


def get_account_summary(account_no):
    """Get account financial summary."""

    account_no = str(account_no).strip()

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN txn_type = 'DEPOSIT'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_deposits,

                COALESCE(
                    SUM(
                        CASE
                            WHEN txn_type = 'WITHDRAWAL'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_withdrawals,

                SUM(
                    CASE
                        WHEN txn_type = 'DEPOSIT'
                        THEN 1
                        ELSE 0
                    END
                ) AS deposit_count,

                SUM(
                    CASE
                        WHEN txn_type = 'WITHDRAWAL'
                        THEN 1
                        ELSE 0
                    END
                ) AS withdrawal_count

            FROM transactions
            WHERE account_no = %s
            """,
            (account_no,)
        )

        summary = cursor.fetchone()

        if summary is None:
            raise AccountNotFoundError(
                "Account not found."
            )

        return summary

    finally:
        if cursor:
            cursor.close()

        conn.close()