from typing import List
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningTask(Base):
  __tablename__ = "learning_task"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(4096))
  questions: Mapped[List["LearningTaskQuestion"]] = relationship(
    back_populates="task", cascade="all, delete-orphan"
  )

  unit_id: Mapped[int] = mapped_column(ForeignKey("learning_unit.id"))
  unit: Mapped["LearningUnit"] = relationship(back_populates="tasks")

  def __repr__(self) -> str:
    return f"LearningTask(id={self.id!r}, questions={self.questions!r})"
