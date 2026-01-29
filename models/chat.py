from models.base import Base
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("User", back_populates="owned_chats")
    
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    members = relationship("ChatMember", back_populates="chat", cascade="all, delete-orphan")
