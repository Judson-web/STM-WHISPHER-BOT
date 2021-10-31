import ast
import json
from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChosenInlineResult
)
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, PeerIdInvalid
from WhisperBot.database.whisper_sql import Whispers
from WhisperBot.database.users_sql import Users
from WhisperBot.database import SESSION
from WhisperBot.bot_users import check_for_users


main = [
    InlineQueryResultArticle(
        title="Valerie",
        input_message_content=InputTextMessageContent("നിങ്ങളുടെ സന്ദേശത്തിന്റെ അവസാനം അദ്ദേഹത്തിന്റെ @username അല്ലെങ്കിൽ ID എഴുതുക"),
        url="https://t.me/storytym",
        description="EX: @Pooi1Bot <Message> @username/id",
        thumb_url="https://telegra.ph/file/b83a6a2a8b4ef04b49bff.jpg",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("♥ Movie Group ♥", url="https://t.me/movieshub_group")]
            ]
        ),
    )
]


@Client.on_chosen_inline_result()
async def _chosen(bot: Client, result: ChosenInlineResult):
    if result.query == "":
        return
    sender = result.from_user.id
    specific = result.inline_message_id
    try:
        str_to_list = result.query.split(" ")
        message = " ".join(str_to_list[:-1])
        receiver = str_to_list[-1]
        to_user = await bot.get_users(receiver)
        receiver_id = to_user.id
        to_user = to_user.__str__()
        SESSION.add(Whispers(specific, message))
        q = SESSION.query(Users).get(sender)
        if q:
            q.target_user = to_user
        else:
            SESSION.add(Users(sender, to_user))
        SESSION.commit()
        await check_for_users([sender, receiver_id])
    except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, IndexError):
        message = result.query
        SESSION.add(Whispers(specific, message))
        SESSION.commit()


async def previous_target(sender):
    q = SESSION.query(Users).get(sender)
    if q and q.target_user is not None:
        target_user = q.target_user
        target_user = json.loads(target_user)
        receiver = target_user["id"]
        data_list = [sender, receiver]
        first_name = target_user["first_name"]
        try:
            last_name = target_user["last_name"]
            name = first_name + last_name
        except KeyError:
            name = first_name
        text1 = f"ഹായ് {name}, നിങ്ങൾക്കുള്ള രഹസ്യ സന്ദേശം! "
        text2 = "(താങ്കൾക്ക് മാത്രമേ വായിക്കാൻ കഴിയൂ)."
        mention = f"[{name}](tg://user?id={receiver})"
        results = [
              InlineQueryResultArticle(
                  title=text1,
                  input_message_content=InputTextMessageContent(
                      f"ഹായ് {mention}, നിങ്ങൾക്കുള്ള രഹസ്യ സന്ദേശം!" + " " + text2),
                  url="https://t.me/storytym",
                  description=text2,
                  thumb_url="https://telegra.ph/file/b83a6a2a8b4ef04b49bff.jpg",
                  reply_markup=InlineKeyboardMarkup(
                      [
                          [
                              InlineKeyboardButton(
                                  "🤫 Show Message 🤫",
                                  callback_data=str(data_list),
                              )
                          ]
                      ]
                  ),
              ),
              main[0]
        ]
    else:
        results = main
    return results


# Inline System
@Client.on_inline_query()
async def answer(bot: Client, query):
    query_list = query.query.split(" ")
    sender = query.from_user.id
    if query.query == "":
        await query.answer(
            results=main,
            switch_pm_text="🔒 Learn How to send Whispers",
            switch_pm_parameter="start"
        )
    elif len(query_list) == 1:
        sender = query.from_user.id
        results = await previous_target(sender)
        await query.answer(
            results,
            switch_pm_text="🔒 Learn How to send Whispers",
            switch_pm_parameter="start"
        )
    elif len(query_list) >= 2:
        mentioned_user = query_list[-1]
        try:
            mentioned_user = ast.literal_eval(mentioned_user)
        except (ValueError, SyntaxError):
            pass
        if isinstance(mentioned_user, str) and not mentioned_user.startswith("@"):
            sender = query.from_user.id
            results = await previous_target(sender)
            await query.answer(
                results,
                switch_pm_text="🔒 Learn How to send Whispers",
                switch_pm_parameter="start"
            )
            return
        try:
            target_user = await bot.get_users(mentioned_user)
            sender = query.from_user.id
            receiver = target_user.id
            data_list = [sender, receiver]
            if target_user.last_name:
                name = target_user.first_name + target_user.last_name
            else:
                name = target_user.first_name
            text1 = f"A whisper message to {name}"
            text2 = "Only he/she can open it."
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title=text1,
                        input_message_content=InputTextMessageContent(f"ഹായ് {target_user.mention}, നിങ്ങൾക്കുള്ള രഹസ്യ സന്ദേശം!" + " " + text2),
                        url="https://t.me/storytym",
                        description=text2,
                        thumb_url="https://telegra.ph/file/8a1ea7c9f16a3259f8e35.jpg",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "🤫 Show Message 🤫",
                                        callback_data=str(data_list),
                                    )
                                ]
                            ]
                        ),
                    )
                ],
                switch_pm_text="🔒 Learn How to send Whispers",
                switch_pm_parameter="start"
            )
            await check_for_users(receiver)
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid,  IndexError):
            sender = query.from_user.id
            results = await previous_target(sender)
            await query.answer(
                results,
                switch_pm_text="🔒 Learn How to send Whispers",
                switch_pm_parameter="start"
            )
    await check_for_users(sender)
