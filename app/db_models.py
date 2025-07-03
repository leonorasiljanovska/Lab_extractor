from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from app.db import Base
import hashlib


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)  # hashed id string
    gender = Column(String, nullable=True)
    hospital_name = Column(String, nullable=True)
    # Relationship to lab tests
    lab_tests = relationship("LabTest", back_populates="patient")

    @staticmethod
    def generate_id(name: str, surname: str) -> str:
        # Example: SHA256 hash of "Name Surname"
        full_str = f"{name.strip().lower()} {surname.strip().lower()}"
        return hashlib.sha256(full_str.encode()).hexdigest()


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    parameter = Column(String)
    value = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    reference_min = Column(Float, nullable=True)
    reference_max = Column(Float, nullable=True)
    reference_range = Column(String, nullable=True)
    status = Column(String, nullable=True)
    test_date = Column(DateTime, nullable=False)
    patient = relationship("Patient", back_populates="lab_tests")
