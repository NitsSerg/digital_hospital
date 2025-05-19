from . import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    appointment_time = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(String(20), default='scheduled')

    # Зв'язки
    patient = relationship("User", backref="appointments", foreign_keys=[patient_id])
    doctor = relationship("Doctor", backref="appointments", foreign_keys=[doctor_id])

    def __repr__(self):
        return f"<Appointment {self.id} | patient={self.patient_id}, doctor={self.doctor_id}>"
