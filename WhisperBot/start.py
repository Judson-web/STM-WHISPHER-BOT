from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup


# Start Message
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
	user = await bot.get_me()
	mention = user["mention"]
	await bot.send_sticker(msg.chat.id, "CAACAgQAAxkBAAEDMSphfknQOK-yM7r4AQoDDoS_Ujkx0AACJAoAAmT4KFFPVSBDOWWZECEE")
	await bot.send_message(
		msg.chat.id,
		Data.START.format(msg.from_user.mention, mention),
	)
