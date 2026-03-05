import requests
from django.conf import settings
from datetime import datetime
import base64

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.base_url = "https://sandbox.safaricom.co.ke" # Change to api.safaricom.co.ke for production

    def get_token(self):
        """Generates the required OAuth token for Daraja"""
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
        return response.json().get('access_token')

    def stk_push(self, phone, amount, reference):
        """Triggers the M-Pesa PIN prompt on the customer's phone"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        headers = {"Authorization": f"Bearer {self.get_token()}"}
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone, # Customer phone
            "PartyB": self.shortcode,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": reference,
            "TransactionDesc": f"Mshoni Payment - {reference}"
        }
        
        response = requests.post(f"{self.base_url}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
        return response.json()