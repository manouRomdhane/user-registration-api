from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.db.connection import get_connection

client = TestClient(app)


def test_user_registration():
    # GIVEN
    payload = {
        "email": "test@example.com",
        "password": "StrongPass123"
    }

    # WHEN
    response = client.post("/users", json=payload)

    # THEN (HTTP)
    assert response.status_code == 201
    assert "User created" in response.json()["message"]

    # THEN (DATABASE CHECKS)
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # USER EXISTS
            cur.execute("SELECT id, is_active FROM users WHERE email=%s", ("test@example.com",))
            row = cur.fetchone()
            assert row is not None
            user_id, is_active = row
            assert is_active is False

            # ACTIVATION CODE EXISTS
            cur.execute("SELECT code, expires_at FROM activation_codes WHERE user_id=%s", (user_id,))
            ac_row = cur.fetchone()
            assert ac_row is not None
            code, expires_at = ac_row

            # CODE IS 4 DIGITS
            assert len(code) == 4
            assert code.isdigit()

            # EXPIRATION < 60 seconds
            assert expires_at <= datetime.utcnow() + timedelta(seconds=61)

    finally:
        conn.close()
