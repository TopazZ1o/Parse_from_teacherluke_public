import os
import requests
from bs4 import BeautifulSoup

os.makedirs("audio", exist_ok=True)

url = "https://teacherluke.co.uk"
link = f"/archive-of-episodes-1-149/"

response = requests.get(f'{url}/{link}')
# print(response)

bs = BeautifulSoup(response.text, "lxml")
# print(bs)

block = bs.find('div', class_ = 'entry-content')

for audio in block.find_all('a'):
    audio_link = audio.find_next('a').get('href')

    if 'youtube.com' in audio_link or 'youtube.be' in audio_link:
        continue

    storage = requests.get(audio_link).text
    necessary_bs = BeautifulSoup(storage, 'lxml')
    necessary_block = necessary_bs.find('div', class_ = 'entry-content')
    name_block = necessary_bs.find('h1', class_ = 'entry-title')
    if name_block:
        name_block_text = name_block.text
        name_block_editied = (name_block_text.replace('/', '.').replace('?', '.').
                              replace(':', '.').replace('*', '.').replace('"', '.').
                              replace('<', '.').replace('>', '.').replace('|', '.'))
        result_link = necessary_block.find('a').get('href')
        necessary_audio = requests.get(result_link).content

        with open(f'audio/{name_block_editied}.mp3', 'wb') as file:
            file.write(necessary_audio)

        print(f'аудио {name_block_editied}.mp3 скачалось')
    else:
        print("Элемент не найден")

