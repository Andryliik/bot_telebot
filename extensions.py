import requests
import json
from config import keys



class ConvertionException(Exception):               # обработчик ошибок
    pass

class MonetaryConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
            if quote == base:
                raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

            try:
                quote_ticker = keys[quote]
            except KeyError:
                raise ConvertionException(f'Не удалось обработать валюту {quote}')

            try:
                base_ticker = keys[base]
            except KeyError:
                raise ConvertionException(f'Не удалось обработать валюту {base}')

            try:
                amount = float(amount)
            except ValueError:
                raise ConvertionException(f'Не удалось обработать количество {amount}')

            url = f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"    #получаем результат конверта по API
            payload = {}
            headers = {"apikey": " "}
            response = requests.get(url, headers=headers, data=payload)
            d = json.loads(response.content)

            return d
