import requests
import os
from pyfzf.pyfzf import FzfPrompt

from PIL import Image 

base_url = "https://api.mangadex.org"

title = "Attack on Titan"

r = requests.get(f"{base_url}/manga", params={"title": title})
fzf = FzfPrompt()
data = r.json()["data"]
choice = fzf.prompt([manga["attributes"]["title"]["en"] for manga in data])[0]
for manga in data:
    if choice == manga["attributes"]["title"]["en"]:
        chapters = fzf.prompt(range(1, int(manga["attributes"]["lastChapter"]) + 1), "--multi")
        chapters_list = requests.get(f"{base_url}/manga/{manga["id"]}/feed", params={"limit": int(manga["attributes"]["lastChapter"]), "translatedLanguage[]": ["en"]})
        chapters_data = chapters_list.json()["data"]

        for chapter in chapters:
            for i in range(1, len(chapters_data)):
                if str(chapter) == chapters_data[i]["attributes"]["chapter"]:
                    index = i
                    break
                index = ""
            if index:
                print(f"{base_url}/at-home/server/{chapters_data[int(index)]["id"]}")
                download_request = requests.get(
                    f"{base_url}/at-home/server/{chapters_data[int(index)]["id"]}",
                ).json()
            if download_request["chapter"]["data"]:
                download_data = download_request["chapter"]["data"]
                i = 1
                for image in download_data:
                    image_url = f"{download_request["baseUrl"]}/data/{download_request["chapter"]["hash"]}/{image}"
                    image_data = requests.get(image_url).content
                    manga_path = os.path.join(os.path.expanduser('~'), "Documents", choice)
                    if not os.path.exists(manga_path):
                        os.mkdir(manga_path)
                    chapter_path = os.path.join(manga_path, str(chapter))
                    if not os.path.exists(chapter_path):
                        os.mkdir(chapter_path)
                    image_path = os.path.join(chapter_path, f"{str(i)}.png")
                    if not os.path.exists(image_path):
                        with open(image_path, 'wb') as file:
                            file.write(image_data)
                    i += 1


