import requests
from bs4 import BeautifulSoup

class Get_Music :
    def ___init__(self):
        self.soup = ""

    def get_page(self):
        url = "https://www.beatport.com/chart/best-new-house-november/650570"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36" }

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        self.soup = soup

    def get_songs(self):
        titles = []
        items = self.soup.find_all("span", class_="buk-track-primary-title")

        for item in items:
            title = item.decode_contents()
            titles.append(title)
        
        return titles

    def get_artists(self):
        artists = []
        items = self.soup.find_all("p", class_="buk-track-artists")

        # raw_items returns a list of lists, with a lot of whitespace
        raw_items = []
        for item in items:
            raw_items.append(item.findAll(text=True))

        # This function first strips all the white space from each of the lists in arr
        # It then return an item for each of the items (eliminate newline character)
        # Finally it remove the unnecesssary "," remaining
        def filter(arr):
            filtered_arr = [item.strip() for item in arr]
            filtered_arr = [item for item in filtered_arr if item]
            filtered_arr = [item for item in filtered_arr if item != ","]

            return filtered_arr

        for arr in raw_items:
            artists.append(filter(arr))

        # First list is one that just contains "Artists", so this checks and removes it
        if artists[0][0] == "Artists":
            del artists[0]

        return artists

    def music_list(self):
        clean_list = []
        self.get_page()
        titles = self.get_songs()
        artists = self.get_artists()

        for i in range(len(titles)):
            item = {"Title": titles[i], "Artists": artists[i]}
            clean_list.append(item)
        
        return clean_list
