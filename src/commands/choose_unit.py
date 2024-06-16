from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.learning_unit import LearningUnit
from entities.user_account import UserAccount

class ChooseUnitHandler:

  @staticmethod
  def convert_unit(unit):
    return f"/unit{unit.id} - {unit.name}\n{unit.description}\n"

  @staticmethod
  async def handle(message: Message, engine) -> None:
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == str(message.from_user.id))
      user = session.scalars(user_statement).one()

      user_level_id = user.level_id

      if user_level_id == None:
        await message.answer(f"Ви повинні спершу вибрати рівень.\n\n/choose_level - Виберіть рівень (PA, PB, PC).")
        return

      statement = select(LearningUnit).where(LearningUnit.level_id == user_level_id)
      units = session.scalars(statement).all()

    result = '\n'.join(list(map(ChooseUnitHandler.convert_unit, units)))

    await message.answer(f"Будь ласка, оберіть юніт:\n{result}")

  @staticmethod
  async def handle_choice(message: Message, engine) -> None:
    user_id = message.from_user.id
    text = message.text
    start = len("/unit")

    unit_id = text[start:]
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == f"{user_id}")
      user = session.scalars(user_statement).one()
      
      user_level_id = user.level_id
      if user_level_id == None:
        await message.answer(f"Ви повинні спершу вибрати рівень.\n\n/choose_level - Виберіть рівень (PA, PB, PC).")
        return

      user.unit_id = int(unit_id)

      session.commit()

    await message.answer(f"Ви обрали юніт.\n/choose_task - Виберіть завдання.\n\n/user_details - Показати обрані значення.")
