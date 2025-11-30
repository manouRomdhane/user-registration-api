import logging

# -----------------------------------------------------------------------------
# Logger configuration for the "registration" domain
# -----------------------------------------------------------------------------
logger = logging.getLogger("registration")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
handler.setFormatter(formatter)

# Avoid adding duplicate handlers if the module is imported multiple times
if not logger.handlers:
    logger.addHandler(handler)


# -----------------------------------------------------------------------------
# Email redaction utility
# -----------------------------------------------------------------------------
def redact_email(email: str) -> str:
    """
    Redact an email address for logging.

    Rules:
    - Keep first and last character of the local part
    - Replace all middle characters with '*'
    - Keep the domain intact

    Examples:
        "john.doe@gmail.com" → "j******e@gmail.com"
        "a@gmail.com"        → "a@gmail.com"
        "ab@gmail.com"       → "a*b@gmail.com"
    """
    if "@" not in email:
        return "<redacted>"

    local, domain = email.split("@", 1)

    if len(local) <= 2:
        # Not enough length to mask; return minimal masking
        return f"{local[0]}*{local[-1]}@{domain}" if len(local) == 2 else f"{local}@{domain}"

    # Normal case: first + stars + last
    masked_local = local[0] + ("*" * (len(local) - 2)) + local[-1]

    return f"{masked_local}@{domain}"
