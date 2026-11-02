from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner
)

def make_appointment(status=AppointmentStatus.SCHEDULED):
    patient = Patient("P1","Alex Example")
    practitioner = Practitioner("D1","Taylor Example","General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026,10,20,10,30),
        status,
    )
    return appointment

def test_patient_valid_fields_are_trimmed():
    patient = Patient("P1","Alex Example")

    assert patient.patient_id == "P1"
    assert patient.name == "Alex Example"

@pytest.mark.parametrize("patient_id,name", [
    ("","Alex Example"),
    (" ","Alex Example"),
    ("P1", "  "),
    (None,"Alex Example"),
    ("P1",None),
])
def test_patient_rejects_invalid_required_test(patient_id,name):
    with pytest.raises(ValueError):
        Patient(patient_id,name)

def test_practitioner_valid_fields_are_trimmed():
    practitioner = Practitioner("D1","Taylor Example","General")
    assert practitioner.practitioner_id == "D1"
    assert practitioner.name == "Taylor Example"
    assert practitioner.specialty == "General"

@pytest.mark.parametrize("practitioner_id,name,speciality", [
    ("", "Taylor Example", "General"),
    ("D1", "", "General"),
    ("D1", "Taylor Example", ""),
    (None, "Taylor Example", "General"),
    ("D1", None, "General"),
    ("D1", "Taylor Example", None),
])
def test_practitioner_rejects_invalid_required_test(practitioner_id,name,speciality):
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, speciality)

def test_appointment_starts_scheduled_and_keeps_participants():
    appointment = make_appointment()

    assert appointment.appointment_id == "A1"
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient.patient_id == "P1"
    assert appointment.practitioner.practitioner_id == "D1"
    assert appointment.date_time == datetime(2026,10,20,10,30)

def test_appointment_rejects_invalid_participant_objects():
    practitioner =Practitioner (
        "D1",
        "Taylor Example",
        "General", )
    patient = Patient ("P1","Alex Example")
    date_time = datetime(2026,10,20,10,30)

    with pytest.raises(ValueError):
        Appointment("A1","not a patient",practitioner,date_time)

    with pytest.raises(ValueError):
        Appointment("A1",patient,"not a practitioner",date_time)

@pytest.mark.parametrize("date_time", [
    "2026-10-20 10:30",
    datetime(2026,10,20,10,30,15),
    datetime(2026,10,20,10,30,0,1),
    datetime(2026,10,20,10,30,0,tzinfo=__import__("datetime").timezone.utc),
])

def test_appointment_rejects_invalid_date_time(date_time):
    patient = Patient ("P1","Alex Example")
    practitioner = Practitioner ("D1","Taylor Example","General")

    with pytest.raises(ValueError):
        Appointment("A1",patient,practitioner,date_time)

def test_appointment_rejects_invalid_status():
    patient = Patient ("P1","Alex Example")
    practitioner = Practitioner ("d1","Taylor Example","General")

    with pytest.raises(ValueError):
        Appointment("A1",patient,practitioner,datetime(2026,10,20,10,30),"scheduled")

def test_scheduled_appointment_can_be_cancelled_again():
    appointment = make_appointment()
    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED

def test_completed_appointment_cannot_be_cancelled():
    appointment = make_appointment(AppointmentStatus.COMPLETED)

    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.COMPLETED

def test_patient_id_cannot_be_changed():
    patient = Patient ("P1","Alex Example")

    with pytest.raises(AttributeError):
        patient.patient_id = "P2"
    assert patient.patient_id == "P1"

def test_practitioner_id_cannot_be_changed():
    practitioner = Practitioner ("D1","Taylor Example", "general")

    with pytest.raises(AttributeError):
        practitioner.practitioner_id = "D2"
    assert practitioner.practitioner_id == "D1"

def test_appointment_id_cannot_be_changed():
    appointment = make_appointment()

    with pytest.raises(AttributeError):
        appointment.appointment_id = "A2"

    assert appointment.appointment_id == "A1"


