import asyncio

from checking.parsing_fabric import Parser
import requests, json, time
from wallet.wallet import send_nft

class Getgems(Parser):

    timedelta = 1 # количество секунд между обновлениями страницы, 5 минут чтобы не было бана за ддос

    url = "https://getgems.io"

    API_KEY = '1756385924564-mainnet-10269054-r-WE7jzcrtfKUrK7eL0OnOhNdE4GQrzC8lqlUdP9nbKK2wBXAv'

    base_headers = {
            'accept': 'application/json',
            'Authorization': API_KEY,
            'Content-Type':"application/json"}
    limit = 10

    mnemonics = []

    operations = []

    def work(self, event):
        super().work(event)
        # Создаем список текущих активных задач
        tasks = asyncio.all_tasks()

        # Ждем завершения всех задач
        for task in asyncio.gather(*tasks):
            task.cancel()

    def get_new_orders_list(self): # Функция для получения списка данных от парсинга

        headers = self.base_headers
        url = f'https://api.getgems.io/public-api/v1/nfts/on-sale/EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N?limit={self.limit}'

        response = requests.get(url, headers=headers)

        if response.status_code // 100 == 2:
            response = json.loads(response.text)
            return response["response"]["items"]
        else:
            return False

    def send_new_orders(self, new_orders:list): # Функция для обработки новых данных от парсера

        def buy_nft(version: str, address: str): # функция для покупки nft

            headers = self.base_headers
            url = f'https://api.getgems.io/public-api/v1/nfts/buy-fix-price/{address}'
            body = json.dumps({"version": version})

            response = requests.post(url, headers=headers, data=body)

            if response.status_code // 100 == 2:
                response = json.loads(response.text)
                response = response["response"]["list"][0]
                send_nft(self.mnemonics, response["to"], int(response["amount"]), response["payload"], 1)
                # перевод на указанные в ответе реквизиты, цена = response['amount'], кошелек для перевода = response['amount'], в течение 9 часов

        headers = self.base_headers
        url = "https://api.getgems.io/public-api/v1/nfts/list"

        body = json.dumps({"addressList":[order["address"] for order in new_orders]})


        response = requests.post(url, headers=headers, data=body) # запрос на получение более точных данных о nft

        if response.status_code//100 == 2: # проверка на ошибки в запросе
            response = json.loads(response.text) # получение данных из ответа сервера

            for dt in response['response']['items']:       # поиск nft с фиксированной ценой покупки
                if dt["sale"]["type"] == "FixPriceSale":    # здесь также можно задать другие условия, например цена и др., имеются все данные о каждом nft
                    buy_nft(dt["sale"]["version"], dt["address"])   # покупка данного nft



