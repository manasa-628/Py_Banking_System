from datetime import date

from .config import (
    get_connection,
    DAILY_WITHDRAWAL_LIMIT
)

from .validators import validate_withdrawal

from .exceptions import (
    AccountNotFoundError,
    AccountLockedError,
    ValidationError,
    InsufficientBalanceError
)


def withdraw_money(account_no, amount):
    """Withdraw money from an account."""

    account_no = str(account_no).strip()

    if amount <= 0:
        raise ValidationError(
            "Withdrawal amount must be greater than zero."
        )

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

        current_balance = float(account["balance"])

        # Validate minimum withdrawal
        validate_withdrawal(
            amount,
            current_balance
        )

        # Get today's withdrawal total
        today = date.today()

        cursor.execute(
            """
            SELECT total_withdrawn
            FROM daily_withdrawal_limits
            WHERE account_no = %s
            AND limit_date = %s
            FOR UPDATE
            """,
            (
                account_no,
                today
            )
        )

        daily_record = cursor.fetchone()

        if daily_record:
            already_withdrawn = float(
                daily_record["total_withdrawn"]
            )
        else:
            already_withdrawn = 0.0

        # Check daily limit
        if (
            already_withdrawn + amount
            > DAILY_WITHDRAWAL_LIMIT
        ):
            raise ValidationError(
                f"Daily withdrawal limit is "
                f"₹{DAILY_WITHDRAWAL_LIMIT}."
            )

        # Check balance
        if amount > current_balance:
            raise InsufficientBalanceError(
                "Insufficient balance."
            )

        new_balance = (
            current_balance - amount
        )

        # Update account balance
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

        # Update or create daily tracker
        if daily_record:

            new_daily_total = (
                already_withdrawn + amount
            )

            cursor.execute(
                """
                UPDATE daily_withdrawal_limits
                SET total_withdrawn = %s
                WHERE account_no = %s
                AND limit_date = %s
                """,
                (
                    new_daily_total,
                    account_no,
                    today
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO daily_withdrawal_limits
                (
                    account_no,
                    limit_date,
                    total_withdrawn
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    account_no,
                    today,
                    amount
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
                'WITHDRAWAL',
                %s,
                %s,
                'Cash withdrawal'
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
                'WITHDRAWAL',
                %s
            )
            """,
            (
                account_no,
                f"Withdrawn ₹{amount:.2f}"
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