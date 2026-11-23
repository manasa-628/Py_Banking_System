class BankingError(Exception):
    """Base exception for banking system."""
    pass


class ValidationError(BankingError):
    """Raised when input validation fails."""
    pass


class AccountNotFoundError(BankingError):
    """Raised when account does not exist."""
    pass


class AuthenticationError(BankingError):
    """Raised when authentication fails."""
    pass


class AccountLockedError(BankingError):
    """Raised when account is locked."""
    pass


class InsufficientBalanceError(BankingError):
    """Raised when balance is insufficient."""
    pass