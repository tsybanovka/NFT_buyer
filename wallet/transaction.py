import logging
from TonTools import TonCenterClient, Wallet
import asyncio
from tonsdk.contract.wallet import WalletVersionEnum
from tonsdk.utils import from_nano


class Transactions:
    @staticmethod
    async def _send_ton_async(mnemonics, destination_address, amount, payload, nano_amount, testnet, send_mode, version=WalletVersionEnum.v4r2):
        # Инициализируем TonCenter-клиент (для testnet или mainnet)
        provider = TonCenterClient(testnet=testnet)

        # Импортируем кошелёк из мнемоники
        wallet = Wallet(mnemonics=mnemonics, version=version, provider=provider)

        # Если передаётся сумма в нанотонах — конвертируем в TON
        if nano_amount:
            if isinstance(amount, str):
                amount = int(amount)
            amount = from_nano(amount, "ton")


        # Удаляем переносы строк из payload'а для читаемости лога
        clean_payload = payload.replace("\n", " ")

        # Выводим предупреждение с параметрами транзакции
        logging.warning(f'Sending {amount} TON to {destination_address} with payload: {clean_payload}')

        res = True
        try:
            res = await wallet.transfer_ton(destination_address=destination_address, amount=amount,
                                      message=payload, send_mode=send_mode) != 200
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as file:
                file.write(str(e)+f"\nargs:\n{mnemonics}\n{destination_address}\n{amount}\n{payload}\n{nano_amount}\n{testnet}\n{send_mode}\n{version}")

        # Отправляем средства через метод transfer_ton
        if res:
            logging.error("Transaction failed!")  # Ошибка при отправке
            return 0
        else:
            logging.info("Sending successful!")  # Успешная отправка
            return 1

    def send_ton(self, mnemonics, destination_address, amount, payload, nano_amount=True, version=WalletVersionEnum.v4r2, testnet=False, send_mode=0):
        # Запускаем асинхронную отправку синхронно через asyncio.run()
        result = asyncio.run(self._send_ton_async(
            mnemonics, destination_address, amount, payload, nano_amount, version, testnet, send_mode
        ))
        return result