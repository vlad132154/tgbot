from aiogram import Bot, types, Dispatcher, executor
from pyowm import OWM

bot = Bot(token='Telegram bot API')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        owm = OWM('OpenWeatherMap API')
        mgr = owm.weather_manager()
        city = message["text"]
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')
        t = str(round(temperature['temp'])) + " °C"
        t0 = str(round(temperature['feels_like'])) + " °C"
        pressure = round(w.pressure['press'] / 1.333)
        wind = w.wind()
        if 337.5 < wind['deg'] <= 360 or wind['deg'] <= 22.5:
            direction = "северный"
        elif 22.5 < wind['deg'] <= 67.5:
            direction = "северо-восточный"
        elif 67.5 < wind['deg'] <= 112.5:
            direction = "восточный"
        elif 112.5 < wind['deg'] <= 157.5:
            direction = "юго-восточный"
        elif 157.5 < wind['deg'] <= 202.5:
            direction = "южный"
        elif 202.5 < wind['deg'] <= 247.5:
            direction = "юго-западный"
        elif 247.5 < wind['deg'] <= 292.5:
            direction = "западный"
        else:
            direction = "северо-западный"
        await message.reply(f"Погода в городе: {city}\n"
                            f"Температура: {t}\n"
                            f"Ощущается как: {t0}\n"
                            f"Влажность: {w.humidity}%\n"
                            f"Давление: {pressure} мм рт.ст.\n"
                            f"Скорость ветра: {wind['speed']} м/с \n"
                            f"Направление ветра: {direction}\n"
                            f"Хорошего дня!")
    except:
        await message.reply("Проверьте название города!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

