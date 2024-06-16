from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import Session
from sqlalchemy import event
from sqlalchemy.sql import text

from entities.base import Base
from entities.learning_level import LearningLevel
from entities.learning_path import LearningPath
from entities.learning_unit import LearningUnit
from entities.learning_task import LearningTask
from entities.learning_task_question import LearningTaskQuestion
from entities.learning_task_question_option import LearningTaskQuestionOption
from entities.user_account_questions import UserAccountQuestions

class DBManager:
  def __init__(self):
    self._engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/tgbot', echo=True)

  @property
  def engine(self):
      return self._engine

  def init_db(self):
    # Base.metadata.drop_all(self._engine)
    Base.metadata.create_all(self._engine)

