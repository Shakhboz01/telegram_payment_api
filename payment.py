import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

#log
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# PRICES
PRICE_1 = types .LabeledPrice(label="Subscribe 500 rubles", amount=500 * 100)
PRICE_2 = types.LabeledPrice(label="Subscribe 40000 rubles", amount=40000 * 100)
PRICE_3 = types.LabeledPrice(label="Subscribe 80000 rubles", amount=80000 * 100)

@dp.message_handler(commands=['buy'])
async def buy(message: types.message):
    if config.PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Test payment')

    await bot.send_invoice(
        message.chat.id,
        title='Subscribe',
        description='Choose your subscription plan:',
        provider_token=config.PAYMENT_TOKEN,
        currency='rub',
        prices=[PRICE_1],  # Add the new prices to the list
        start_parameter='subscription',
        payload='Test invoice payload'
    )

    await bot.send_invoice(
        message.chat.id,
        title='Subscribe',
        description='Choose your subscription plan2:',
        provider_token=config.PAYMENT_TOKEN,
        currency='rub',
        prices=[PRICE_3],  # Add the new prices to the list
        start_parameter='subscription',
        payload='Test invoice payload'
    )

@dp.pre_checkout_query_handler(lambda query: True)
async  def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successfull_payment(message: types.Message):
    print('Success payment')
    payment_info: message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")
    await bot.send_message(message.chat.id, f"Payment for amount {message.successful_payment.total_amount // 100} rubles passed successfully")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
