import bcrypt
import random
from datetime import datetime, timedelta
from psycopg2.errors import UniqueViolation

from app.db.connection import get_connection
from app.services.email_service import send_activation_email
from app.utils.logging import logger, redact_email


class ConflictError(Exception):
    """Raised when trying to create a user that already exists (email unique constraint)."""
    pass


def _generate_code() -> str:
    """
    Generate a 4-digit numeric activation code as a string.

    Using 0000–9999 with left-padding ensures the code always has 4 digits.
    """
    return f"{random.randint(0, 9999):04d}"


def create_user(email: str, password: str) -> None:
    """
    Create a new user:

    - Hash the password with bcrypt.
    - Insert the user row in the `users` table.
    - Generate a 4-digit activation code, valid for 1 minute.
    - Store the activation code in `activation_codes`.
    - Call the third-party email service to send the code.
      If the email service is unavailable, log a warning and print the code.

    Raises:
        ConflictError: if a user with the same email already exists.
    """
    # Hash the password using bcrypt (one-way hash + salt).
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    try:
        # Using the connection as a context manager ensures commit/rollback is handled.
        with conn:
            with conn.cursor() as cur:
                # Insert the user and get its generated ID.
                cur.execute(
                    "INSERT INTO users (email, password_hash) "
                    "VALUES (%s, %s) RETURNING id",
                    (email, hashed),
                )
                user_id = cur.fetchone()[0]

                # Generate the activation code, valid for 1 minute from now (UTC).
                code = _generate_code()
                expires = datetime.utcnow() + timedelta(minutes=1)

                # Store the activation code in a dedicated table.
                cur.execute(
                    "INSERT INTO activation_codes (user_id, code, expires_at) "
                    "VALUES (%s, %s, %s)",
                    (user_id, code, expires),
                )

                # Call the third-party email service (HTTP API, mocked in this project).
                ok = send_activation_email(email, code)
                if not ok:
                    # The third-party is optional: user creation still succeeds,
                    # but we log a warning and print the code for debugging.
                    logger.warning(
                        f"Email Service unavailable for {redact_email(email)}; "
                        "activation code printed to stdout."
                    )

                # Always print the code in console (allowed by the requirements).
                print(f"[MOCK EMAIL] Activation code for {redact_email(email)}: {code}")
                logger.info(f"User created {redact_email(email)}")

        # If we reach here, the transaction has been committed successfully.

    except UniqueViolation:
        # Unique constraint on `users.email` violated → user already exists.
        conn.rollback()
        raise ConflictError("User already exists.")
    finally:
        # Ensure the DB connection is always closed.
        conn.close()


def activate_user(email: str, password: str, code: str) -> bool:
    """
    Try to activate a user account.

    Steps:
    - Look up the user by email.
    - If user not found → return False.
    - If already active → return True (idempotent activation).
    - Verify the password with bcrypt.
    - Fetch the last activation code for this user.
    - Check if:
        * the code matches
        * and it has not expired (expires_at > now).
    - If valid → mark user as active and (optionally) invalidate the code.

    Returns:
        True  → activation successful (or user already active).
        False → invalid email/password/code OR expired code.

    The API layer (FastAPI route) will convert False into an HTTP error
    (e.g. 400 with a message: "Invalid or expired code").
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # 1) Fetch user row by email.
                cur.execute(
                    "SELECT id, password_hash, is_active "
                    "FROM users WHERE email = %s",
                    (email,),
                )
                row = cur.fetchone()
                if not row:
                    # Email not found.
                    logger.info(f"Activation failed: unknown user {redact_email(email)}")
                    return False

                user_id, hashed, is_active = row

                # 2) If already active, we consider this a success (idempotent).
                if is_active:
                    logger.info(f"Activation skipped: user already active {redact_email(email)}")
                    return True

                # 3) Check password using bcrypt.
                if not bcrypt.checkpw(password.encode(), hashed.encode()):
                    logger.info(f"Activation failed: invalid password for {redact_email(email)}")
                    return False

                # 4) Fetch activation code row for this user.
                cur.execute(
                    "SELECT code, expires_at "
                    "FROM activation_codes WHERE user_id = %s",
                    (user_id,),
                )
                ac_row = cur.fetchone()
                if not ac_row:
                    # No activation code found (should not happen in normal flow).
                    logger.info(f"Activation failed: no activation code for {redact_email(email)}")
                    return False

                db_code, expires = ac_row

                now = datetime.utcnow()

                # 5) Check whether code matches and is still valid.
                if db_code != code:
                    logger.info(f"Activation failed: wrong code for {redact_email(email)}")
                    return False

                if now >= expires:
                    # Code expired (more than 1 minute old).
                    logger.info(f"Activation failed: code expired for {redact_email(email)}")
                    return False

                # 6) Mark user as active.
                cur.execute(
                    "UPDATE users SET is_active = TRUE WHERE id = %s",
                    (user_id,),
                )

                # (Optional) Invalidate the activation code so it can't be reused.
                # cur.execute("DELETE FROM activation_codes WHERE user_id = %s", (user_id,))

                logger.info(f"User activated: {redact_email(email)}")
                return True

    finally:
        # Always close the connection.
        conn.close()
