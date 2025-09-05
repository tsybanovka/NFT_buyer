from parsing_fabric import Parser
from ton_fragment.numbers.numbers import Numbers

class Fragment(Parser):

    timedelta = 300 # количество секунд между обновлениями страницы, 5 минут чтобы не было бана за ддос

    url = "https://fragment.com"

    def get_new_orders_list(self):
        return Numbers("sale", "listed").result

    def send_new_orders(self, new_orders):
        for order in new_orders:
            print("https://fragment.com/number/"+order["title"][1:].replace(" ", ""))

f = Fragment()
f.send_new_orders(f.get_new_orders_list())