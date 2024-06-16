from typing import List
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningTaskQuestionOption(Base):
  __tablename__ = "learning_task_question_option"

  id: Mapped[int] = mapped_column(primary_key=True)
  text: Mapped[str] = mapped_column(String(4096))
  is_answer: Mapped[bool] = mapped_column(Boolean)
  explanation: Mapped[str] = mapped_column(String(4096))

  question_id: Mapped[int] = mapped_column(ForeignKey("learning_task_question.id"))
  question: Mapped["LearningTaskQuestion"] = relationship(back_populates="options")

  def __repr__(self) -> str:
    return f"LearningTaskQuestion(id={self.id!r}, text={self.text!r})"
