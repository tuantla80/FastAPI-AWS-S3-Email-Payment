import asyncclick

from db import database
from managers.user import UserManager
from models.enums import RoleType


@asyncclick.command()
@asyncclick.option("-f", "--first_name", type=str, required=True)
@asyncclick.option("-l", "--last_name", type=str, required=True)
@asyncclick.option("-e", "--email", type=str, required=True)
@asyncclick.option("-p", "--phone", type=str, required=True)
@asyncclick.option("-i", "--iban", type=str, required=True)
@asyncclick.option("-pw", "--password", type=str, required=True)
async def create_user(first_name, last_name, email, phone, iban, password):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "iban": iban,
        "password": password,
        "role": RoleType.admin,
    }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")
