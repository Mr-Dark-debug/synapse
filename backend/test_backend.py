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
    paper_id = "2310.12345"
    item_data = {
        "paper_id": paper_id,
        "paper_title": "Test Paper",
        "paper_summary": "This is a test paper."
    }
    response = requests.post(f"{BASE_URL}/collections/{collection_id}/items", json=item_data, headers=headers)
    if response.status_code == 200:
        print("✅ Item added")
    else:
        print(f"❌ Add item failed: {response.text}")

    # 4. Test the new check endpoint - paper should be saved
    print("\n4. Testing check saved endpoint (saved paper)...")
    response = requests.get(f"{BASE_URL}/collections/items/check/{paper_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("saved") == True:
            print("✅ Check saved endpoint working correctly for saved paper")
        else:
            print(f"❌ Check saved endpoint returned unexpected result: {result}")
    else:
        print(f"❌ Check saved endpoint failed: {response.text}")

    # 5. Test the new check endpoint - paper should not be saved
    print("\n5. Testing check saved endpoint (unsaved paper)...")
    unsaved_paper_id = "9999.99999"
    response = requests.get(f"{BASE_URL}/collections/items/check/{unsaved_paper_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("saved") == False:
            print("✅ Check saved endpoint working correctly for unsaved paper")
        else:
            print(f"❌ Check saved endpoint returned unexpected result: {result}")
    else:
        print(f"❌ Check saved endpoint failed: {response.text}")

    # 6. Create Chat Session
    print("\n6. Creating Chat Session...")
    response = requests.post(f"{BASE_URL}/chat/sessions", json={"title": "Test Chat"}, headers=headers)
    if response.status_code == 200:
        session_id = response.json()["id"]
        print(f"✅ Session created: {session_id}")
    else:
        print(f"❌ Create session failed: {response.text}")
        return

    # 7. Send Message
    print("\n7. Sending Message...")
    msg_data = {"message": "Hello, how are you?", "paper_ids": []}
    # Note: This might fail if Gemini API key is not set, but we check for 500 or specific error
    response = requests.post(f"{BASE_URL}/chat/sessions/{session_id}/message", json=msg_data, headers=headers)
    if response.status_code == 200:
        print(f"✅ Message sent. Response: {response.json()['response']}")
    else:
        print(f"❌ Send message failed: {response.text}")

    # 8. Get History
    print("\n8. Getting History...")
    response = requests.get(f"{BASE_URL}/chat/sessions/{session_id}", headers=headers)
    if response.status_code == 200:
        msgs = response.json()["messages"]
        print(f"✅ History retrieved. {len(msgs)} messages.")
    else:
        print(f"❌ Get history failed: {response.text}")

if __name__ == "__main__":
    test_backend()