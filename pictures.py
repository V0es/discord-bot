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
        id = self._get_random_id(1, len(pic_list) - 1)
        
        raw_pic = pic_list[id]

        if raw_pic.get('src') is not None:
            picture_url = raw_pic.get('src')
        else:
            while(raw_pic is None):
                id = self._get_random_id(1, len(pic_list) - 1)
                raw_pic = pic_list[id]
            picture_url = raw_pic.get('src')

        return picture_url


    def get_pic_path(self):
        """Функция берёт бинарник картинки из ссылки, записанной в поле 'url', запрашивает сгенерированное имя файла
                                                                и скачивает картинку в этот файл"""
        return self._get_random_filename()

    
    async def delete(self):
        """Функция, которая асинхронно удаляет файл с картинкой"""
        if os.path.exists(self.pic_path):
            os.remove(self.pic_path)
        else:
            raise FileNotFoundError

<<<<<<< HEAD
    async def _download_picture(self):
        """"""
=======
    def _download_picture(self):
        """Функция вытягивает бинарник картинки из ответа на GET-запрос и записывает его в файл"""
>>>>>>> 620d99e7910b6bc6117ba707e8489e882f10096e
        self.picture_binary = web.get_request(self.url).content
        with open(self.pic_path, 'wb') as file:
            file.write(self.picture_binary)


    @staticmethod
<<<<<<< HEAD
    def get_random_id(a : int, b : int) -> int:
        """Возвращает рандомное число, которые будет испольлзоваться как id"""

=======
    def _get_random_id(a : int, b : int) -> int:
        """Функция просто возвращает рандомное число, которое будет использоваться как id"""
>>>>>>> 620d99e7910b6bc6117ba707e8489e882f10096e
        id = random.randint(a, b)
        return id

    @staticmethod
<<<<<<< HEAD
    def get_random_filename() -> str:
        """Генерирует уникальнрое имя файла на основе текущего времени"""

=======
    def _get_random_filename() -> str:
        """Функция возвращает путь к картинке и генерирует для неё рандомное имя (на основе текущего времени)"""
>>>>>>> 620d99e7910b6bc6117ba707e8489e882f10096e
        img_id = str(time.time_ns())[-6::]
        pic_path = '.\images\img'+img_id+'.jpg'
        return pic_path