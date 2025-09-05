import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Parser:      # Класс, использующий паттерн фабрика

    orders_list = [] # список предложений

    timedelta = 60     # время ожидания
    is_working = True  # работает ли парсер

    def start_checking_until_work(self, event): # работать пока is_working = True
        super().__init__()
        threading.Thread(target=self.work, args=[event]).start() # создаем поток со стабильным парсингом

    def work(self, event):
        self.orders_list = self.get_new_orders_list() # получение предложений

        while self.is_working: # цикл
            self.check_new_orders()
            t = 0
            while t != self.timedelta and self.is_working:    #
                self.is_working = -event.isSet()              #
                time.sleep(1)                                 #  эта часть отвечает за своевременное выключение
                t += 1                                        #

    def check_new_orders(self): # функция для поиска новых данных и их отправки на обработку
        new_orders_list = self.get_new_orders_list()

        if new_orders_list != self.orders_list and self.is_working:
            new_orders = [order for order in new_orders_list if order not in self.orders_list]
            self.orders_list += new_orders_list
            self.send_new_orders(self.orders_list)

    def get_new_orders_list(self): # кастомная функция для обновления списка новых предложений (возвращает)
        pass
    def send_new_orders(self, new_orders:list): # кастомная функция взаимодействия с новыми предложениями
        pass

    def fast_get_html(self, url:str):  # функция быстрого получения html кода, для динамических страниц
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Скрытый режим (без графического интерфейса)
        chrome_options.add_argument('--disable-gpu')  # Выключаем GPU ускорение (полезно для виртуальных сред)
        chrome_options.add_argument('--no-sandbox')  # Без песочницы (для Docker и некоторых VPS)
        chrome_options.add_argument('--window-size=1920x1080')  # Размер окна влияет на рендеринг страниц
        chrome_options.page_load_strategy = 'none'  # Минимальное ожидание загрузки страницы
        chrome_options.browser_version = "stable"

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.set_window_size(1920*10, 1080)
            try:
                driver.get(url)
                # Ждём минимальный период времени для завершения базовой загрузки
                wait = WebDriverWait(driver, 5)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body")))  # Дождаться хотя бы body-элемента

                while True:
                    old_page = driver.page_source
                    time.sleep(1)
                    if old_page == driver.page_source:
                        break
                driver.close()
                # Получаем исходный HTML-код страницы
                return old_page
            except Exception as e:
                print(f"Ошибка при получении HTML: {e}")
                return None