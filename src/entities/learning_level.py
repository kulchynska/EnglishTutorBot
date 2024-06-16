from typing import List
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningLevel(Base):
  __tablename__ = "learning_level"

  id: Mapped[int] = mapped_column(primary_key=True)
  level: Mapped[str] = mapped_column(String(512))
  units: Mapped[List["LearningUnit"]] = relationship(
    back_populates="level", cascade="all, delete-orphan"
  )

  path_id: Mapped[int] = mapped_column(ForeignKey("learning_path.id"))
  path: Mapped["LearningPath"] = relationship(back_populates="levels")

  def repr(self) -> str:
    return f"LearningLevel(id={self.id!r}, level={self.level!r})"
