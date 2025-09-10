from fastapi import FastAPI, Request
import requests
import uvicorn
from datetime import datetime

app = FastAPI()

TELEGRAM_BOT_TOKEN = "7554629243:AAFv2PnwsgTyNG0eEIYP-h9aSGmUf2yvaJU"
TELEGRAM_CHAT_ID = "6717395416"  # Your admin ID

def send_test_message():
    """Send a test message to verify Telegram API works"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "✅ TEST: Render webhook → Telegram is WORKING!",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"📡 TEST MESSAGE STATUS: {response.status_code}")
        print(f"📡 TEST MESSAGE RESPONSE: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"💥 TEST MESSAGE ERROR: {e}")
        return False

@app.post("/")
async def telegram_webhook(request: Request):
    # Log that we received a request
    print("✅ WEBHOOK TRIGGERED — REQUEST RECEIVED")
    
    # Send test message every time
    success = send_test_message()
    
    if success:
        print("🎉 SUCCESS: Test message sent to admin")
    else:
        print("❌ FAILED: Could not send test message")
    
    return {"status": "ok"}

@app.get("/test")
def test_endpoint():
    """Manual test endpoint"""
    print("✅ MANUAL TEST TRIGGERED")
    success = send_test_message()
    if success:
        return {"status": "Test message sent successfully"}
    else:
        return {"status": "Failed to send test message"}, 500

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
