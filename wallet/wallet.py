import json, asyncio
from wallet.wallet_utils import *
from wallet.transaction import *


def send_nft(mnemonics:list, destination_address:str, amount:int, payload:str, is_testnet=0):
    try:
        asyncio.run(Transactions()._send_ton_async(mnemonics, destination_address, amount, payload, True, is_testnet, 1))
    except:
        pass


#if __name__ == '__main__':
    Wallet = WalletUtils() # создание экземпляра класса с кошельком
    #Wallet.create_wallet(save_to_file=True, save_dir="../new_wallet.txt") # создание кошелька
    #Wallet.create_wallet(save_to_file=True, save_dir="../wallet_data.txt")  # создание кошелька

    #with open("../new_wallet.txt", "r") as f:     #
    #    mnemonics = json.load(f)['mnemonics']      #   Загрузка сид фраз
#
    #Wallet.init_wallet(mnemonics=mnemonics, testnet=True)  # инициализация кошелька

    #with open("../wallet_data.txt", "r") as f:     #
    #    mnemonics = json.load(f)['mnemonics']      #   Загрузка сид фраз
#
    #Wallet.init_wallet(mnemonics=mnemonics, testnet=True)  # инициализация кошелька

    # Выше производилось создание и инициализация кошельков, далее - транзакция между этими двумя кошельками
    # ВАЖНО - не забыть пополнить на тестовый адрес кошельки - бот для пополнения - @testgiver_ton_bot

    # проверка работы транзакции - https://testnet.tonviewer.com/
    #with open("../wallet_data.txt", "r") as f:     #
    #    mnemonics = json.load(f)['mnemonics']      #   Загрузка сид фраз
#
    #destination_address = "0QAH4ZmH7y4l6G_TSF_dUpcX9NNf_Tjs4uSdrS2GpVYfV84I"
#
    #asyncio.run(Transactions()._send_ton_async(mnemonics, destination_address, 10, "Hello world of TON", True, 1, 1))
    # прошлая команда - транзакция, которая переведёт 1TON на второй кошелёк, с учётом комиссии, она берётся с кошелька отправителя, и подписью <<Hello world of TON>>
    # данная транзакция использует "ненастоящие тоны, поэтому можно баловаться и эксперементировать сколько душе угодно
