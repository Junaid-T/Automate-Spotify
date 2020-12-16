import requests
from datetime import date
import json

from secrets import user_id
from refresh import Refresh
from get_music import Get_Music


class Main:
    def __init__(self):
        self.token = Refresh().refresh()
        self.music = Get_Music().music_list()
        self.user_id = user_id
    
    def create_playlist(self):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        request_body = json.dumps(
          {"name": date.today().strftime("%d/%m/%Y")}
        )

        headers = {
            "Content-Type":"application/json",
            "Authorization":f"Bearer {self.token}"
        }

        response = requests.post(url, data=request_body, headers=headers)

        response_json = response.json()
        playlist_id = response_json["id"]
        print("Creating playlist...")
        return playlist_id
    
    # TO SELF - SEARCH BY TRACK AND ITERATE THROUGH IF ARTIST MATCHES
    def search_music(self):
        uri_list = []
        missed_list = []
        for song in self.music:
            track = song["Title"]
            artist = song["Artists"]

            url = f"https://api.spotify.com/v1/search?q=track:{track}%20artist:{artist}&type=track"

            headers = {
                "Content-Type":"application/json",
                "Authorization": f"Bearer {self.token}"
            }

            response = requests.get(url, headers=headers)
            response_json = response.json()

            if len(response_json["tracks"]["items"]) > 0:
                uri = response_json["tracks"]["items"][0]["uri"]
                uri_list.append(uri)
            else:
                missed_list.append({"Title": track, "Artists": artist})
        print("Finding music...")
        return uri_list

    # DONE BY PASSING THE URI'S INTO THE BODY - NOT WORKING - NEED TO FIX
    # def add_music(self):
    #     playlist_id = self.create_playlist()
    #     uri_list = self.search_music()

    #     url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    #     request_body = json.dumps({"uris": f"{uri_list}"})

    #     headers = {
    #     "Content-Type":"application/json",
    #     "Authorization": f"Bearer {self.token}"
    #     }

    #     requests.post(url, data=request_body, headers=headers)
    #     print("Adding music...")

    def add_music(self):
        playlist_id = self.create_playlist()
        uri_list = self.search_music()

        combinedString = ",".join(uri_list)

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={combinedString}"

        headers = {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {self.token}"
        }

        requests.post(url, headers=headers)
        print("Adding music...")

Main().add_music()

