import requests
from django.conf import settings
from apps.payments.models import Transaction

def initiate_stk_push(project, phone, amount):
    payload = {
        "phone": phone,
        "amount": amount,
    }

    response = requests.post(settings.MPESA_STK_URL, json=payload)

    Transaction.objects.create(
        project=project,
        provider="MPESA",
        reference=response.json().get("CheckoutRequestID"),
        amount=amount,
        status="Pending",
    )

    return response.json()