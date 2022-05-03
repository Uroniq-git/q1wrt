from tkinter import W
from typing import Type
from main import *
from aiogram import Bot, Dispatcher, executor, types
import config
from miscs import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

"""@dp.message_handler(commands=["pin"])
async def pin(message: types.Message):
    if isAdmin(message):
        messageText = message.text.replace("/pin ", "")
        chats = await getAllChats()
        for chat in chats:
            msg = await bot.forward_message(chat[0], message.chat.id, message_id=message.message_id)
            await bot.edit_message_text(msg.chat.id, msg.message_id, msg.text.replace("/pin ", ""))
            await bot.pin_chat_message(msg.chat.id, msg.message_id)
        
        await message.answer("Сообщение закреплено!")
    else: 
        await message.answer("У вас нет прав для данного дейтсвия")"""

@dp.message_handler(commands=["pin"])
async def pin(message: types.Message):
    if isAdmin(message):
        msgText = message.text.replace("/pin ", "").lower()
        adminsMessages = await getAdminsMessages(msgText)
        print(adminsMessages)
        for msg in adminsMessages:
            await bot.pin_chat_message(msg[0], msg[1])
    else: 
        await message.answer("У вас нет прав для данного дейтсвия")

@dp.message_handler(commands=["notmute"])
async def notMute(message: types.Message):
    if isAdmin(message):
        user = message.text.replace("/notmute ", "").replace("@", "")
        config.notMute.append(user)
        await message.answer("Пользователь добавлен в белый список")
    else: 
        await message.answer("У вас нет прав для данного дейтсвия")

@dp.message_handler(commands=["del"])
async def deleteMsg(message: types.Message):
    if isAdmin(message):
        msg = await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        await message.delete()
    else: 
        await message.answer("У вас нет прав для данного дейтсвия")

@dp.message_handler(commands=["banword"])
async def addBanWord(message: types.Message):
    if isAdmin(message):
        words = message.text.replace("/banword ", "").lower().split(' ')
        for word in words:
            config.banWords.append(word)
        await message.answer("Слова(о) добавлены(о) в чёрный список")
    else: 
        await message.answer("У вас нет прав для данного дейтсвия")

@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    if isAdmin(message):
        banUser = message.reply_to_message.from_user.id
        config.banned.append(banUser)

        chats = await getAllChats()
        for chat in chats:
            try:
                await bot.ban_chat_member(chat[0], banUser)
            except:
                pass
    else:
        pass

@dp.message_handler()
async def txt(message: types.Message):
    await addChatToDB(message)
    await addAdminsMsgToDb(message)
    messages = message.text.lower().split(" ")
    for msg in messages:
        if msg in config.banWords:
            if message.from_user.username in config.notMute:
                pass
            else:
                await message.delete()
    
    if message.forward_from:
        if message.from_user.username in config.notMute:
            pass
        else:
            await message.delete()


@dp.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
async def delete(message: types.Message):
    newUsers = message.new_chat_members
    for user in newUsers:
        if user.id in config.banned:
            await bot.ban_chat_member(message.chat.id, user.id)
    await bot.delete_message(message.chat.id, message.message_id)