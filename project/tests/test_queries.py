import pytest

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import (
    appointment_sort_key,
    select_appointments,
)
from smartcare.services import AppointmentService

@pytest.fixture

def sample_appointments():
     patient = Patient("P1", "Alex Example")
     practitioner1 = Practitioner("D1", "Taylor Example", "general")
     practitioner2 = Practitioner ("D2", "Smith Example", "Cardio")

     appointments = [
         Appointment(
             "A2", patient, practitioner1,
             datetime (2026,10,1,10,0)
         ),
         Appointment(
             "A1", patient, practitioner1,
             datetime (2026,10,1,9,0)
         ),
         Appointment(
             "A3", patient, practitioner2,
             datetime(2026,10,1,8,0)
         ),
         Appointment(
             "A4", patient, practitioner1,
             datetime(2026,10,1,9,0)
         ),
     ]
     appointments[1].cancel()

     return appointments

def test_select_appointments_includes_all_statuses_by_default(sample_appointments,):
    result = select_appointments(sample_appointments,"D1")

    assert len(result) == 3

def test_select_appointments_filters_scheduled_status(sample_appointments):
    result = select_appointments(
        sample_appointments,
        "D1",
        AppointmentStatus.SCHEDULED,
    )

    assert [a.appointment_id for a in result] == ["A4", "A2"]

def test_select_appointments_returns_empty_for_no_matches(sample_appointments,):
    result = select_appointments(
        sample_appointments,
        "D1",
        AppointmentStatus.COMPLETED,
    )
    assert result == []

def test_select_appointments_sorts_by_datetime_and_id(sample_appointments):
    result =select_appointments(sample_appointments,"D1")

    assert [a.appointment_id for a in result] == ["A1","A4","A2"]

def test_appointment_sort_key_returns_datetime_and_id(sample_appointments):
    appointment = sample_appointments[0]

    assert appointment_sort_key(appointment) == (
        appointment.date_time,
        appointment.appointment_id,
    )

def test_select_appointments_is_deterministic(sample_appointments):
    first_result = select_appointments(sample_appointments, "D1")
    second_result =select_appointments(sample_appointments, "D1")

    assert first_result == second_result

def test_select_appointments_does_not_modify_source(sample_appointments):
    original = sample_appointments.copy()
    original_ids = [a.appointment_id for a in sample_appointments]

    result = select_appointments(sample_appointments,"D1")

    assert result is not sample_appointments
    assert sample_appointments == original
    assert [a.appointment_id for a in sample_appointments] == original_ids

def test_select_appointments_uses_named_sort_key(sample_appointments, monkeypatch,):
    calls = []

    def tracking_sort_key(appointment):
        calls.append(appointment.appointment_id)
        return appointment_sort_key(appointment)

    monkeypatch.setattr(
        "smartcare.queries.appointment_sort_key",
        tracking_sort_key,
    )

    select_appointments(sample_appointments, "D1")

    assert calls == ["A2","A1","A4"]