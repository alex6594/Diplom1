import json
from pprint import pprint
import requests
import os
import time
from tqdm import tqdm
with open('token.txt', 'r') as file_token:
    token = file_token.read().strip()
with open('version.txt', 'r') as version_file:
    version = version_file.read().strip()


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_name, version_name):
        self.params = {
            'access_token': token_name,
            'v': version_name
        }

    # noinspection PyGlobalUndefined
    def photos(self):
        global j_file
        command_url = self.url + "photos.get"
        command_url_params = {
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        req = requests.get(command_url, params={**self.params, **command_url_params}).json()
        photo_inf = []
        for value in req['response']['items']:
            photo_dict = {
                'file_name': f"{value['likes']['count']}_{value['date']}.jpg",
            }
            for max_size in value['sizes']:
                photo_size = {
                    'size': f"{max_size['type']}"
                }
                photo_dict.update(photo_size)
            photo_inf.append(photo_dict)
            j_file = json.dumps(photo_inf)
        return j_file

    def file_download(self):
        command_url = self.url + "photos.get"
        command_url_params = {
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        req = requests.get(command_url, params={**self.params, **command_url_params}).json()
        photos_url = []
        for files in req['response']['items']:
            photos_url.append(files['sizes'][-1]['url'])
            for img_download in photos_url:
                url = requests.get(img_download)
                img_option = open(f"{files['likes']['count']}_{files['date']}.jpg", 'wb')
                img_option.write(url.content)
                img_option.close()
        return


class YandexCLoud:

    def __init__(self, token_file: str):
        self.token = token_file

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
                }

    def file_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def file_upload(self, disk_file_path: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str, ydpath: str):
        os.path.basename(file_path)
        href_json = self.file_upload(disk_file_path=ydpath)
        href = href_json['href']
        requests.put(href, data=open(file_path, 'rb'))

        return ''


vk_client = VK(token, version)
pprint(vk_client.photos())
vk_client.file_download()

if __name__ == '__main__':
    file_nums = int(input('Введите количество загружаемых файлов: '))
    token = input("Введите токен яндекса: ")
    uploader = YandexCLoud(token)
    path_to_file = input("Введите путь к файлу: ")
    file_way = path_to_file
    yd_path_to_file = input("Введите название директории на яндекс диске: ")
    yd_path = yd_path_to_file
    files_list = []
    timing = []
    for timelaps in range(file_nums):
        timing.append(timelaps)
    for file in range(file_nums):
        file_name = input("Введите имя файла с расширением: ")
        files_list.append(file_name)
    for timer, file_now in zip(tqdm(timing), files_list):
        path_to_file = os.path.abspath(os.path.join(path_to_file, file_now))
        yd_path_to_file = yd_path_to_file + "/" + file_now
        print(uploader.upload(path_to_file, yd_path_to_file))
        time.sleep(3)
        path_to_file = file_way
        yd_path_to_file = yd_path
