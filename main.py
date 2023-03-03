import time
import requests
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os


class TelegramBot:
    def __init__(self):
        self.need_check = None
        self.my_id = os.getenv("TELEGRAM_ID")

    def telegrambot(self):
        token = os.getenv("HOSPITAL_BOT_TOKEN")
        bot = Bot(token=token)
        dp = Dispatcher(bot=bot, storage=MemoryStorage())

        async def start_checking(s):
            while True:
                response = self.check()

                for main_message in response:
                    for _ in range(5):
                        await bot.send_message(self.my_id, main_message)

                await asyncio.sleep(300)

        executor.start_polling(dp, skip_updates=True, on_startup=start_checking)

    def check(self):
        return_response = []

        need_doctors = [
            "Эндокринолог",
            "Кардиолог"
        ]

        headers = {
            'Host': 'gorzdrav.spb.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://gorzdrav.spb.ru/service-free-schedule',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'close',
        }

        response = requests.get(
            'https://gorzdrav.spb.ru/_api/api/v2/schedule/lpu/1056/specialties',
            headers=headers
        )

        for doctor in json.loads(response.text)["result"]:
            if doctor["name"] in need_doctors:
                if int(doctor["countFreeTicket"]) > 0:
                    return_response.append(f"Есть запись у {doctor['name']}")

        return return_response


if __name__ == '__main__':
    telegrambot = TelegramBot()
    telegrambot.telegrambot()
