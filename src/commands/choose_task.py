from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.learning_task import LearningTask
from entities.learning_unit import LearningUnit
from entities.user_account import UserAccount
from entities.learning_task_question import LearningTaskQuestion
from entities.learning_task_question_option import LearningTaskQuestionOption

class ChooseTaskHandler:

  @staticmethod
  def convert_task(task):
    return f"/task{task.id} - {task.name}\n"

  @staticmethod
  def convert_question_option(option):
    return f"/option{option.id} - {option.text}\n"

  @staticmethod
  def get_question_options(question, engine):
    with Session(engine, expire_on_commit=False) as session:
      question_options_statement = select(LearningTaskQuestionOption).where(LearningTaskQuestionOption.question_id == question.id)
      options = session.scalars(question_options_statement).all()
      
    result = '\n'.join(list(map(ChooseTaskHandler.convert_question_option, options)))
    
    return f"Запитання: {question.text}\n{result}\n"

  @staticmethod
  async def handle(message: Message, engine) -> None:
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == str(message.from_user.id))
      user = session.scalars(user_statement).one()

      user_unit_id = user.unit_id

      if user_unit_id == None:
        await message.answer(f"Ви повинні спершу обрати тему.\n\n/choose_unit - Виберіть тему.")
        return

      task_statement = select(LearningTask).where(LearningTask.unit_id == user.unit_id)
      tasks = session.scalars(task_statement).all()

    result = '\n'.join(list(map(ChooseTaskHandler.convert_task, tasks)))

    await message.answer(f"Будь ласка, виберіть завдання:\n{result}")

  @staticmethod
  async def handle_choice(message: Message, engine) -> None:
    user_id = message.from_user.id
    text = message.text
    start = len("/task")

    task_id = text[start:]
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == str(user_id))
      user = session.scalars(user_statement).one()
      
      user_unit_id = user.unit_id
      if user_unit_id == None:
        await message.answer(f"Ви повинні спершу обрати тему.\n\n/choose_unit - Виберіть тему.")
        return

      learning_task_question_statement = select(LearningTaskQuestion).where(LearningTaskQuestion.task_id == int(task_id))
      questions = session.scalars(learning_task_question_statement).all()
      
      session.commit()

    answer = ChooseTaskHandler.get_question_options(questions[0], engine)
    await message.answer(f"{answer}")
