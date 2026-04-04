import json
import requests
mono_url = 'https://monobank.ua'
site_url = 'localhost:8501'
token = ''
def create_payment(order_id, amount_uah):
    paycheck = {
        'amount': amount_uah * 100,
        'ccy': 980,
        'merchantPaymRefer': order_id,
        'redirecturl': site_url,
        'webhookurl': site_url,
        'validaty': 7200
    }
    headers = {
        'Token': token,
        'Content-Type': 'application/json'
    }

    response = requests.post(mono_url, data=json.dumps(paycheck), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text('Виникла помилка, спробуйте ще раз.')}