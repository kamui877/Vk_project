import requests
import json
import time


class Vk_agent:
    host_vk = 'https://api.vk.com/method/'

    def __init__(self, token_vk, vk_id, count=5, album='profile', vers='5.131'):
        self.params = {'v': vers, 'access_token': token_vk}
        self.vk_id = vk_id
        self.count = count
        self.album = album
        print("Получаем фото с вашей страницы...")
        time.sleep(1)

    def get_photo_likes_vk(self):
        vk_url = f"{self.host_vk}photos.get"
        params = {
            'owner_id': self.vk_id,
            'album_id': self.album,
            'rev': 0,
            'extended': 'likes',
            'photo_sizes': 0,
            'count': self.count
        }
        resp = requests.get(vk_url, params={**self.params, **params}).json()
        url_likes = {}
        info_dict = {}
        el = 0
        for val in resp['response']['items']:
            url_likes[val['sizes'][-1]['url']] = str(val['likes']['count'])
            el += 1
            info_dict[f'file name_{el}'] = f'{str(val["likes"]["count"])}.jpg'
            info_dict[f'size_{el}'] = {'height': val['sizes'][-1]['height'], 'width': val['sizes'][-1]['width']}
        with open('info.json', 'w', encoding='utf-8') as file:
            json.dump(info_dict, file, indent=2)
        return url_likes

    def upload(self, y_token):
        print('Фото получены')
        time.sleep(1)
        print('Начинаем загрузку фото на Яндекс Диск...')
        time.sleep(1)
        host = 'https://cloud-api.yandex.net:443'
        link = f'{host}/v1/disk/resources'
        link_1 = f'{host}/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {y_token}'}
        requests.put(link, headers=headers, params={'path': 'vk_photos'})
        for key, val in user_1.get_photo_likes_vk().items():
            params = {'path': f"/vk_photos/{val}", 'url': key}
            requests.post(link_1, headers=headers, params=params)
        print("Загрузка завершена!")


if __name__ == "__main__":
    vk_tok = input('Введит токен Вконтакте: ')
    id_vk = input('Введите id страницы Вконтакте: ')
    count_photo = int(input("Введите кол-во фотографий(по-умолчанию 5): "))
    print('\nprofile — фотографии профиля(по умолчанию),\
           \nwall — фотографии со стены,\
           \nsaved — сохраненные фотографии')
    album_1 = input('Введите название альбома: ')
    y_tok = input('Ведите токен Яндекс диска: ')
    user_1 = Vk_agent(vk_tok, id_vk, count_photo)
    user_1.upload(y_tok)
