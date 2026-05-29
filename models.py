from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Screening(Base):
    __tablename__ = "screenings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start_time = Column(String)
    total_seats = Column(Integer)
    
    reservations = relationship("Reservation", back_populates="screening", cascade="all, delete-orphan")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    screening_id = Column(Integer, ForeignKey("screenings.id"))
    seat_number = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    screening = relationship("Screening", back_populates="reservations")