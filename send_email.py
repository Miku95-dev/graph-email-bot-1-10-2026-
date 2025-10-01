import requests
import json
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file (chỉ dùng khi test local)
load_dotenv()

# Load secrets từ biến môi trường
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']
user_email = os.environ['USER_EMAIL']

# Lấy access token
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
token_r = requests.post(token_url, data=token_data)

# In phản hồi để kiểm tra lỗi xác thực
print("Token response status:", token_r.status_code)
print("Token response text:", token_r.text)

# Xử lý lỗi nếu không lấy được token
try:
    token_r.raise_for_status()
    access_token = token_r.json().get("access_token")
except requests.exceptions.RequestException as e:
    print("Failed to get access token:", e)
    exit(1)

# Chuẩn bị email
email_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

content = "Chào bạn, đây là tệp Tinh Thần Biến được gửi từ Graph API."
encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

email_data = {
    "message": {
        "subject": "Tự động gửi email bằng Graph API",
        "body": {
            "contentType": "Text",
            "content": "Email này được gửi tự động để duy trì hoạt động tài khoản E5 Developer."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": user_email
                }
            }
        ],
        "attachments": [
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": "Tinh Thần Biến.txt",
                "contentBytes": encoded
            }
        ]
    },
    "saveToSentItems": "true"
}

# Gửi email
r = requests.post(email_url, headers=headers, data=json.dumps(email_data))
print("Status:", r.status_code)
print("Response:", r.text)
