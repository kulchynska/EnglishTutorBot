from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.learning_task import LearningTask
from entities.learning_unit import LearningUnit
from entities.user_account import UserAccount
from entities.learning_task_question import LearningTaskQuestion
from entities.learning_task_question_option import LearningTaskQuestionOption
from entities.user_account_questions import UserAccountQuestions

class ChooseOptionHandler:

  @staticmethod
  def convert_question_option(option):
    return f"/option{option.id} - {option.text}\n"

  @staticmethod
  def get_question_options(question, engine):
    with Session(engine, expire_on_commit=False) as session:
      question_options_statement = select(LearningTaskQuestionOption).where(LearningTaskQuestionOption.question_id == question.id)
      options = session.scalars(question_options_statement).all()
      
    result = '\n'.join(list(map(ChooseOptionHandler.convert_question_option, options)))
    
    return f"Запитання: {question.text}\n{result}\n"

  @staticmethod
  async def handle(message: Message, engine) -> None:
    user_id = message.from_user.id
    text = message.text
    start = len("/option")

    option_id = text[start:]
    with Session(engine, expire_on_commit=False) as session:
      user_statement = select(UserAccount).where(UserAccount.user_id == str(message.from_user.id))
      user = session.scalars(user_statement).one()

      learning_task_question_option_statement = select(LearningTaskQuestionOption).where(LearningTaskQuestionOption.id == int(option_id))
      option = session.scalars(learning_task_question_option_statement).one()

      if option.is_answer == True:
        result = f"Правильна відповідь! {option.explanation}.\n\n"
        user_account_questions = UserAccountQuestions(
          user_id=str(user.user_id),
          learning_task_question_id=option.question.id,
          is_answered=True
        )
        session.add_all([user_account_questions])
        session.commit()
        
        user_questions_statement = select(UserAccountQuestions.learning_task_question_id).where(UserAccountQuestions.user_id == str(user.user_id)).where(UserAccountQuestions.is_answered == True)
        user_questions_ids = session.scalars(user_questions_statement).all()

        print("IDS: " + str(user_questions_ids))
        questions = option.question.task.questions
        next_question = ""
        for question in questions:
          if question.id not in user_questions_ids:
            next_question += ChooseOptionHandler.get_question_options(question, engine)
            break

        if next_question == "":
          # result += "\nВи відповіли на всі запитання даної вправи."
          print("TODO")
        else:
          result += next_question
      else:
        result = f"Неправильна відповідь! {option.explanation}"

    await message.answer(f"{result}")
