from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.learning_level import LearningLevel
from entities.user_account import UserAccount

class ChooseLevelHandler:

  @staticmethod
  def convert_level(level):
    return f"/level{level.id} - {level.level}\n"

  @staticmethod
  async def handle(message: Message, engine) -> None:
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == str(message.from_user.id))
      user = session.scalars(user_statement).one()

      user_path_id = user.path_id

      if user_path_id == None:
        await message.answer(f"Ви повинні спершу обрати напрямок.\n\n/choose_path - Виберіть напрямок (Front-end, Back-end etc).")
        return

      statement = select(LearningLevel).where(LearningLevel.path_id == user_path_id)
      levels = session.scalars(statement).all()

    result = '\n'.join(list(map(ChooseLevelHandler.convert_level, levels)))

    await message.answer(f"Будь ласка, оберіть рівень:\n{result}")

  @staticmethod
  async def handle_choice(message: Message, engine) -> None:
    user_id = message.from_user.id
    text = message.text
    start = len("/level")

    level_id = text[start:]
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == f"{user_id}")
      user = session.scalars(user_statement).one()
      user_path_id = user.path_id

      if user_path_id == None:
        await message.answer(f"Ви повинні спершу обрати напрямок.\n\n/choose_path - Виберіть напрямок (Front-end, Back-end etc).")
        return

      user.level_id = int(level_id)

      session.commit()

    await message.answer(f"Ви обрали рівень.\n/choose_unit - Виберіть юніт.\n\n/user_details - Показати обрані значення.")
