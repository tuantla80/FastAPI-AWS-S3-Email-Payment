import boto3
from botocore.exceptions import ClientError

from decouple import config
from fastapi import HTTPException


class S3Service:
   def __init__(self):
      self.access_key = config('AWS_ACCESS_KEY')
      self.secret_key = config('AWS_SECRET_ACCESS_KEY')
      self.s3_client = boto3.client(
         service_name = 's3',
         aws_access_key_id=self.access_key,
         aws_secret_access_key=self.secret_key
      )
      self.bucket_name = config('AWS_BUCKET_NAME')

   def upload_photo(self, file_path, file_name, ext):
      try:
         self.s3_client.upload_file(
            file_path,
            self.bucket_name,
            file_name,
            ExtraArgs={
               'ACL': 'public-read',
               'ContentType': f'image/{ext}'
            }
         )
         return f'https://{self.bucket_name}.s3.{config("AWS_REGION")}.amazonaws.com/{file_name}'
      except ClientError as ex:
         print(ex)
         raise HTTPException(status_code=500, detail=f'{ex}')
      except Exception as ex:
         print('ex2 = ', ex)
         raise HTTPException(status_code=500, detail=f'{ex}')


if __name__ == '__main__':
   s3 = S3Service()
   print('s3 = ', s3)
