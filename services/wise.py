import json
import uuid

import requests
from decouple import config
from fastapi import HTTPException


class WiseService:
   def __init__(self):
      self.main_url = config('WISE_URL')
      self.headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {config("WISE_TOKEN")}',
      }
      self.profile_id = self._get_profile_id()

   def _get_profile_id(self):
      url = self.main_url + '/v1/profiles'
      res = requests.get(url, headers=self.headers)

      if res.status_code == 200:
         res = res.json()
         return [el['id'] for el in res if el['type'] == 'personal'][0]
      else:
         raise HTTPException(status_code=500, detail='Payment provider is not available at the moment')

   def create_quote(self, amount):
      url = self.main_url + '/v2/quotes'
      data = {
         'sourceCurrency': 'EUR',
         'targetCurrency': 'EUR',
         'targetAmount': amount,
         'profile': self.profile_id,
      }
      res = requests.post(url, headers=self.headers, data=json.dumps(data))
      if res.status_code == 200:
         res = res.json()
         return res['id']
      else:
         raise HTTPException(status_code=500, detail='Payment provider is not available at the moment')

   def create_recipient_account(self, full_name, iban):
      url = self.main_url + '/v1/accounts'
      data = {
         'currency': 'EUR',
         'type': 'iban',
         'profile': self.profile_id,
         'accountHolderName': full_name,
         'legalType': 'PRIVATE',
         'details': {'iban': iban},
      }
      res = requests.post(url, headers=self.headers, data=json.dumps(data))
      if res.status_code == 200:
         res = res.json()
         return res['id']
      else:
         raise HTTPException(status_code=500, detail='Payment provider is not available at the moment')

   def create_transfer(self, target_account_id, quote_id):
      customer_transaction_id = str(uuid.uuid4())
      url = self.main_url + '/v1/transfers'
      data = {
         'targetAccount': target_account_id,
         'quoteUuid': quote_id,
         'customerTransactionId': customer_transaction_id,
         'details': {},
      }
      res = requests.post(url, headers=self.headers, data=json.dumps(data))
      if res.status_code == 200:
         res = res.json()
         return res['id']
      else:
         raise HTTPException(status_code=500, detail='Payment provider is not available at the moment')

   def fund_transfer(self, transfer_id):
      url = self.main_url + f'/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments'
      data = {'type': 'BALANCE'}
      res = requests.post(url, headers=self.headers, data=json.dumps(data))
      if res.status_code == 201:
         res = res.json()
         return res['balanceTransactionId'] # 'id'
      else:
         raise HTTPException(status_code=500, detail='Payment provider is not available at the moment')

   def cancel_transfer(self, transfer_id):
      url = self.main_url + f'/v1/transfers/{transfer_id}/cancel'
      res = requests.put(url, headers=self.headerss)
      if res.status_code == 200:
         resp = res.json()
         return resp["id"]
      else:
         raise HTTPException(status_code=500, detail="Payment provider is not available at the moment")


if __name__ == '__main__':
   wise = WiseService()
   print(f'profile_id = {wise.profile_id}')
   quote_id = wise.create_quote(amount=99)
   print(f'quote_id = {quote_id}')
   recipient_id = wise.create_recipient_account(full_name='Test Recipient', iban='GB15MIDL40051512345678')
   print(f'recipient_id = {recipient_id}')
   transfer_id = wise.create_transfer(target_account_id=recipient_id, quote_id=quote_id)
   print(f'transfer_id = {transfer_id}')
   res = wise.fund_transfer(transfer_id=transfer_id)
   print(f'response = ', res)


