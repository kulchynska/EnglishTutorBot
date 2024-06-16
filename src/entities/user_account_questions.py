from typing import List
from typing import Optional
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class UserAccountQuestions(Base):
  __tablename__ = "user_account_questions"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[str] = mapped_column(ForeignKey("user_account.user_id"))

  learning_task_question_id: Mapped[int] = mapped_column(ForeignKey("learning_task_question.id"))
  is_answered: Mapped[bool] = mapped_column(Boolean)

  def repr(self) -> str:
    return f"UserAccountQuestions(id={self.id!r}, user_id={self.user_id!r}, is_answered={self.is_answered!r})"
