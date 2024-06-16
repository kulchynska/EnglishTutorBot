import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from commands.start_command import StartCommandHandler
from commands.choose_path import ChoosePathHandler
from commands.choose_level import ChooseLevelHandler
from commands.choose_unit import ChooseUnitHandler
from commands.details_command import DetailsCommandHandler
from commands.choose_task import ChooseTaskHandler
from commands.choose_option import ChooseOptionHandler

from db.db_manager import DBManager

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

db_manager = DBManager()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await StartCommandHandler.handle(message, db_manager.engine)

@dp.message(F.text == "/user_details")
async def user_details_handler(message: Message) -> None:
  await DetailsCommandHandler.handle(message, db_manager.engine)

@dp.message(F.text == "/choose_path")
async def choose_path_handler(message: Message) -> None:
  await ChoosePathHandler.handle(message, db_manager.engine)

@dp.message(F.text.startswith("/path"))
async def handle_path_choice(message: Message) -> None:
  await ChoosePathHandler.handle_choice(message, db_manager.engine)

@dp.message(F.text == "/choose_level")
async def choose_level_handler(message: Message) -> None:
  await ChooseLevelHandler.handle(message, db_manager.engine)

@dp.message(F.text.startswith("/level"))
async def handle_level_choice(message: Message) -> None:
  await ChooseLevelHandler.handle_choice(message, db_manager.engine)

@dp.message(F.text == "/choose_unit")
async def choose_unit_handler(message: Message) -> None:
  await ChooseUnitHandler.handle(message, db_manager.engine)

@dp.message(F.text.startswith("/unit"))
async def handle_unit_choice(message: Message) -> None:
  await ChooseUnitHandler.handle_choice(message, db_manager.engine)

@dp.message(F.text == "/choose_task")
async def test_handler(message: Message) -> None:
  await ChooseTaskHandler.handle(message, db_manager.engine)

@dp.message(F.text.startswith("/task"))
async def test_handler(message: Message) -> None:
  await ChooseTaskHandler.handle_choice(message, db_manager.engine)

@dp.message(F.text.startswith("/option"))
async def test_handler(message: Message) -> None:
  await ChooseOptionHandler.handle(message, db_manager.engine)

@dp.message()
async def test(message: Message) -> None:
  await message.answer(f"{message.text}", reply_markup=ReplyKeyboardRemove())

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
  db_manager.init_db()
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
