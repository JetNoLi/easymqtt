import logging
from asyncio import get_event_loop, CancelledError
from contextlib import suppress
#from motor.motor_asyncio import AsyncIOMotorClient
from mongotriggers import MongoTrigger
from pymongo import MongoClient
import pymongo
#import requests
import json
from bson.objectid import ObjectId
#from motor import motor_asyncio
import threading

global client
global trigger
global db

def init():
    global client
    global trigger
    global db
    client = MongoClient("")
    trigger = MongoTrigger(client)
    db = client['why']


def notification(objectId):
    global db
    doc = db['switchCol'].find_one({'_id':ObjectId(objectId)})
    print(doc)

def watchThreaded():
    try:
        with db['switchCol'].watch([{'$match': {'operationType': 'update'}}]) as stream:
            for update in stream:
                # Do something
                print(update['documentKey']['_id'])
                notification(update['documentKey']['_id'])
    except pymongo.errors.PyMongoError:
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        logging.error('...')


# async def cleanup():
#     task.cancel()
#     with suppress(CancelledError):
#         await task

# def watchCol():
#     resume_token = None
#     pipeline = [{'$match': {'operationType': 'update'}}]
#     try:
#         print("trying")
#         async with db['switchCol'].watch(pipeline) as stream:
#             async for update in stream:
#                 print(update)
#                 resume_token = stream.resume_token
#                 notification(update['documentKey']['_id'])
#     except pymongo.errors.PyMongoError:
#         # The ChangeStream encountered an unrecoverable error or the
#         # resume attempt failed to recreate the cursor.
#         if resume_token is None:
#             # There is no usable resume token because there was a
#             # failure during ChangeStream initialization.
#             logging.error('...')
#         else:
#             # Use the interrupted ChangeStream's resume token to
#             # create a new ChangeStream. The new stream will
#             # continue from the last seen insert change without
#             # missing any events.
#             async with db['switchCol'].watch(pipeline, resume_after=resume_token) as stream:
#                 async for update in stream:
#                     print(update)


if __name__ == "__main__":
    init()
    print("Initialised")
    thread = threading.Thread(target=watchThreaded)
    thread.start()
    #get_event_loop().run_until_complete(AsyncIOMotorClient)
    print("AsyncIOMotorClient Passed")
    #get_event_loop().run_until_complete(watchCol)
    print("WatchCol Passed")
    #get_event_loop().run_forever()
#     conn = AsyncIOMotorClient()
#     loop = get_event_loop()
#     task = loop.create_task(watchCol())
#       
#     try:
#         print("About to run forever")
#         loop.run_forever()
#
#     except KeyboardInterrupt:
#         pass
#
#     finally:
#         loop.run_until_complete(cleanup())
#         loop.shutdown_asyncgens()
#         loop.close()