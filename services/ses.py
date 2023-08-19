'''
ses: AWS Simple Email Service
'''

import boto3
from decouple import config


class SESService:
   def __init__(self):
      self.access_key = config('AWS_ACCESS_KEY')
      self.secret_key = config('AWS_SECRET_ACCESS_KEY')
      self.ses_region = config('AWS_SES_REGION')
      self.ses = boto3.client(
         service_name='ses',
         region_name=self.ses_region,
         aws_access_key_id=self.access_key,
         aws_secret_access_key=self.secret_key
      )

   def send_mail(self, sender, receivers, subject, content):
      body = {
         'Text': {
            'Data': content,
            'Charset': 'UTF-8'
         }
      }

      try:
         self.ses.send_email(
            Source=sender,
            Destination={
               'ToAddresses': receivers,
               'CcAddresses': [],
               'BccAddresses': []
            },
            Message={
               'Subject': {
                  'Data': subject,
                  'Charset': 'UTF-8'
               },
               'Body': body
            },
         )
      except Exception as ex:
         raise ex