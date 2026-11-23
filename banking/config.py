import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "manasa28",
    "database": "banking_db"
}


# Deposit rules
MIN_DEPOSIT = 500
MAX_DEPOSIT = 100000


# Withdrawal rules
MIN_WITHDRAWAL = 100
MIN_BALANCE = 1000
DAILY_WITHDRAWAL_LIMIT = 50000


# PIN security
PIN_LENGTH = 4
MAX_FAILED_PIN_ATTEMPTS = 3


# Account opening
MIN_OPENING_DEPOSIT = 1000


def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn