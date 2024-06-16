from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class LearningPath(Base):
  __tablename__ = "learning_path"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(512))
  description: Mapped[str] = mapped_column(String(4096))

  levels: Mapped[List["LearningLevel"]] = relationship(
    back_populates="path", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"LearningPath(id={self.id!r}, name={self.name!r}, description={self.description!r})"

