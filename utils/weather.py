import pyowm
from pyowm.commons import exceptions
from typing import Dict
from config.config import Config as cfg
import utils.web as web


owm = pyowm.OWM(cfg.pyowm_api_key, config=cfg.config_dict)
mgr = owm.weather_manager()


def _get_weather_props(city : str) -> Dict:
    observation = mgr.weather_at_place(city)
    
    weather_values = {
        'lon' : str(observation.location.lon),
        'lat' : str(observation.location.lat),
        'city' : city,
        'temp' : observation.weather.temperature('celsius')['temp'],
        'feels_like' : observation.weather.temperature('celsius')['feels_like'],
        'wind_speed' : round(observation.weather.wind('meters_sec')['speed']),
        'hum' : observation.weather.humidity,
        'status' : observation.weather.detailed_status,
        'pressure' : _round_pressure(observation.weather.pressure['press'])
    }

    return weather_values

    

def _round_pressure(pressure : int) -> float:
    rounded_pres = round(pressure * 0.750062, 1)
    return rounded_pres


def get_weather_status(city : str) -> str:
    try:
        weather_vals = _get_weather_props(city)
    except exceptions.APIResponseError:
        message = 'Я не знаю такого города :('
        return message

    message = f'''В городе {weather_vals['city']} сейчас {weather_vals['status']}. 
    Температура: {weather_vals['temp']}°С.
    Ощущается как: {weather_vals['feels_like']}°С.

    Влажность воздуха: {weather_vals['hum']}%. 
    Скорость ветра: {round(weather_vals['wind_speed'])} м/с.
    Атмосферное давление составляет {weather_vals['pressure']} мм.рт.ст.'''
    return message


def get_suntime_status(city : str) -> str:
    try:
        vals = _get_weather_props(city)
    except ValueError:
        answer_message = 'Я не знаю такого города :('
        return answer_message
    
    coords = dict([val for val in vals.items() if val[0] == 'lon' or val[0] == 'lat']) #'срезаем' словарь с данными о погоде; берём оттуда пары с координатами и создаём из них новый словарь
    
    suntimes = _get_suntime_info(coords)
    try:
        answer_message = f'''    Дата: {suntimes['date']}. 
    Рассвет - {suntimes['sunrise']}. 
    Закат - {suntimes['sunset']}'''
    except KeyError:
        answer_message = 'Упс, похоже вы ввели полярный город, в котором сейчас полярная ночь или полярный день.'
    
    return answer_message
    


def _get_suntime_info(params : Dict) -> Dict:
    """Данная функция формирует и отправляет GET запрос на сервер на основе полученных параметров,
                    ответ преобразует к удобному для работы виду и возвращает его"""
    headers = {'X-Yandex-API-Key': cfg.yand_api_key}

    answer = web.get_request(cfg.suntime_url, params, headers).json() # формирую get запрос, ответ перевожу в json
    try:
        answer = list(answer['forecast'].items())
        # беру dict_list всех пар словаря answer и преобразую в list для дальнейшей работы
    except KeyError:
        print('Error accured! Check logs.')
        return
    suntimes = dict([answer[0], answer[3], answer[4], answer[5],
                     answer[6]])  # 'выдёргиваю' из списка нужные пары и складываю новый словарь
    suntimes['date'] = _swap_year_day(suntimes['date'])
    return suntimes


def _swap_year_day(date : str) -> str:
    """Данная функция приводит дату к более читабельному виду
                (из формата YYYY-MM-DD преобразует в формат DD-MM-YYYY)
        Операция производится в 3 этапа:
        1)Строка разбивается на список из 3 элементов с разделителем '-'.
        2)Меняются местами 2 крайних элемента(день и год).
        3)Список собирается обратно в строку."""

    date = date.split('-')
    tmp = date[0]
    date[0] = date[2]
    date[2] = tmp
    date = '-'.join(date)
    return date
    
    
    

    