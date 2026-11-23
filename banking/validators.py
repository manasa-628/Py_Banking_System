from .config import (
    MIN_DEPOSIT,
    MAX_DEPOSIT,
    MIN_WITHDRAWAL,
    MIN_BALANCE,
    PIN_LENGTH,
    MIN_OPENING_DEPOSIT
)

from .exceptions import ValidationError


def validate_pin(pin):
    """Validate PIN."""

    pin = str(pin).strip()

    if not pin.isdigit():
        raise ValidationError(
            "PIN must contain only digits."
        )

    if len(pin) != PIN_LENGTH:
        raise ValidationError(
            f"PIN must be exactly {PIN_LENGTH} digits."
        )

    return True


def validate_holder_name(name):
    """Validate account holder name."""

    name = name.strip()

    if not name:
        raise ValidationError(
            "Holder name cannot be empty."
        )

    if not name.replace(" ", "").isalpha():
        raise ValidationError(
            "Holder name must contain only letters."
        )

    return True


def validate_account_type(account_type):
    """Validate account type."""

    account_type = account_type.strip().upper()

    if account_type not in ("SAVINGS", "CURRENT"):
        raise ValidationError(
            "Account type must be SAVINGS or CURRENT."
        )

    return True


def validate_opening_deposit(amount):
    """Validate opening deposit."""

    if amount < MIN_OPENING_DEPOSIT:
        raise ValidationError(
            f"Opening deposit must be at least "
            f"₹{MIN_OPENING_DEPOSIT}."
        )

    return True


def validate_deposit(amount):
    """Validate deposit amount."""

    if amount < MIN_DEPOSIT:
        raise ValidationError(
            f"Minimum deposit is ₹{MIN_DEPOSIT}."
        )

    if amount > MAX_DEPOSIT:
        raise ValidationError(
            f"Maximum deposit is ₹{MAX_DEPOSIT}."
        )

    return True


def validate_withdrawal(amount, current_balance):
    """Validate withdrawal amount."""

    if amount < MIN_WITHDRAWAL:
        raise ValidationError(
            f"Minimum withdrawal is ₹{MIN_WITHDRAWAL}."
        )

    if current_balance - amount < MIN_BALANCE:
        raise ValidationError(
            f"Minimum balance of ₹{MIN_BALANCE} "
            "must be maintained."
        )

    return True