"""
Simple token‑based authentication utilities.
In a real product this would be replaced by a full OAuth/JWT solution.
"""

# Hard‑coded list of valid bearer tokens for demo purposes.
VALID_TOKENS = {
    "secret-token-123": "service_a",
    "another-token-456": "service_b",
}


def verify_token(auth_header: str) -> bool:
    """
    Validate an ``Authorization: Bearer <token>`` header.
    Returns ``True`` if the token is known, ``False`` otherwise.
    """
    if not auth_header:
        return False
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False
    token = parts[1]
    return token in VALID_TOKENS


def token_owner(auth_header: str) -> str | None:
    """
    Return the logical owner (e.g. service name) of a valid token,
    or ``None`` if the token is invalid.
    """
    if not verify_token(auth_header):
        return None
    token = auth_header.split()[1]
    return VALID_TOKENS.get(token)