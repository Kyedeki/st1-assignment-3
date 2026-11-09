# SmartCare Appointment System

## Project Overview

SmartCare is a Python-based appointment management system developed for the SmartCare assessment. It supports patient and practitioner registration, appointment booking, appointment lookup, cancellation, and practitioner appointment listing.

The system uses synthetic records and stores data in memory during each application session. Data is lost when the application exits. No database or persistent storage is implemented.

## Requirements

- Python 3.13
- pytest 8.3.5
- Runtime uses only the Python standard library.

Install the development dependencies if required:

```bash
python -m pip install -r requirements-dev.txt
```

## Running the Application

From the `project/` directory, run the demonstration:

```bash
python main.py
```

To launch the interactive menu:

```bash
python main.py --interactive
```

The interactive menu supports:

1. Register patient
2. Find patient
3. Register practitioner
4. Find practitioner
5. Book appointment
6. Cancel appointment
7. Find appointment
8. List practitioner appointments
0. Exit

## Running Tests

Run the complete test suite:

```bash
python -m pytest -q
```

The Stage 9 regression test result was **81 passed, 0 failed**.

## System Structure

- `domain.py` – Contains the Patient, Practitioner and Appointment entities, appointment status and guarded cancellation.
- `data_store.py` – Manages in-memory patient, practitioner and appointment collections.
- `services.py` – Coordinates registration, lookup, booking, cancellation and appointment listing operations.
- `queries.py` – Provides pure appointment sorting and filtering functions.
- `console.py` – Handles date/time parsing, appointment formatting, the demonstration and interactive menu.
- `main.py` – Selects between demonstration and interactive application modes.
- `tests/` – Contains automated tests for domain behaviour, services, queries and workflows.

## Stage 9 Features

Stage 9 introduces appointment query functionality and interactive console integration.

The query functions include:

- `appointment_sort_key()` – Returns a sorting key based on appointment date/time and appointment ID.
- `select_appointments()` – Filters appointments by practitioner and optional status, returning a new list sorted in ascending order.

The appointment service provides `list_practitioner_appointments()`, which validates the practitioner and optional appointment status before returning the matching appointments.

The interactive menu allows users to register and find records, book and cancel appointments, and list appointments by practitioner and status.

## Input and Validation

The console accepts appointment dates and times in the format:

`YYYY-MM-DD HH:MM`

Invalid input, duplicate records, unknown IDs, booking conflicts and invalid appointment status values are handled through error messages. The menu allows users to continue after expected input errors.

IDs are trimmed, non-blank and case-sensitive. Store lookups return `None` when a record is absent, while service lookups raise `LookupError`.

## Limitations

- Data is stored in memory and is lost when the application exits.
- No database, file-based persistence or external storage is implemented.
- Only synthetic information should be used.
- No age, appointment duration, patient-conflict or past-date validation rules apply.
- The system does not implement PG rescheduling or an assurance solution.