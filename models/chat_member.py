from models.base import Base
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"), primary_key=True, nullable=False)
    chat = relationship("Chat", back_populates="members")
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    user = relationship("User", back_populates="memberships")
    
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    