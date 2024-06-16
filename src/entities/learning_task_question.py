from typing import List
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningTaskQuestion(Base):
  __tablename__ = "learning_task_question"

  id: Mapped[int] = mapped_column(primary_key=True)
  text: Mapped[str] = mapped_column(String(4096))

  options: Mapped[List["LearningTaskQuestionOption"]] = relationship(
    back_populates="question", cascade="all, delete-orphan"
  )

  task_id: Mapped[int] = mapped_column(ForeignKey("learning_task.id"))
  task: Mapped["LearningTask"] = relationship(back_populates="questions")

  def __repr__(self) -> str:
    return f"LearningTaskQuestion(id={self.id!r}, text={self.text!r})"
