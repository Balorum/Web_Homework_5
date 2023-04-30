import platform
from time import time, ctime
import aiohttp
import asyncio
import sys

date_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Now": "11",
    "Dec": "12",
}


async def get_responce(date, beuty_currency):

    async with aiohttp.ClientSession() as session:
        url = "https://api.privatbank.ua/p24api/exchange_rates?json&date=" + date
        print(f"Starting {url}")
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    beautiful_result = beautifuler(result, beuty_currency)
                    return beautiful_result
                else:
                    print(f"Error status: {response.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            print(f"Connection error: {url}", str(err))


def main(counter, currency):
    beuty_currency = spliting_currency(currency)
    result = []
    for i in range(counter):
        date = get_date(i)
        result.append(asyncio.run(get_responce(date, beuty_currency)))
    print(result)


def spliting_currency(currency: str):
    upper_currency = ["EUR", "USD"]
    if currency == "":
        return upper_currency
    else:
        list_currency = currency.split(" ")
        for i in list_currency:
            upper_currency.append(i.upper())
    return upper_currency


def get_date(i):
    current_time = time() - 86400 * i
    splited_date = ctime(current_time).split(" ")
    full_date = (
        splited_date[2] + "." + date_dict[splited_date[1]] + "." + splited_date[4]
    )
    return full_date


def beautifuler(result, currency):
    beautiful_kurs = {}
    external = {}
    for j in result["exchangeRate"]:
        for i in currency:
            if j["currency"] == i:
                sale_purches = {}
                sale_purches["sale"] = j["saleRateNB"]
                sale_purches["purches"] = j["purchaseRateNB"]
                beautiful_kurs[i] = sale_purches
        external[result["date"]] = beautiful_kurs
    return external


def inputing():
    if int(sys.argv[1]) >= 10:
        print("Ну просили же - не більше 10 днів :(")
        exit(0)
    counter = int(sys.argv[1])
    if len(sys.argv) >= 3:
        currency = " ".join(sys.argv[2::])
    main(counter, currency)


# Приклад роботи: Web_Homework_5.py 3 cHf GeL
if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    inputing()
