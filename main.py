from fastapi import FastAPI, Request
import requests
import uvicorn
from datetime import datetime

app = FastAPI()

TELEGRAM_BOT_TOKEN = "7554629243:AAFv2PnwsgTyNG0eEIYP-h9aSGmUf2yvaJU"
TELEGRAM_CHAT_ID = "6717395416"  # Your admin ID

def send_to_telegram(message: str, urgent=False):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    if urgent:
        message = f"🚨 *URGENT* 🚨\n\n{message}"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Notification sent to admin")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
    return False

@app.post("/")
async def telegram_webhook(request: Request):
    update = await request.json()
    print("📩 RECEIVED TELEGRAM UPDATE:")
    print(update)

    # Extract user info — even if not "first message"
    if "message" in update:
        user = update["message"]["from"]
        user_id = user.get("id", "unknown")
        username = user.get("username", "N/A")
        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        language = user.get("language_code", "unknown")
        message_text = update["message"].get("text", "[no text]")

        name = f"{first_name} {last_name}".strip() or "Anonymous"
        notification = (
            f"💬 *MESSAGE RECEIVED*\n\n"  # Changed from "NEW VISITOR" to "MESSAGE RECEIVED"
            f"🆔 User ID: `{user_id}`\n"
            f"👤 Name: {name}\n"
            f"📝 Username: @{username}\n"
            f"🗣️ Language: {language.upper()}\n"
            f"💬 Message: _{message_text[:50]}{'...' if len(message_text) > 50 else ''}_\n"
            f"🕒 Time: {datetime.utcnow().strftime('%H:%M UTC')}"
        )

        send_to_telegram(notification, urgent=True)  # Notify on EVERY message

    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
