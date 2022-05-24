import web
import os
from config import Config as cfg
import random
import time

class Picture:
    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.url = self._get_pic_url()
        self.pic_path = self.get_pic_path()
        self._download_picture()


    def _get_pic_url(self):
        """Функция парсит страницу и вытягивает оттуда адрес исходника картинки в переменную pic_url"""
        params_dict = {'q': self.keyword,
                       'tbm': 'isch'}
        page = web.get_request(cfg.host, params=params_dict)
        soup = web.make_soup(page)

        pic_list = soup.find_all(class_='yWs4tf')
        id = self.get_random_id(1, len(pic_list) - 1)
        
        raw_pic = pic_list[id]

        if raw_pic.get('src') is not None:
            picture_url = raw_pic.get('src')
        else:
            while(raw_pic is None):
                id = self.get_random_id(1, len(pic_list) - 1)
                raw_pic = pic_list[id]
            picture_url = raw_pic.get('src')

        return picture_url


    def get_pic_path(self):
        """Функция берёт бинарник картинки из ссылки, записанной в поле 'url', запрашивает сгенерированное имя файла
                                                                и скачивает картинку в этот файл"""
        return self.get_random_filename()

    
    async def delete(self):
        if os.path.exists(self.pic_path):
            os.remove(self.pic_path)
        else:
            raise FileNotFoundError

    def _download_picture(self):
        self.picture_binary = web.get_request(self.url).content
        with open(self.pic_path, 'wb') as file:
            file.write(self.picture_binary)


    @staticmethod
    def get_random_id(a : int, b : int) -> int:
        id = random.randint(a, b)
        return id

    @staticmethod
    def get_random_filename() -> str:
        img_id = str(time.time_ns())[-6::]
        pic_path = cfg.parent_dirname+'\images\img'+img_id+'.jpg'
        return pic_path