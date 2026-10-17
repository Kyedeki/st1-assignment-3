from datetime import datetime

import pytest

from smartcare import data_store
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

def test_find_patient():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    patient = patient_service.register_patient(
        "P1",
        "Alex Example",
    )
    found_patient = patient_service.find_patient("P1")
    assert found_patient is patient

def test_find_practitioner():
    data_store = SmartCareDataStore()
    practitioner_service = PractitionerService(data_store)

    practitioner = practitioner_service.register_practitioner(
        "D1",
        "Taylor Example",
        "General",

    )
    found_practitioner = practitioner_service.find_practitioner("D1")
    assert found_practitioner is practitioner

def test_find_unknown_practitioner():
    data_store = SmartCareDataStore()
    practitioner_service = PractitionerService(data_store)

    with pytest.raises(LookupError):
        practitioner_service.find_practitioner("D2")

def test_find_practitioner_with_blank_id():
    data_store = SmartCareDataStore()
    practitioner_service = PractitionerService(data_store)

    with pytest.raises(ValueError):
        practitioner_service.find_practitioner(" ")

def test_find_unknown_patient():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    with pytest.raises(LookupError):
        patient_service.find_patient("P2")

def test_find_patient_with_blank_id():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    with pytest.raises(ValueError):
        patient_service.find_patient(" ")

def test_cancel_appointment():
    data_store = SmartCareDataStore()

    appointment_service = AppointmentService(data_store)
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")
    practitioner = practitioner_service.register_practitioner("D1", "Taylor Example", "General")
    appointment = appointment_service.book_appointment("A1","P1","D1", datetime(2026,10,1,9),)
    canceled_appointment = appointment_service.cancel_appointment("A1")

    assert canceled_appointment is appointment
    assert appointment.status == AppointmentStatus.CANCELLED
    assert data_store.find_appointment("A1") is appointment

def test_cancel_appointment_with_blank_id():
    data_store = SmartCareDataStore()
    appointment_service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(" ")

def test_cancel_appointment_twice():
    data_store = SmartCareDataStore()

    appointment_service = AppointmentService(data_store)
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")
    practitioner = practitioner_service.register_practitioner("D1", "Taylor Example", "General")
    appointment = appointment_service.book_appointment("A1","P1","D1", datetime(2026,10,1,9),)
    appointment2 = appointment_service.cancel_appointment("A1")
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A1")

def test_cancel_completed_appointment():
    data_store = SmartCareDataStore()

    appointment_service = AppointmentService(data_store)
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")
    practitioner = practitioner_service.register_practitioner("D1", "Taylor Example", "General")
    appointment = Appointment("A1",patient,practitioner,datetime(2026,10,1,9),AppointmentStatus.COMPLETED)
    data_store.add_appointment(appointment)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A1")
    assert appointment.status == AppointmentStatus.COMPLETED
    assert data_store.find_appointment("A1") is appointment

def test_find_practitioner_with_spaces():
    data_store = SmartCareDataStore()
    practitioner_service = PractitionerService(data_store)

    practitioner = practitioner_service.register_practitioner("D1", "Taylor Example", "General")
    found_practitioner = practitioner_service.find_practitioner(" D1 ")

    assert found_practitioner is practitioner

def test_find_patitient_with_spaces():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")
    found_patient = patient_service.find_patient(" P1 ")

    assert found_patient is patient

def test_find_practitioner_is_case_sensitive():
    data_store = SmartCareDataStore()
    practitioner_service = PractitionerService(data_store)

    practitioner = practitioner_service.register_practitioner("D1", "Taylor Example", "General")

    with pytest.raises(LookupError):
        practitioner_service.find_practitioner("d1")

def test_find_patient_is_case_sensitive():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")

    with pytest.raises(LookupError):
        patient_service.find_patient("p1")

def test_find_patient_with_non_string_id():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)

    with pytest.raises(ValueError):
        patient_service.find_patient(123345)

def test_find_practitioner_with_non_string_id():
    data_store = SmartCareDataStore()
    practitioner_service = PatientService(data_store)

    with pytest.raises(ValueError):
        practitioner_service.find_patient(123345)