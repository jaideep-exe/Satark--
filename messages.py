"""
All fixed text the bot says. Member 4 can edit this file without touching bot.py.
Plain text only (no Markdown) so Telegram never rejects a message.
"""

WELCOME = (
    "Namaste! I am Satark, your scam checker.\n\n"
    "Send me a suspicious message, a screenshot, a voice note, or a UPI ID / phone number, "
    "and I will point out the red flags and tell you if it has been reported before.\n\n"
    "I only say how many times something was reported. I never accuse anyone."
)

HELP = (
    "How to use Satark:\n"
    "1. Paste the suspicious message, OR send a screenshot, OR send a voice note.\n"
    "2. Read the red flags and safe steps.\n"
    "3. Tap 'Report this as a scam' to protect the next person.\n\n"
    "If you already lost money, tap 'I lost money' for immediate steps."
)

ANALYZING = "Checking this for you, one moment..."

ERROR = "Sorry, something went wrong while checking this. Please try again."

SAFE_STEPS = (
    "Safe steps:\n"
    "- Do not share OTP, PIN or card details with anyone.\n"
    "- Do not click unknown links or install apps someone sends you.\n"
    "- Hang up and call your bank on the number printed on your card."
)

NO_REPORTS_NOTE = (
    "No reports yet for these, but the red flags above are present. "
    "No reports does not mean safe."
)

# Shown first on HIGH risk and when the user taps 'I lost money'
URGENT_STEPS = (
    "ACT NOW:\n"
    "1. Call 1930 (national cyber fraud helpline) immediately. Faster is better for freezing money.\n"
    "2. File a complaint on the National Cyber Crime Reporting Portal: cybercrime.gov.in\n"
    "3. Call your bank and ask them to block the transaction / card.\n"
    "4. Keep screenshots, transaction IDs and phone numbers as proof."
)

FAMILY_ALERT_INTRO = "Forward this to your family so they stay safe:"

# Member 4: improve this wording
FAMILY_ALERT = (
    "SCAM ALERT: I just received a suspicious message that looks like a fraud "
    "(fake bank / KYC / OTP request). Please do NOT share any OTP, PIN or click any links "
    "from unknown people. If someone asks for money urgently, call me first. "
    "National cyber fraud helpline: 1930."
)

COMPLAINT_INTRO = "Draft complaint text you can paste on cybercrime.gov.in (fill in the [brackets]):"

# Member 4: improve this wording
COMPLAINT_DRAFT = (
    "I want to report an online financial fraud / suspected scam.\n"
    "Date and time: [date, time]\n"
    "How the scammer contacted me: [call / SMS / WhatsApp / Telegram]\n"
    "Scammer's phone number: [number]\n"
    "Scammer's UPI ID: [upi id]\n"
    "What they asked for: [OTP / payment / personal details]\n"
    "Amount lost (if any): [amount]\n"
    "Transaction ID (if any): [id]\n"
    "Short description: [what happened, in 2-3 lines]"
)

REPORT_THANKS = "Thank you. Your report helps protect the next person."
REPORT_DUPLICATE = "You have already reported these, so I did not count them twice."
REPORT_NOTHING = "I found no UPI ID or phone number in that message to save a report against."
