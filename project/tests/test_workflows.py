import pytest

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)
from smartcare.console import run_menu

@pytest.fixture

def setup_services():
    data_store = SmartCareDataStore()

    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient_service.register_patient("P1","Alice")

    practitioner_service.register_practitioner(
        "D1","Taylor Example", "General"
    )
    practitioner_service.register_practitioner(
        "D2", "Smith Example", "Cardio"
    )

    appointment_service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )
    appointment_service.book_appointment(
        "A2", "P1", "D1", datetime(2026, 10, 1, 10, 0)
    )
    appointment_service.book_appointment(
        "A3", "P1", "D2", datetime(2026, 10, 1, 11, 0)
    )

    appointment_service.cancel_appointment("A1")

    return data_store, appointment_service

def test_list_practitioner_appointments_returns_correct_practitioner(setup_services,):
    data_store,appointment_service = setup_services
    result = appointment_service.list_practitioner_appointments("D1")

    assert len(result) == 2
    assert all(
        appointment.practitioner.practitioner_id == "D1"
        for appointment in result
    )
def test_list_practitioner_appointments_includes_cancelled_by_default(setup_services,):
    data_store, appointment_service = setup_services
    result = appointment_service.list_practitioner_appointments("D1")

    assert len(result) == 2
    assert result[0].appointment_id == "A1"
    assert result[0].status is AppointmentStatus.CANCELLED

def test_list_practitioner_appointments_filters_scheduled(
    setup_services,
):
    data_store, appointment_service = setup_services

    result = appointment_service.list_practitioner_appointments(
        "D1",
        AppointmentStatus.SCHEDULED,
    )

    assert len(result) == 1
    assert result[0].appointment_id == "A2"

def test_list_practitioner_appointments_unknown_practitioner(
        setup_services,
):
    data_store, appointment_service = setup_services

    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments("D99")


def test_list_practitioner_appointments_invalid_status(
    setup_services,
):
    data_store, appointment_service = setup_services

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(
            "D1",
            "scheduled",
        )
def test_list_practitioner_appointments_returns_empty_list(
    setup_services,
):
    data_store, appointment_service = setup_services

    practitioner_service = PractitionerService(data_store)
    practitioner_service.register_practitioner(
        "D3", "Dr Lee", "Paediatrics"
    )

    result = appointment_service.list_practitioner_appointments("D3")

    assert result == []

def test_list_practitioner_appointments_rejects_blank_id(
    setup_services,
):
    data_store, appointment_service = setup_services

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(" ")

def test_listing_does_not_modify_stored_appointments(setup_services):
    data_store, appointment_service = setup_services

    original = data_store.list_appointments()
    original_statuses = [a.status for a in original]

    appointment_service.list_practitioner_appointments("D1")

    after = data_store.list_appointments()

    assert len(after) == len(original)
    assert after == original
    assert [a.status for a in after] == original_statuses

def test_listing_returns_original_stored_appointment_objects(
    setup_services,
):
    data_store, appointment_service = setup_services

    stored_appointments = data_store.list_appointments()

    result = appointment_service.list_practitioner_appointments("D1")

    for appointment in result:
        assert any(
            appointment is stored
            for stored in stored_appointments
        )
def test_listing_accepts_practitioner_id_with_whitespace(
    setup_services,
):
    data_store, appointment_service = setup_services

    result = appointment_service.list_practitioner_appointments(" D1 ")

    assert len(result) == 2
    assert all(
        a.practitioner.practitioner_id == "D1"
        for a in result
    )
def test_listing_rejects_non_string_practitioner_id(setup_services):
    data_store, appointment_service = setup_services

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(None)
def test_failed_listing_does_not_modify_records(setup_services):
    data_store, appointment_service = setup_services

    original = data_store.list_appointments()
    original_statuses = [a.status for a in original]

    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments("D99")

    after = data_store.list_appointments()

    assert after == original
    assert [a.status for a in after] == original_statuses

def test_cancelled_appointment_remains_in_store(setup_services):
    data_store, appointment_service = setup_services

    appointment_service.list_practitioner_appointments("D1")

    cancelled = appointment_service.find_appointment("A1")

    assert cancelled.status is AppointmentStatus.CANCELLED
    assert cancelled.appointment_id == "A1"

def test_listing_returns_empty_for_completed_status(setup_services):
    data_store, appointment_service = setup_services

    result = appointment_service.list_practitioner_appointments(
        "D1",
        AppointmentStatus.COMPLETED,
    )

    assert result == []
def test_interactive_menu_workflow(monkeypatch, capsys):
    """Test registration, booking, cancellation and appointment listing."""

    user_inputs = iter([
        # Register patient
        "1", "P1", "Alice",

        # Register practitioners
        "3", "D1", "Dr Smith", "General Practice",
        "3", "D2", "Dr Jones", "Cardiology",

        # Book A1 with D1
        "5", "A1", "P1", "D1", "2026-10-01 09:00",

        # Attempt same time with D1 (should fail)
        "5", "A2", "P1", "D1", "2026-10-01 09:00",

        # Same time with D2 (should succeed)
        "5", "A3", "P1", "D2", "2026-10-01 09:00",

        # Cancel A1
        "6", "A1",

        # Find A1
        "7", "A1",

        # List all D1 appointments
        "8", "D1", "",

        # List scheduled D1 appointments
        "8", "D1", "scheduled",

        # Book D1's newly available time slot
        "5", "A4", "P1", "D1", "2026-10-01 09:00",

        # List D1 appointments again
        "8", "D1", "",

        # Exit
        "0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(user_inputs),
    )

    run_menu()

    output = capsys.readouterr().out

    assert "Registered patient: P1" in output
    assert "Registered practitioner: D1" in output
    assert "Registered practitioner: D2" in output
    assert "Booked:" in output
    assert "Cancelled:" in output
    assert "cancelled" in output.lower()
    assert "Invalid" not in output
    assert "Session-only data: records are lost on exit." in output

def test_interactive_menu_invalid_input_recovery(monkeypatch, capsys):
    """Test that invalid inputs are handled and the menu continues."""

    user_inputs = iter([
        # Invalid menu choice
        "9",

        # Register patient
        "1", "P1", "Alice",

        # Duplicate patient registration
        "1", "P1", "Alice Duplicate",

        # Register practitioner
        "3", "D1", "Dr Smith", "General Practice",

        # Booking with an unknown patient
        "5", "A1", "P99", "D1", "2026-10-01 09:00",

        # Booking with malformed date/time
        "5", "A1", "P1", "D1", "01-10-2026",

        # Unknown appointment
        "7", "A99",

        # Invalid listing status
        "8", "D1", "invalid",

        # Exit
        "0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(user_inputs),
    )

    run_menu()

    output = capsys.readouterr().out

    assert "Invalid menu choice" in output
    assert "Patient ID already exists" in output
    assert "Patient not found" in output
    assert "YYYY-MM-DD HH:MM" in output
    assert "Appointment not found" in output
    assert "Session-only data: records are lost on exit." in output