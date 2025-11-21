import requests
import json

BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"
PASSWORD = "password123"

def test_backend():
    # 1. Login
    print("1. Logging in...")
    try:
        # Register first just in case
        requests.post(f"{BASE_URL}/auth/signup", json={"email": EMAIL, "password": PASSWORD})
    except:
        pass

    response = requests.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # 2. Create Collection
    print("\n2. Creating Collection...")
    response = requests.post(f"{BASE_URL}/collections/", json={"name": "My Thesis", "description": "Important papers"}, headers=headers)
    if response.status_code == 200:
        collection_id = response.json()["id"]
        print(f"✅ Collection created: {collection_id}")
    else:
        print(f"❌ Create collection failed: {response.text}")
        return

    # 3. Add Item to Collection
    print("\n3. Adding Item...")
    item_data = {
        "paper_id": "2310.12345",
        "paper_title": "Test Paper",
        "paper_summary": "This is a test paper."
    }
    response = requests.post(f"{BASE_URL}/collections/{collection_id}/items", json=item_data, headers=headers)
    if response.status_code == 200:
        print("✅ Item added")
    else:
        print(f"❌ Add item failed: {response.text}")

    # 4. Create Chat Session
    print("\n4. Creating Chat Session...")
    response = requests.post(f"{BASE_URL}/chat/sessions", json={"title": "Test Chat"}, headers=headers)
    if response.status_code == 200:
        session_id = response.json()["id"]
        print(f"✅ Session created: {session_id}")
    else:
        print(f"❌ Create session failed: {response.text}")
        return

    # 5. Send Message
    print("\n5. Sending Message...")
    msg_data = {"message": "Hello, how are you?", "paper_ids": []}
    # Note: This might fail if Gemini API key is not set, but we check for 500 or specific error
    response = requests.post(f"{BASE_URL}/chat/sessions/{session_id}/message", json=msg_data, headers=headers)
    if response.status_code == 200:
        print(f"✅ Message sent. Response: {response.json()['response']}")
    else:
        print(f"❌ Send message failed: {response.text}")

    # 6. Get History
    print("\n6. Getting History...")
    response = requests.get(f"{BASE_URL}/chat/sessions/{session_id}", headers=headers)
    if response.status_code == 200:
        msgs = response.json()["messages"]
        print(f"✅ History retrieved. {len(msgs)} messages.")
    else:
        print(f"❌ Get history failed: {response.text}")

if __name__ == "__main__":
    test_backend()
