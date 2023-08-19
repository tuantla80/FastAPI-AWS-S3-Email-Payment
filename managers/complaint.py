import os
import uuid

from contants import TEMP_FILE_FOLDER
from db import database
from models import user, complaint, RoleType, State
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo


s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        query = complaint.select()
        if user['role'] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user['id'])
        elif user['role'] == RoleType.approver:
            query = query.where(complaint.c.status == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data, user):
        data = complaint_data.dict()
        data["complainer_id"] = user["id"]
        id_ = await database.execute(complaint.insert().values(**data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(
            complaint.delete().where(complaint.c.id == int(complaint_id))
        )

    @staticmethod
    async def approve(complaint_id, appover):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.approved)
        )

        complaint_record = await database.fetch_one(complaint.select().where(complaint.c.id == complaint_id))
        complainer_id = dict(complaint_record._mapping)['complainer_id']

        complainer_record = await database.fetch_one(user.select().where(user.c.id == complainer_id))
        complainer_email = dict(complainer_record._mapping)['email']
        ses.send_mail(
            sender=appover['email'],
            receivers=[complainer_email],
            subject='Your complaint is approved',
            content='Congrats! You complaint is approved. '
                    'Please check your bank account after 2 business days to '
                    'verify the claimed amount is there.\n Kind regards!',
        )

    @staticmethod
    async def reject(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.rejected)
        )

    @staticmethod
    async def create_complaint(complaint_data, user, keep_photo_at_local_server=False):
        data = complaint_data.dict()
        data['complainer_id'] = user['id']

        encoded_photo = data.pop('encoded_photo')
        ext = data.pop('extension')
        file_name = f'{uuid.uuid4()}.{ext}'
        file_path = os.path.join(TEMP_FILE_FOLDER, file_name)
        decode_photo(file_path, encoded_photo)
        data['photo_url'] = s3.upload_photo(file_path, file_name, ext)

        if not keep_photo_at_local_server:
            os.remove(file_path)

        id_ = await database.execute(complaint.insert().values(**data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))