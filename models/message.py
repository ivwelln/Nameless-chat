from models.base import Base
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
    chat = relationship("Chat", back_populates="messages")
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="messages")
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    