"""
Satark Telegram bot  (Member 1)

Run:  python bot.py
Needs a .env file with TELEGRAM_BOT_TOKEN=...
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import messages

# ---------------------------------------------------------------------------
# STEP 1: for now we use FAKE functions from stubs.py.
# When your teammates are done, swap these lines for the real imports:
#   from gemini_analysis import analyze_evidence      (Member 2)
#   from database import check_identifier, add_report (Member 3)
# ---------------------------------------------------------------------------
from stubs import add_report, analyze_evidence, check_identifier

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("satark")

RISK_LABELS = {
    "low": "LOW RISK",
    "medium": "MEDIUM RISK",
    "high": "HIGH RISK",
}
RISK_EMOJI = {"low": "🟢", "medium": "🟡", "high": "🔴"}


# ---------------------------------------------------------------------------
# Building the reply text
# ---------------------------------------------------------------------------
def format_verdict(result: dict, counts: dict) -> str:
    """Turn the analysis dict + report counts into one readable message."""
    risk = str(result.get("risk_level", "medium")).lower()
    lines = [f"{RISK_EMOJI.get(risk, '🟡')} {RISK_LABELS.get(risk, risk.upper())}"]

    summary = result.get("summary")
    if summary:
        lines.append("")
        lines.append(summary)

    red_flags = result.get("red_flags") or []
    if red_flags:
        lines.append("")
        lines.append("Red flags:")
        for flag in red_flags:
            lines.append(f"- {flag}")

    identifiers = result.get("identifiers") or []
    if identifiers:
        lines.append("")
        lines.append("Identifiers found:")
        for ident in identifiers:
            value = ident.get("value", "?")
            kind = ident.get("type", "id")
            n = counts.get(value, 0)
            if n > 0:
                lines.append(f"- {kind}: {value} (reported {n} times)")
            else:
                lines.append(f"- {kind}: {value} (no reports yet)")
        if all(counts.get(i.get("value"), 0) == 0 for i in identifiers):
            lines.append("")
            lines.append(messages.NO_REPORTS_NOTE)

    lines.append("")
    if risk == "high":
        lines.append(messages.URGENT_STEPS)
    else:
        lines.append(messages.SAFE_STEPS)

    text = "\n".join(lines)
    return text[:4000]  # Telegram's limit is 4096 characters


def action_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🚩 Report this as a scam", callback_data="report")],
            [InlineKeyboardButton("💸 I lost money", callback_data="loss")],
        ]
    )


async def send_verdict(update: Update, context: ContextTypes.DEFAULT_TYPE, result: dict):
    """Look up report counts, remember the result, and send the reply."""
    identifiers = result.get("identifiers") or []
    counts = {}
    for ident in identifiers:
        value = ident.get("value")
        if value:
            counts[value] = check_identifier(value)

    # Remember this result so the buttons below know what to report.
    context.user_data["last_result"] = result

    await update.message.reply_text(
        format_verdict(result, counts), reply_markup=action_buttons()
    )

    # High risk: also send ready-to-forward family alert + complaint draft
    if str(result.get("risk_level", "")).lower() == "high":
        await update.message.reply_text(messages.FAMILY_ALERT_INTRO)
        await update.message.reply_text(messages.FAMILY_ALERT)
        await update.message.reply_text(messages.COMPLAINT_INTRO)
        await update.message.reply_text(messages.COMPLAINT_DRAFT)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.WELCOME)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.HELP)


# ---------------------------------------------------------------------------
# Evidence handlers: text, photo, voice
# asyncio.to_thread runs slow functions (like the Gemini call) in the
# background so the bot does not freeze for other users.
# ---------------------------------------------------------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.ANALYZING)
    try:
        result = await asyncio.to_thread(analyze_evidence, text=update.message.text)
        await send_verdict(update, context, result)
    except Exception:
        logger.exception("Text analysis failed")
        await update.message.reply_text(messages.ERROR)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.ANALYZING)
    try:
        photo = update.message.photo[-1]  # last item = biggest size
        tg_file = await photo.get_file()
        data = bytes(await tg_file.download_as_bytearray())
        result = await asyncio.to_thread(
            analyze_evidence,
            text=update.message.caption,
            file_bytes=data,
            mime_type="image/jpeg",
        )
        await send_verdict(update, context, result)
    except Exception:
        logger.exception("Photo analysis failed")
        await update.message.reply_text(messages.ERROR)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.ANALYZING)
    try:
        tg_file = await update.message.voice.get_file()
        data = bytes(await tg_file.download_as_bytearray())
        result = await asyncio.to_thread(
            analyze_evidence, file_bytes=data, mime_type="audio/ogg"
        )
        await send_verdict(update, context, result)
    except Exception:
        logger.exception("Voice analysis failed")
        await update.message.reply_text(messages.ERROR)


# ---------------------------------------------------------------------------
# Button presses
# ---------------------------------------------------------------------------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # stops the button's loading spinner

    is_loss = query.data == "loss"
    chat = query.message

    # Victim first: urgent steps before anything else
    if is_loss:
        await chat.reply_text(messages.URGENT_STEPS)

    result = context.user_data.get("last_result")
    identifiers = (result or {}).get("identifiers") or []
    if not identifiers:
        await chat.reply_text(messages.REPORT_NOTHING)
        return

    user_id = query.from_user.id
    saved_any = False
    for ident in identifiers:
        value = ident.get("value")
        if not value:
            continue
        ok = add_report(user_id, value, ident.get("type", "unknown"), is_loss)
        saved_any = saved_any or ok

    await chat.reply_text(messages.REPORT_THANKS if saved_any else messages.REPORT_DUPLICATE)


# ---------------------------------------------------------------------------
# Start the bot
# ---------------------------------------------------------------------------
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN. Create a .env file (see .env.example).")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    logger.info("Satark bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
