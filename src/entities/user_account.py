from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities.base import Base

class UserAccount(Base):
  __tablename__ = "user_account"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[str] = mapped_column(String(512), unique=True)

  path_id: Mapped[Optional[int]] = mapped_column(ForeignKey("learning_path.id"))
  level_id: Mapped[Optional[int]] = mapped_column(ForeignKey("learning_level.id"))
  unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("learning_unit.id"))

  # path: Mapped["LearningPath"] = relationship(back_populates="levels")

  def repr(self) -> str:
    return f"UserAccount(id={self.id!r}, user_id={self.user_id!r})"
