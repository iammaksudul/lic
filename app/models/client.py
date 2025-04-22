 # app/models/client.py
from sqlalchemy import Column, Integer, String
from app.database import Base  # This import is now correct

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # Add other fields as necessary
