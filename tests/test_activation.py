from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.db.connection import get_connection

client = TestClient(app)


def create_user_for_test():
    """Helper function to insert a user + activation code directly in DB."""
    email = "activation@test.com"
    password = "Secret123"

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email=%s", (email,))
            cur.execute("""
                INSERT INTO users (email, password_hash)
                VALUES (%s, crypt(%s, gen_salt('bf')))
                RETURNING id
            """, (email, password))
            user_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO activation_codes (user_id, code, expires_at)
                VALUES (%s, %s, %s)
            """, (user_id, "1234", datetime.utcnow() + timedelta(minutes=1)))

    return email, password, "1234"


def test_activation_success():
    email, password, code = create_user_for_test()

    response = client.post(
        "/users/activate",
        json={"code": code},
        auth=(email, password)   # BASIC AUTH
    )

    assert response.status_code == 200
    assert "activated" in response.json()["message"].lower()


def test_activation_wrong_password():
    email, _, code = create_user_for_test()

    response = client.post(
        "/users/activate",
        json={"code": code},
        auth=(email, "badpassword")
    )

    assert response.status_code == 400


def test_activation_wrong_code():
    email, password, _ = create_user_for_test()

    response = client.post(
        "/users/activate",
        json={"code": "9999"},
        auth=(email, password)
    )

    assert response.status_code == 400


def test_activation_expired_code():
    email, password, _ = create_user_for_test()

    # Force code to be expired
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE activation_codes SET expires_at = %s WHERE user_id = (SELECT id FROM users WHERE email=%s)",
                (datetime.utcnow() - timedelta(seconds=10), email)
            )

    response = client.post(
        "/users/activate",
        json={"code": "1234"},
        auth=(email, password)
    )

    assert response.status_code == 400
