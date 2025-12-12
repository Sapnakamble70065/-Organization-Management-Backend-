from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# MongoDB Atlas se connect ho raha hai
client = AsyncIOMotorClient(settings.MONGO_URI)

# Master Database jisme organizations & admin ka data ayega
master_db = client[settings.MASTER_DB]

# Master collections
orgs_coll = master_db["organizations"]
admins_coll = master_db["admins"]
