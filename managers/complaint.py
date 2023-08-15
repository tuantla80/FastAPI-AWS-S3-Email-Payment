from db import database
from models import complaint, RoleType, State

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
      data['complainer_id'] = user['id']
      id_ = await database.execute(complaint.insert().values(**data))
      return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

   @staticmethod
   async def delete_complaint(complaint_id):
      await database.execute(complaint.delete().where(complaint.c.id == int(complaint_id)))

