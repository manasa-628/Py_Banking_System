import mysql.connector
from mysql.connector import Error

from .config import DB_CONFIG


def get_root_connection():
    """Connect to MySQL without selecting a database."""

    config = {
        "host": DB_CONFIG["host"],
        "user": DB_CONFIG["user"],
        "password": DB_CONFIG["password"],
        "autocommit": False
    }

    return mysql.connector.connect(**config)


def create_database_if_not_exists():
    """Create banking_db database if it does not exist."""

    conn = get_root_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS banking_db"
        )

        conn.commit()

        print("Database 'banking_db' is ready.")

    except Error as exc:
        conn.rollback()
        raise RuntimeError(
            f"Unable to create database: {exc}"
        ) from exc

    finally:
        if cursor:
            cursor.close()

        conn.close()


def create_tables():
    """Create all required banking tables."""

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = None

    try:
        cursor = conn.cursor()

        # Accounts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                account_no VARCHAR(15) PRIMARY KEY,
                holder_name VARCHAR(50) NOT NULL,
                pin_hash VARCHAR(64) NOT NULL,
                balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                account_type ENUM('SAVINGS','CURRENT')
                    NOT NULL DEFAULT 'SAVINGS',
                status ENUM('ACTIVE','INACTIVE','LOCKED')
                    NOT NULL DEFAULT 'ACTIVE',
                failed_attempts TINYINT NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP
            )
            """
        )

        # Transactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) NOT NULL,
                txn_type ENUM(
                    'DEPOSIT',
                    'WITHDRAWAL',
                    'BALANCE_CHECK'
                ) NOT NULL,
                amount DECIMAL(15,2) DEFAULT NULL,
                balance_after DECIMAL(15,2) NOT NULL,
                description VARCHAR(255) DEFAULT NULL,
                txn_date DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (account_no)
                    REFERENCES accounts(account_no)
                    ON DELETE CASCADE
            )
            """
        )

        # Audit log table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) DEFAULT NULL,
                event_type VARCHAR(50) NOT NULL,
                details TEXT DEFAULT NULL,
                event_time DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Daily withdrawal table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_withdrawal_limits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) NOT NULL,
                limit_date DATE NOT NULL,
                total_withdrawn DECIMAL(15,2)
                    NOT NULL DEFAULT 0.00,

                UNIQUE KEY uq_account_date
                    (account_no, limit_date),

                FOREIGN KEY (account_no)
                    REFERENCES accounts(account_no)
                    ON DELETE CASCADE
            )
            """
        )

        conn.commit()

        print("All banking tables are ready.")

    except Error as exc:
        conn.rollback()

        raise RuntimeError(
            f"Unable to create tables: {exc}"
        ) from exc

    finally:
        if cursor:
            cursor.close()

        conn.close()


def initialize_database():
    """Initialize database and tables."""

    create_database_if_not_exists()
    create_tables()


if __name__ == "__main__":
    initialize_database()