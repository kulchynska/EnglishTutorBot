from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.learning_path import LearningPath
from entities.user_account import UserAccount

class ChoosePathHandler:

  @staticmethod
  def convert_path(path):
    return f"/path{path.id} - {path.name}\n{path.description}\n"

  @staticmethod
  async def handle(message: Message, engine) -> None:
    with Session(engine, expire_on_commit=False) as session:
      statement = select(LearningPath)
      pathes = session.scalars(statement).all()

    result = '\n'.join(list(map(ChoosePathHandler.convert_path, pathes)))

    await message.answer(f"Будь ласка, оберіть напрямок:\n{result}")

  @staticmethod
  async def handle_choice(message: Message, engine) -> None:
    user_id = message.from_user.id
    text = message.text
    start = len("/path")

    path_id = text[start:]
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == f"{user_id}")
      user = session.scalars(user_statement).one()
      user.path_id = int(path_id)

      session.commit()

    await message.answer(f"Ви обрали напрямок.\n/choose_level - Виберіть рівень (PA, PB, PC).\n\n/user_details - Показати обрані значення.")
