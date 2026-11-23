# 🏦 PyBank - Banking Management System

## 📌 Project Description

PyBank is a Python-based Banking Management System developed to perform basic banking operations efficiently.

The application helps users manage bank accounts, deposit money, withdraw money, check account balances, and maintain banking transactions.

The project follows a modular programming approach, where different banking operations are implemented using separate Python modules.

It also includes an application interface for easy interaction with banking operations.

## 🎯 Objectives

- Manage bank account information
- Create and maintain customer accounts
- Deposit money into accounts
- Withdraw money from accounts
- Check account balance
- Validate banking transactions
- Maintain transaction records
- Display account information
- Handle banking errors using exception handling
- Manage banking operations efficiently

## 🛠️ Technologies Used

- Python
- MySQL
- MySQL Connector
- Streamlit
- VS Code
- MySQL Workbench
- Git and GitHub

## 🚀 Features

### Account Management

- Create new bank accounts
- Store account information
- Manage customer details
- Validate account information

### Deposit Management

- Deposit money into an account
- Validate deposit amounts
- Update account balance
- Apply minimum deposit rules

### Withdrawal Management

- Withdraw money from an account
- Check available balance
- Validate withdrawal amounts
- Apply withdrawal limits
- Prevent invalid transactions

### Balance Management

- Check current account balance
- Display available balance
- View updated account information

### Transaction Management

- Maintain banking transaction details
- Track deposit activities
- Track withdrawal activities
- Display transaction information

### User Interface

- Interact with banking operations
- Navigate banking menus
- Perform banking transactions
- View account information

## 🗄️ Database

**Database Name:**

```text
banking_db
```

### Database Configuration

- MySQL database connectivity
- Account data management
- Banking transaction management
- Database operations using Python

## 📂 Project Structure

```text
BANKING_SYSTEM_PY/
│
├── banking/
│   ├── __init__.py
│   ├── account.py
│   ├── balance.py
│   ├── config.py
│   ├── db_setup.py
│   ├── deposit.py
│   ├── display.py
│   ├── exceptions.py
│   ├── history.py
│   ├── validators.py
│   └── withdraw.py
│
├── app.py
├── main.py
├── requirement.txt
└── .gitignore
```

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/manasa-628/Py_Banking_System.git
```

### 2. Open the Project Folder

```bash
cd Py_Banking_System
```

### 3. Install Required Packages

```bash
pip install -r requirement.txt
```

### 4. Configure the Database

- Open MySQL Workbench.
- Configure your MySQL database.
- Open `banking/config.py`.
- Update the database connection details according to your MySQL setup.

### 5. Run the Application

**To run the Python application:**

```bash
python main.py
```

**To run the Streamlit application:**

```bash
python -m streamlit run app.py
```

## 🧪 Testing

The following banking functionalities are included in the project:

- Account Management
- Deposit Money
- Withdraw Money
- Balance Checking
- Transaction History
- Banking Validations
- Exception Handling
- Database Connectivity
- Application Menu Navigation

## 📚 Python Concepts Used

- Functions
- Classes and Objects
- Modules and Packages
- Conditional Statements
- Loops
- Exception Handling
- User Input Handling
- Data Validation
- Modular Programming
- Database Connectivity
- CRUD Operations

## 👩‍💻 Developer

**Manasa**

B.Tech - Data Science

## 📌 Conclusion

PyBank is a Banking Management System developed using Python and database technologies to manage essential banking operations.

It provides functionalities such as account management, deposits, withdrawals, balance checking, and transaction management.

This project helped in understanding Python programming, modular development, database connectivity, validations, and exception handling.
