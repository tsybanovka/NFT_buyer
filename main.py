import asyncio
import threading
import time

from security.every_time_crypt import start_crypt
from security.data_interfice import get_data, end_work_with_data
from checking.getgems import Getgems


data, key, is_not_working = get_data() # получение данных кошелька

if is_not_working: # проверка на правильность ключа

    is_working = threading.Event() # Создания контроля над всеми подпотоками

    every_time_crypt = threading.Thread(target=start_crypt, args=[key, is_working]) # создание потока для постоянной смены ключа
    every_time_crypt.start() # запуск потока для постоянной смены ключа


    getgems = Getgems()
    getgems.send_new_orders(getgems.get_new_orders_list())
    time.sleep(1)
    is_working.set() # отключение всех потоков

    end_work_with_data(data) # завершение работы и запись данных кошелька
else:
    print("До свидания!")