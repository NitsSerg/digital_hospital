from . import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience_years = Column(Integer, default=1)
    work_start = Column(String(8), nullable=True)  # hh:mm або hh:mm:ss
    work_end = Column(String(8), nullable=True)

    user = relationship("User", backref=db.backref("doctor_profile", cascade="all, delete", passive_deletes=True))

    def __repr__(self):
        return f"<Doctor {self.id}, spec={self.specialization}>"

    def set_work_start(self, start_str):
        self.work_start = start_str.strip()


