import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import time

# Bot tokeni
TOKEN = "7562689551:AAF_CGnoVNT4VSPH-yuATwTQOA8cEdbGMEI"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Kanallar ma'lumotlari
CHANNELS = [
    {"name": "1-kanal", "url": "https://t.me/+ES6RKiQkRWBkZTUy"},
    {"name": "2-kanal", "url": "https://t.me/+wig3NGYpZ_Y2MjYy"}
]

# Loggingni yoqish
logging.basicConfig(level=logging.INFO)

# Video kodlari va ularga mos keladigan video fayllar URL
VIDEO_FILES = {
    "1": "https://t.me/video_bor_bot_kod/3",
    "2": "https://t.me/video_bor_bot_kod/5",
    "3": "https://t.me/video_bor_bot_kod/6",
    "4": "https://t.me/video_bor_bot_kod/7",
    "5": "https://t.me/video_bor_bot_kod/8",
    "6": "https://t.me/video_bor_bot_kod/9",
    "7": "https://t.me/video_bor_bot_kod/10",
    "8": "https://t.me/video_bor_bot_kod/11",
    "9": "https://t.me/video_bor_bot_kod/12",
    "10": "https://t.me/video_bor_bot_kod/13"
}

# Start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🖐 𝗦𝗮𝗹𝗼𝗺, {user_name}!\n"
        "🔍 𝗙𝗶𝗹𝗺 𝗸𝗼𝗱𝗶𝗻𝗶 𝗸𝗶𝗿𝗶𝘁𝗶𝗻𝗴:\n\n"
        "Quyidagi tugmalar orqali kanallarimizga obuna bo‘ling. \n"
        "Obuna bo‘lgandan so‘ng, 'Tekshirish' tugmasini bosing."
    )

    # Tugmalarni yaratish
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        keyboard.add(InlineKeyboardButton(f"🔗 Obuna bo‘ling: {channel['name']}", url=channel['url']))
    keyboard.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_subscription"))

    # Xabarni yuborish
    sent_message = await message.answer(welcome_text, reply_markup=keyboard)
    return sent_message.message_id

# Tekshirish tugmasi bosilganda
@dp.callback_query_handler(lambda call: call.data == "check_subscription")
async def verify_subscription(call: types.CallbackQuery):
    # Kanallar va tekshirish tugmasini o'chirish
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # Kodlar tugmasi va xabarni yuborish
    user_name = call.from_user.first_name
    welcome_text_after_check = (
        f"🖐 𝗦𝗮𝗹𝗼𝗺, {user_name}!\n"
        "🔍 𝗙𝗶𝗹𝗺 𝗸𝗼𝗱𝗶𝗻𝗶 𝗸𝗶𝗿𝗶𝘁𝗶𝗻𝗴:\n\n"
        "Quyidagi tugmani bosing va film kodini oling."
    )
    
    # Tugma: Film kodlari
    keyboard_kodlar = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📥 Film kodlari", url="https://t.me/gilosHUB_kod")
    )

    # Xabarni yuborish
    await call.message.answer(welcome_text_after_check, reply_markup=keyboard_kodlar)

# Kodlarni tekshirish va video yuborish
@dp.message_handler(lambda message: message.text in VIDEO_FILES)
async def send_video(message: types.Message):
    code = message.text.strip()
    
    if code in VIDEO_FILES:
        video_url = VIDEO_FILES[code]

        # Video faylni yuborish
        await message.answer_video(video_url)
    else:
        await message.answer("Bunday kod mavjud emas. Iltimos, to'g'ri kodni kiriting.")

# Botni doimiy ishlashga moslash
async def main():
    while True:
        try:
            logging.info("Bot ishga tushdi.")
            await dp.start_polling()
        except Exception as e:
            logging.error(f"Botda xatolik: {e}")
            time.sleep(15)  # Xatolikdan so‘ng 15 soniya kutib qayta urinadi

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
