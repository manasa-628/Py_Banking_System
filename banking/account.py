import hashlib
import random

from .config import get_connection, MAX_FAILED_PIN_ATTEMPTS

from .validators import (
    validate_pin,
    validate_holder_name,
    validate_account_type,
    validate_opening_deposit
)

from .exceptions import (
    AccountNotFoundError,
    AuthenticationError,
    AccountLockedError
)


def hash_pin(pin):
    """Convert PIN into SHA-256 hash."""
    return hashlib.sha256(
        str(pin).encode()
    ).hexdigest()


def generate_account_number():
    """Generate a 10-digit account number."""
    return str(
        random.randint(1000000000, 9999999999)
    )


def create_account(
    holder_name,
    pin,
    account_type,
    opening_deposit
):
    """Create a new bank account."""

    # Validate inputs
    validate_holder_name(holder_name)
    validate_pin(pin)
    validate_account_type(account_type)
    validate_opening_deposit(opening_deposit)

    holder_name = holder_name.strip()
    account_type = account_type.strip().upper()

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        # Generate unique account number
        while True:

            account_no = generate_account_number()

            cursor.execute(
                """
                SELECT account_no
                FROM accounts
                WHERE account_no = %s
                """,
                (account_no,)
            )

            if cursor.fetchone() is None:
                break

        # Hash PIN
        pin_hash = hash_pin(pin)

        # Insert account
        cursor.execute(
            """
            INSERT INTO accounts
            (
                account_no,
                holder_name,
                pin_hash,
                balance,
                account_type,
                status,
                failed_attempts
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                'ACTIVE',
                0
            )
            """,
            (
                account_no,
                holder_name,
                pin_hash,
                opening_deposit,
                account_type
            )
        )

        # Record opening deposit
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
            VALUES
            (
                %s,
                'DEPOSIT',
                %s,
                %s,
                'Opening deposit'
            )
            """,
            (
                account_no,
                opening_deposit,
                opening_deposit
            )
        )

        # Record audit log
        cursor.execute(
            """
            INSERT INTO audit_log
            (
                account_no,
                event_type,
                details
            )
            VALUES
            (
                %s,
                'ACCOUNT_CREATED',
                %s
            )
            """,
            (
                account_no,
                "New account created"
            )
        )

        # Save changes
        conn.commit()

        return account_no

    except Exception:

        conn.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conn.close()


def authenticate(account_no, pin):
    """Authenticate account using account number and PIN."""

    account_no = str(account_no).strip()
    pin = str(pin).strip()

    validate_pin(pin)

    conn = get_connection()
    cursor = None

    try:

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        # Account doesn't exist
        if account is None:

            raise AccountNotFoundError(
                "Account not found."
            )

        # Account locked
        if account["status"] == "LOCKED":

            raise AccountLockedError(
                "Account is locked due to multiple "
                "wrong PIN attempts."
            )

        # Account inactive
        if account["status"] == "INACTIVE":

            raise AuthenticationError(
                "Account is inactive."
            )

        # Compare entered PIN hash
        entered_hash = hash_pin(pin)

        # Correct PIN
        if entered_hash == account["pin_hash"]:

            cursor.execute(
                """
                UPDATE accounts
                SET failed_attempts = 0
                WHERE account_no = %s
                """,
                (account_no,)
            )

            # Audit successful login
            cursor.execute(
                """
                INSERT INTO audit_log
                (
                    account_no,
                    event_type,
                    details
                )
                VALUES
                (
                    %s,
                    'LOGIN_SUCCESS',
                    'Successful login'
                )
                """,
                (account_no,)
            )

            conn.commit()

            return account

        # Wrong PIN
        failed_attempts = (
            account["failed_attempts"] + 1
        )

        # Lock after 3 wrong attempts
        if failed_attempts >= MAX_FAILED_PIN_ATTEMPTS:

            cursor.execute(
                """
                UPDATE accounts
                SET
                    failed_attempts = %s,
                    status = 'LOCKED'
                WHERE account_no = %s
                """,
                (
                    failed_attempts,
                    account_no
                )
            )

            cursor.execute(
                """
                INSERT INTO audit_log
                (
                    account_no,
                    event_type,
                    details
                )
                VALUES
                (
                    %s,
                    'ACCOUNT_LOCKED',
                    'Account locked after failed PIN attempts'
                )
                """,
                (account_no,)
            )

            conn.commit()

            raise AccountLockedError(
                "Account locked after 3 wrong PIN attempts."
            )

        # Update failed attempts
        cursor.execute(
            """
            UPDATE accounts
            SET failed_attempts = %s
            WHERE account_no = %s
            """,
            (
                failed_attempts,
                account_no
            )
        )

        # Audit failed login
        cursor.execute(
            """
            INSERT INTO audit_log
            (
                account_no,
                event_type,
                details
            )
            VALUES
            (
                %s,
                'LOGIN_FAILED',
                %s
            )
            """,
            (
                account_no,
                f"Wrong PIN attempt {failed_attempts}"
            )
        )

        conn.commit()

        remaining = (
            MAX_FAILED_PIN_ATTEMPTS
            - failed_attempts
        )

        raise AuthenticationError(
            f"Incorrect PIN. "
            f"Attempts remaining: {remaining}"
        )

    except Exception:

        try:
            conn.rollback()
        except Exception:
            pass

        raise

    finally:

        if cursor:
            cursor.close()

        conn.close()