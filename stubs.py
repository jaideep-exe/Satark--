"""
FAKE versions of the other members' functions, so Member 1 (bot) can test alone.

When the real ones are ready, delete the import of this file in bot.py and use:
    from gemini_analysis import analyze_evidence      # Member 2
    from database import check_identifier, add_report # Member 3
"""


def analyze_evidence(text=None, file_bytes=None, mime_type=None):
    """Member 2 will replace this. Must return a dict with these exact keys."""
    t = (text or "").lower()
    if any(w in t for w in ["otp", "kyc", "blocked", "lottery", "arrest", "refund"]):
        return {
            "risk_level": "high",
            "red_flags": [
                "Creates urgency (account will be blocked)",
                "Asks for OTP or personal details",
                "Claims to be a bank or authority",
            ],
            "identifiers": [
                {"type": "upi", "value": "fakekyc@upi"},
                {"type": "phone", "value": "9876543210"},
            ],
            "summary": "This looks like a typical fake KYC / OTP scam.",
        }
    if file_bytes:
        return {
            "risk_level": "medium",
            "red_flags": ["Screenshot received (stub: no real analysis yet)"],
            "identifiers": [],
            "summary": "Stub reply for a photo or voice note.",
        }
    return {
        "risk_level": "low",
        "red_flags": [],
        "identifiers": [],
        "summary": "No obvious scam signs found (stub).",
    }


def check_identifier(value):
    """Member 3 will replace this. Returns how many times it was reported."""
    return 3 if value == "fakekyc@upi" else 0


def add_report(user_id, identifier, id_type, is_loss):
    """Member 3 will replace this. Returns False if this user already reported it."""
    print(f"[stub] report saved: user={user_id} id={identifier} type={id_type} loss={is_loss}")
    return True
