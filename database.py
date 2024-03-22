from motor import motor_asyncio as mm
import asyncio

class user_database:
    def __init__(self,connection_string,database_name,collection):
        self._client = mm.AsyncIOMotorClient(connection_string)
        self.db = self._client[database_name]
        self.collection = self.db[collection]
        print('connected')
        
    async def new_user(self,userID,remaining):
        user = {"userID": userID, "remaining": remaining}
        await self.collection.insert_one(user)
    
    async def update_plan(self,userID,add):
        await self.collection.update_one(
            {"userID": int(userID)},
            {
                "$inc": {
                    "remaining":  add
                }
            }
        )
    
    async def find_user(self,userID):
        return await self.collection.find_one({"userID": userID})
        
    