from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup


# Start Message
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
	user = await bot.get_me()
	mention = user["mention"]
	await bot.send_sticker(msg.chat.id, "CAACAgUAAxkBAAEDMRxhfkcp7OF4TI34TGaSWifmVkg4CAACpwIAAqUUIFQfwKQ46FbjHSEE")
	await bot.send_message(
		msg.chat.id,
		Data.START.format(msg.from_user.mention, mention),
	)
