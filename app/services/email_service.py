"""
Email service module responsible for sending activation codes
to a third-party SMTP provider that exposes an HTTP API.

This module must be isolated from business logic so that:
- The API can change (SMTP → HTTP → provider change)
- Failures do not break user creation logic
- The service can be mocked easily for tests
"""

import os
import json
import http.client
from urllib.parse import urlparse

# The email API endpoint is configurable via environment variable.
# This allows switching between:
# - a mock service
# - a local SMTP container with HTTP wrapper
# - a real provider (Mailgun, SendGrid, etc.)
#
# Default: local mock running at http://email-mock:3001/send
EMAIL_API_URL = os.getenv("EMAIL_API_URL", "http://email-mock:3001/send")


def send_activation_email(email: str, code: str) -> bool:
    """
    Sends the activation code to a third-party email service.

    The service is assumed to expose an HTTP endpoint that accepts:
        POST /send
        Body: { "email": "...", "code": "1234" }

    The function returns:
        True  → email sent successfully
        False → failure (network error, timeout, non-200 response)

    IMPORTANT:
    - This function must never raise exceptions to business logic.
    - It must remain safe, isolated, and side-effect only.
    """

    try:
        # Parse EMAIL_API_URL = "http://email-mock:3001/send"
        parsed = urlparse(EMAIL_API_URL)
        host = parsed.hostname or "localhost"
        port = parsed.port or 80
        path = parsed.path or "/send"

        # Prepare HTTP client
        conn = http.client.HTTPConnection(host, port, timeout=3)

        # JSON payload for the third-party email service
        payload = json.dumps({"email": email, "code": code})
        headers = {"Content-Type": "application/json"}

        # Perform HTTP POST request
        conn.request("POST", path, body=payload, headers=headers)

        # Wait for response
        resp = conn.getresponse()
        conn.close()

        # Consider success if 200 or 202
        return resp.status in (200, 202)

    except Exception:
        # We return False so the main logic can still continue
        # and fallback to printing or logging the activation code.
        return False
