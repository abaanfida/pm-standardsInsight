from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Standard(Base):
    __tablename__ = "standards"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String)
    file_path = Column(String)

    sections = relationship("Section", back_populates="standard")

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    standard_id = Column(Integer, ForeignKey("standards.id"))
    section_number = Column(String)
    title = Column(String)
    content = Column(Text)

    standard = relationship("Standard", back_populates="sections")
