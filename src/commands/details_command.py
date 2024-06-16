import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from entities.user_account import UserAccount
from entities.learning_path import LearningPath
from entities.learning_level import LearningLevel
from entities.learning_unit import LearningUnit

class DetailsCommandHandler:

  @staticmethod
  def convert_user(user: UserAccount, engine) -> str:
    choosen_path_id = user.path_id
    choosen_level_id = user.level_id
    choosen_unit_id = user.unit_id

    choosen_path = "Напрямок: не обрано" if choosen_path_id == None else "Напрямок: "
    choosen_level = "Рівень: не обрано" if choosen_level_id == None else "Рівень: "
    choosen_unit = "Тема: не обрано" if choosen_unit_id == None else "Тема: "


    with Session(engine, expire_on_commit=False) as session:
      print(choosen_path_id)
      if choosen_path_id != None:
        choosen_path_entity = session.get(LearningPath, choosen_path_id)
        choosen_path += f"{choosen_path_entity.name}"
      
      if choosen_level_id != None:
        choosen_level_entity = session.get(LearningLevel, choosen_level_id)
        choosen_level += f"{choosen_level_entity.level}"
      
      if choosen_unit_id != None:
        choosen_unit_entity = session.get(LearningUnit, choosen_unit_id)
        choosen_unit += f"{choosen_unit_entity.name}"


    answer = f"\n{choosen_path}\n{choosen_level}\n{choosen_unit}\n"
    return answer

  @staticmethod
  async def handle(message: Message, engine) -> None:
    user_id = message.from_user.id

    with Session(engine, expire_on_commit=False) as session:
      statement = select(UserAccount).where(UserAccount.user_id == f"{user_id}")

      try:
        user = session.scalars(statement).one()
      except NoResultFound:
        user = UserAccount(
          user_id=user_id
        )
        session.add_all([user])
        session.commit()

    user_details = DetailsCommandHandler.convert_user(user, engine)

    await message.answer(f"""
{html.bold(message.from_user.full_name)}:
{user_details}
""")
