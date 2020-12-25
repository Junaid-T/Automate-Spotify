import requests
import json

from secrets import database_link
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient(database_link)
        self.db = self.client.get_database("Spotify")
        self.collection = self.db.Music
    
    def get_music(self):
        previous_titles = []
        test_music_get = self.collection.find({}, {"Title": 1, "Artists": 1})
        for x in test_music_get:
            x.pop("_id")
            previous_titles.append(x)
        return previous_titles
    
    def push_music(self, missed_list):
        self.collection.insert_many(missed_list)
    
    def delete_music(self):
        self.collection.delete_many({})