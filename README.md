
# 🤖 Chatbot API

This FastAPI project provides endpoints for a document-aware AI chatbot with support for file uploads, user registration, and message logging using AWS (S3, DynamoDB) and MySQL.

---

## 🔧 Setup Instructions

- Python ≥ 3.8
- Install dependencies:
```bash
pip install fastapi uvicorn boto3 pymysql python-multipart
```

---

## 🚀 Base URL

```
http://<your-domain-or-ip>:<port>/
```

---

## 📄 Endpoints

### 🔐 `/signup`
**Method:** POST  
Register a new user.

**Request Body:**
```json
{
  "user_id": "john123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

### 🔓 `/signin`
**Method:** POST  
Authenticate an existing user.

**Request Body:**
```json
{
  "user_id": "john123"
}
```

---

### 💬 `/chat`
**Method:** POST  
Chat with the bot with optional file upload.

**Form Parameters:**
- `user_id`: string (required)
- `message`: string (required)
- `file`: file (optional)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/chat \
-F "user_id=john123" \
-F "message=Summarize this document" \
-F "file=@./sample.pdf"
```

---

## 🧪 Python Test Script

```python
import requests

def test_signup():
    res = requests.post("http://localhost:8000/signup", json={
        "user_id": "john123",
        "name": "John Doe",
        "email": "john@example.com"
    })
    print("Signup:", res.json())

def test_signin():
    res = requests.post("http://localhost:8000/signin", json={
        "user_id": "john123"
    })
    print("Signin:", res.json())
    return res.json().get("session_id")

def test_chat(message="Hello!", file_path=None):
    files = {"file": open(file_path, "rb")} if file_path else None
    data = {
        "user_id": "john123",
        "message": message
    }
    res = requests.post("http://localhost:8000/chat", data=data, files=files)
    print("Chat:", res.json())

if __name__ == "__main__":
    test_signup()
    session_id = test_signin()
    test_chat("Hello, how can you help?")
    test_chat("Please summarize this document.", file_path="sample.pdf")
```

---
