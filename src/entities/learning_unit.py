from typing import List
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningUnit(Base):
  __tablename__ = 'learning_unit'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(512))
  description: Mapped[str] = mapped_column(String(4096))

  tasks: Mapped[List["LearningTask"]] = relationship(
    back_populates = "unit", cascade="all, delete-orphan"
  )

  level_id: Mapped[int] = mapped_column(ForeignKey("learning_level.id"))
  level: Mapped["LearningLevel"] = relationship(back_populates="units")

  def __repr__(self) -> str:
    return f"LearningUnit(id={self.id!r}, name={self.name!r}, description={self.description!r})"
