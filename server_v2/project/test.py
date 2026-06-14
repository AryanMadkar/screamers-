import requests
import sys
import os
from dotenv import load_dotenv

# Load PORT from environment or default to 8000
load_dotenv()
PORT = os.getenv("PORT", 8000)
URL = f"http://localhost:{PORT}/chat"

def main():
    print("==================================================")
    print("     Screemer Interactive Chat Terminal Client     ")
    print("==================================================")
    print(f"Connecting to API at: {URL}")
    print("Type 'exit', 'quit', or press Ctrl+C to stop.")
    print("==================================================\n")

    user_id = None
    conversation_id = None

    try:
        # Check if the server is running first
        health_url = f"http://localhost:{PORT}/health"
        try:
            res = requests.get(health_url, timeout=3)
            if res.status_code == 200:
                print("✓ Connected to server health endpoint.")
            else:
                print(f"⚠ Server returned status code {res.status_code} on health check.")
        except requests.exceptions.ConnectionError:
            print("❌ ERROR: Cannot connect to the server.")
            print(f"Please make sure the server is running by executing: python app.py")
            sys.exit(1)

        while True:
            try:
                user_msg = input("\nYou: ").strip()
            except EOFError:
                break

            if not user_msg:
                continue

            if user_msg.lower() in ("exit", "quit"):
                print("Exiting chat. Goodbye!")
                break

            payload = {
                "message": user_msg,
                "user_id": user_id,
                "conversation_id": conversation_id
            }

            try:
                response = requests.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Update session trackers
                    user_id = data.get("user_id")
                    conversation_id = data.get("conversation_id")
                    
                    # Print reply
                    ai_reply = data.get("response", "")
                    print(f"\nPriya: {ai_reply}")
                else:
                    print(f"\n❌ Error ({response.status_code}): {response.text}")
            except Exception as e:
                print(f"\n❌ Request failed: {e}")

    except KeyboardInterrupt:
        print("\n\nExiting chat. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
