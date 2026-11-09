# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 2
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: 5a5f35c21df62da670616ec7e64596bd788b0b3. Command: python -m pytest -q. Working directory: project/. Actual result: 57 passed, 0 failed.

## A. Tutorial activities

### A1 Session state classification

| Information            | Required session/domain or transient state? | Requirement or reason |
|------------------------|--|-|
| Patient identit y      |  | |
| Appointment history    |  | |
| Temporary menu choice  |  | |
| Practitioner specialty |  | |
| Debug print output     |  | |
| Appointment status     |  |  |

What is intentionally lost on exit?: In-memory patient, practitioner, and appointment records are discarded when the application exits. Stage 9 does not implement the persistent change

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | | | | |
| select_appointments | | | | |
| Service listing | | | | |
| Console | | | | |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <!-- response -->

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | | |
| Service prints/reads the menu | | |
| Query sorts its source in place | | |
| Store prints Appointment saved | | |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: <!-- response -->

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <!-- response -->

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| | | | | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion                                                                                        | Actual result | Evidence link      |
|-----------------------|---------------|----------------------------------------------------------------------------------------------------------------------|---------------|--------------------|
| QRY-01, FP-01         | queries.py    | appointment_sort_key() returns a tuple containing appointment date/time and appointment ID.                          | Passed        | test_queries.py    |
| QRY-02, FP-02         | queries.py    | select_appointments() filters appointments by practitioner ID and returns a new sorted list.                         | Passed        | test_queries.py    |
| QRY-03                | queries.py    | 	Tests practitioner isolation and filtering by SCHEDULED, CANCELLED and COMPLETED status.                             | Passed        | test_queries.py    |
| QRY-04, FP-03         | queries.py    | 	Tests chronological ordering, equal-time appointment ID tie-breaking, deterministic results and named-key reuse.     | Passed        | test_queries.py    |
| FP-02, FP-03          | queries.py    | 	Tests repeated calls, new result lists and source-list non-mutation.                                                 | Passed        | test_queries.py    |
| Service listing       | services.py   | 	Tests known practitioners, empty results, unknown practitioners, invalid status, whitespace IDs and object identity. | Passed        | test_workflows.py  |
| History retention     | services.py   | 	Confirms cancelled appointments remain stored and retrievable.                                                       | Passed        | test_workflows.py  |


Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O:
- select_appointments() is a pure query because it recieves its inputs explicitly through the parameters and does not access global state or the data store. It does not perform input/output, print messages or modify the appointment objects. It creates a new list, filters the matching appointments and sorts the result using the appointment_sort_key(). The original collections remains unchanged
What the tests do and do not establish:
- the query tests verify the isolation of the practitioner, filter status, ordering, deterministic results, and source-list non-mutation. The service test verify the validation, empty, and unknown practitioner cases, object identity and cancellation history. The test provides evidence that the implemented code works for the tested scenarios. Does not estalish database persistence, because stage 9 only uses session only data

## D. Integrated console and workflow evidence

| Scenario / acceptance ID     | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|------------------------------|---|---|---|---|
| UI-01 full menu workflow     | Automated test: test_interactive_menu_workflow|Register patient and practitioners, book appointments, reject a conflicting booking, allow another practitioner at the same time, cancel and retrieve an appointment, filter listings and reuse a cancelled time slot. |Passed. The test verified registration, booking, cancellation, retrieval, listing and exit through the interactive menu. |/test_workflows.py |
| UI-02 invalid-input recovery |Automated test: test_interactive_menu_invalid_input_recovery |Invalid menu choice, duplicate registration, unknown booking participant, malformed date/time, unknown appointment and invalid listing status should produce errors without crashing the menu. |Passed. The test verified the expected error messages and successful continuation to application exit. |test_workflows.py |
| Automated service workflow   |Service tests in test_workflows.py |Verify practitioner listing, filtering, validation, cancellation history, unchanged records and object identity |14 service workflow tests passed. |project/tests/test_workflows.py |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI:The Stage 9 query, service, store, domain and console responsibilities were designed and implemented before requesting the GitHub Copilot review. The implementation was tested before the review, with 81 tests passing.
Actual prompt/context supplied: GitHub Copilot was asked to review the Stage 9 implementation, focusing on query correctness, separation of responsibilities, service validation, console error handling, test coverage and potential defects.
Actual response: The review found no Critical or Important implementation defects. It identified one Important testing weakness and two Optional testing improvements.

| AI finding                                                                                                                                                         | Code/test evidence                                                                | Severity  | Accept/Modify/Reject and reason                                                                                                                 | Change or no change                                       | Actual verification                                                                                     |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| The interactive workflow test does not sufficiently assert conflict rejection, cancellation, slot reuse and whether a rejected booking leaves the state unchanged. | tests/test_workflows.py:206–253; services.py:116–130; console.py:125–136, 151–175 | Important | Accept. Stronger assertions would provide clearer evidence that the workflow behaves correctly and rejected bookings do not modify stored data. | Strengthen the workflow test assertions.                  | Existing full suite: 81 passed. Additional verification is pending until the test is updated and rerun. |
| Query tests do not explicitly test the cancelled filter or verify that repeated calls return distinct list objects.                                                | tests/test_queries.py:47–96; queries.py:16–34                                     | Optional  | Accept. These tests would provide more direct evidence of status filtering and the requirement to return a new list.                            | Add cancelled-status and distinct-list assertions         | Existing query tests: 8 passed. Additional verification is pending.                                     |
| Console date-input tests do not directly test impossible calendar dates or invalid clock values.                                                                   | tests/test_workflows.py:269–300; console.py:16–31                                 | Optional  | Accept. Additional tests would strengthen validation coverage for invalid date and time inputs.                                                 | Add tests for impossible dates and invalid clock values.  | Existing full suite: 81 passed. Additional verification is pending.                                     ||||||

- The findings were accepted because they identify opportunities to strengthen test coverage rather than defects in the current implementation. The review did not require changes to the query or service design.
Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate:
The domain entities maintain valid data and domain rules, including guarded appointment cancellation. The data store manages patient, practitioner and appointment collections and their relationships. Services coordinate registration, lookup, booking, cancellation and appointment listing. The query functions perform filtering and sorting without side effects. The console handles user interaction, input parsing, displaying results and recovering from expected errors. This separation keeps business rules out of the console and prevents query functions from controlling application state.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches:
- Stage 9 implementation branch: feature/stage9-queries.
- Stage 9 work covers query functions, practitioner appointment listing, console menu integration and automated workflow tests.
- Stage 9 work covers query functions, practitioner appointment listing, console menu integration and automated workflow tests.
- Stage 8 was completed and integrated before Stage 9. Stage 9 started from integrated Stage 8 SHA 5a5f35c21df62da670616ec7e64596bd788b0b3.
- Branch/issue links: https://github.com/Kyedeki/st1-assignment-3/tree/docs/stage9-evidence

PR/diff and another-member human reviewer:
Review responses and Copilot comparison: [<!-- links -->](https://github.com/Kyedeki/st1-assignment-3/pull/13) |Reviewer: Cassandra Navarro
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: project/README.md
- Required contents:
  - Run the demonstration using python main.py.
  - Run the interactive console using python main.py --interactive.
  - Run the test suite using python -m pytest -q.
  - State that records are stored in memory only and are lost when the application exits.
  - Evidence/link: [Insert GitHub README link after confirming the changes are committed.]
Unresolved issues and support/action: No Critical or Important implementation issues were identified. Minor test improvements remain, and the team will address them before finalising Stage 9.
UG common candidate / PG future branch plan: Proceed to Stage 12 using the approved common Stage 9 version.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [x] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
