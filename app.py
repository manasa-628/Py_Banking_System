
import streamlit as st

from banking.config import get_connection
from banking.account import create_account, authenticate


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="PyBank",
    page_icon="🏦",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None


# ---------------- APPLICATION TITLE ----------------

st.title("🏦 PyBank - Banking Management System")


# ---------------- SIDEBAR MENU ----------------

st.sidebar.title("Main Menu")

menu = st.sidebar.selectbox(
    "Select an option",
    [
        "Home",
        "Open New Account",
        "Login",
        "Deposit",
        "Withdraw",
        "Check Balance",
        "Transaction History",
        "Account Summary",
        "Logout"
    ]
)


# ---------------- HOME ----------------

if menu == "Home":

    st.header("Welcome to PyBank")

    st.write(
        "Manage your banking activities through "
        "a simple and secure interface."
    )

    if st.session_state.logged_in:

        st.success("You are logged in.")

        account = st.session_state.account

        st.write(f"Account Holder: {account['holder_name']}")
        st.write(f"Account Number: {account['account_no']}")

    else:

        st.info("Please create an account or log in.")


# ---------------- CREATE ACCOUNT ----------------

elif menu == "Open New Account":

    st.header("📝 Open New Account")

    with st.form("account_form"):

        holder_name = st.text_input(
            "Account Holder Name"
        )

        pin = st.text_input(
            "Enter 4-digit PIN",
            type="password"
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password"
        )

        account_type = st.selectbox(
            "Account Type",
            ["SAVINGS", "CURRENT"]
        )

        opening_deposit = st.number_input(
            "Opening Deposit",
            min_value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

        if submitted:

            if pin != confirm_pin:

                st.error("PINs do not match.")

            else:

                try:

                    account_no = create_account(
                        holder_name=holder_name,
                        pin=pin,
                        account_type=account_type,
                        opening_deposit=opening_deposit
                    )

                    st.success(
                        "Account created successfully!"
                    )

                    st.info(
                        f"Your account number is: {account_no}"
                    )

                    st.warning(
                        "Please save your account number."
                    )

                except Exception as e:

                    st.error(f"Error: {e}")


# ---------------- LOGIN ----------------

elif menu == "Login":

    st.header("🔐 Login")

    if st.session_state.logged_in:

        st.success("You are already logged in.")

        account = st.session_state.account

        st.write(
            f"Welcome, {account['holder_name']}!"
        )

        st.write(
            f"Account Number: {account['account_no']}"
        )

    else:

        with st.form("login_form"):

            account_no = st.text_input(
                "Account Number"
            )

            pin = st.text_input(
                "Enter PIN",
                type="password"
            )

            login_button = st.form_submit_button(
                "Login"
            )

            if login_button:

                try:

                    account = authenticate(
                        account_no=account_no,
                        pin=pin
                    )

                    st.session_state.logged_in = True
                    st.session_state.account = account

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Login failed: {e}"
                    )


# ---------------- DEPOSIT ----------------


# ---------------- DEPOSIT ----------------

elif menu == "Deposit":

    st.header("💰 Deposit Money")

    if not st.session_state.logged_in:

        st.warning("Please login first.")

    else:

        account_no = st.session_state.account["account_no"]

        st.info(f"Account Number: {account_no}")

        with st.form("deposit_form"):

            amount = st.number_input(
                "Enter Deposit Amount",
                min_value=0.0,
                step=100.0
            )

            deposit_button = st.form_submit_button(
                "Deposit Money"
            )

            if deposit_button:

                if amount < 500:

                    st.error(
                        "Minimum deposit amount is ₹500."
                    )

                elif amount > 100000:

                    st.error(
                        "Maximum deposit amount is ₹100000."
                    )

                else:

                    conn = None
                    cursor = None

                    try:

                        conn = get_connection()

                        cursor = conn.cursor(dictionary=True)

                        # Get current balance

                        cursor.execute(
                            """
                            SELECT balance
                            FROM accounts
                            WHERE account_no = %s
                            """,
                            (account_no,)
                        )

                        account_data = cursor.fetchone()

                        if account_data is None:

                            st.error("Account not found.")

                        else:

                            current_balance = float(
                                account_data["balance"]
                            )

                            new_balance = (
                                current_balance + amount
                            )

                            # Update account balance

                            cursor.execute(
                                """
                                UPDATE accounts
                                SET balance = %s
                                WHERE account_no = %s
                                """,
                                (new_balance, account_no)
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
                                VALUES
                                (
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

                            st.success(
                                "Deposit successful!"
                            )

                            st.metric(
                                "Updated Balance",
                                f"₹{new_balance:,.2f}"
                            )

                            st.info(
                                f"Deposited Amount: ₹{amount:,.2f}"
                            )

                    except Exception as e:

                        if conn is not None:
                            conn.rollback()

                        st.error(
                            f"Deposit failed: {e}"
                        )

                    finally:

                        if cursor is not None:
                            cursor.close()

                        if conn is not None:
                            conn.close()

# ---------------- WITHDRAW ----------------


# ---------------- WITHDRAW ----------------

elif menu == "Withdraw":

    st.header("💸 Withdraw Money")

    if not st.session_state.logged_in:

        st.warning("Please login first.")

    else:

        account_no = st.session_state.account["account_no"]

        st.info(f"Account Number: {account_no}")

        with st.form("withdraw_form"):

            amount = st.number_input(
                "Enter Withdrawal Amount",
                min_value=0.0,
                step=100.0
            )

            withdraw_button = st.form_submit_button(
                "Withdraw Money"
            )

            if withdraw_button:

                if amount < 100:

                    st.error(
                        "Minimum withdrawal amount is ₹100."
                    )

                else:

                    conn = None
                    cursor = None

                    try:

                        conn = get_connection()

                        cursor = conn.cursor(dictionary=True)

                        # Get current balance

                        cursor.execute(
                            """
                            SELECT balance
                            FROM accounts
                            WHERE account_no = %s
                            """,
                            (account_no,)
                        )

                        account_data = cursor.fetchone()

                        if account_data is None:

                            st.error("Account not found.")

                        else:

                            current_balance = float(
                                account_data["balance"]
                            )

                            minimum_balance = 1000

                            # Check minimum balance

                            if (
                                current_balance - amount
                                < minimum_balance
                            ):

                                st.error(
                                    "Withdrawal denied. "
                                    "Minimum balance must be ₹1000."
                                )

                            else:

                                # Check daily withdrawal limit

                                cursor.execute(
                                    """
                                    SELECT
                                        COALESCE(
                                            SUM(amount), 0
                                        ) AS total_withdrawn
                                    FROM transactions
                                    WHERE account_no = %s
                                    AND txn_type = 'WITHDRAWAL'
                                    AND DATE(txn_date) = CURDATE()
                                    """,
                                    (account_no,)
                                )

                                daily_data = cursor.fetchone()

                                total_withdrawn = float(
                                    daily_data["total_withdrawn"]
                                )

                                daily_limit = 50000

                                if (
                                    total_withdrawn + amount
                                    > daily_limit
                                ):

                                    st.error(
                                        "Daily withdrawal limit "
                                        "of ₹50000 exceeded."
                                    )

                                else:

                                    new_balance = (
                                        current_balance - amount
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

                                    # Record withdrawal transaction

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

                                    st.success(
                                        "Withdrawal successful!"
                                    )

                                    st.info(
                                        f"Withdrawn Amount: "
                                        f"₹{amount:,.2f}"
                                    )

                                    st.metric(
                                        "Remaining Balance",
                                        f"₹{new_balance:,.2f}"
                                    )

                    except Exception as e:

                        if conn is not None:

                            conn.rollback()

                        st.error(
                            f"Withdrawal failed: {e}"
                        )

                    finally:

                        if cursor is not None:

                            cursor.close()

                        if conn is not None:

                            conn.close()

# ---------------- CHECK BALANCE ----------------

elif menu == "Check Balance":

    st.header("💳 Check Balance")

    if not st.session_state.logged_in:

        st.warning("Please login first.")

    else:

        account_no = st.session_state.account["account_no"]

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT account_no, holder_name, balance
                FROM accounts
                WHERE account_no = %s
            """

            cursor.execute(query, (account_no,))

            account_data = cursor.fetchone()

            cursor.close()
            conn.close()

            if account_data:

                st.success(
                    f"Account Holder: {account_data['holder_name']}"
                )

                st.metric(
                    "Current Balance",
                    f"₹{account_data['balance']:,.2f}"
                )

            else:

                st.error("Account not found.")

        except Exception as e:

            st.error(f"Database error: {e}")


# ---------------- TRANSACTION HISTORY ----------------

elif menu == "Transaction History":

    st.header("📋 Transaction History")

    if not st.session_state.logged_in:

        st.warning(
            "Please login first to view transactions."
        )

    else:

        account_no = st.session_state.account["account_no"]

        st.write(
            f"Account Number: {account_no}"
        )

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    txn_id AS `Transaction ID`,
                    txn_type AS `Transaction Type`,
                    amount AS `Amount`,
                    balance_after AS `Balance After`,
                    description AS `Description`,
                    txn_date AS `Transaction Date`
                FROM transactions
                WHERE account_no = %s
                ORDER BY txn_date DESC
            """

            cursor.execute(
                query,
                (account_no,)
            )

            transactions = cursor.fetchall()

            if transactions:

                st.success(
                    f"Total transactions: {len(transactions)}"
                )

                st.dataframe(
                    transactions,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No transactions found for this account."
                )

        except Exception as e:

            st.error(
                f"Error loading transactions: {e}"
            )

        finally:

            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()


# ---------------- ACCOUNT SUMMARY ----------------

elif menu == "Account Summary":

    st.header("📊 Account Summary")

    if not st.session_state.logged_in:

        st.warning("Please login first.")

    else:

        account = st.session_state.account

        st.write(
            f"Account Holder: {account['holder_name']}"
        )

        st.write(
            f"Account Number: {account['account_no']}"
        )

        st.write(
            f"Account Type: {account['account_type']}"
        )

        st.info(
            "Your account summary is displayed above."
        )


# ---------------- LOGOUT ----------------

elif menu == "Logout":

    if st.session_state.logged_in:

        st.session_state.logged_in = False
        st.session_state.account = None

        st.success(
            "You have been logged out."
        )

    else:

        st.info(
            "You are not logged in."
        )