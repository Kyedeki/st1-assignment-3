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

The query functions should operate on explicit appointment data rather than accessing a global datastore. The service layer should coordinate domain operations, while the console handles user input and output.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| `appointment_sort_key` | `appointment: Appointment` | Tuple containing appointment date/time and ID | Produce a consistent sorting key without modifying the appointment | `Appointment.date_time` and `Appointment.appointment_id` |
| `select_appointments` | Appointment collection, optional practitioner ID and optional status filter | New sorted list of `Appointment` objects | Filter using explicit inputs, apply named sorting key and avoid mutating the original collection | Existing `Appointment`, `Practitioner` and `AppointmentStatus` objects |
| Service listing | Practitioner ID and optional status filter | List of matching appointments or an appropriate validation error | Validate practitioner existence and filter values; obtain appointments from the shared datastore; delegate filtering and sorting to the query function | Existing registered practitioners and datastore operations |
| Console | User-selected action and input values | Displayed results, messages and continued menu interaction | Read inputs, convert date/time and status values, call service methods, display results and recover from supported input errors | Existing service methods and domain validation rules |

**Relationship to existing contracts:** Patients have unique, case-sensitive IDs and names. Practitioners have unique IDs, names and specialties. Each appointment has its own ID, references actual registered patient and practitioner objects, and stores a date/time and appointment status.

The query functions should reuse these existing objects rather than creating copies of domain entities. Cancellation should retain the appointment record, and filtering should not modify appointment status or datastore contents.

The intended sorting order is date/time followed by appointment ID, providing a consistent result when multiple appointments share the same time.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| `Appointment.cancel()` reads input | The domain model is performing user interaction instead of managing appointment state. | `Appointment.cancel()` should enforce the cancellation rules and update the appointment status. The console should ask for input and call the appropriate service method. |
| Service prints/reads the menu | The service layer is mixing application operations with presentation and interaction logic. | `console.py` should display the menu, read user choices and show messages. Services should coordinate registration, lookup, booking, cancellation and validated listing. |
| Query sorts its source in place | Using `appointments.sort()` modifies the caller's collection, breaking the required non-mutation behaviour of a pure query. | `queries.py` should use `sorted()` and return a new list, leaving the original collection and appointment objects unchanged. |
| Store prints "Appointment saved" | The datastore is performing presentation work and implying persistence that SmartCare does not provide. | `SmartCareDataStore` should manage in-memory collections and return appropriate results. The console should display user-facing confirmation messages. |

**Responsibility conclusion:** Each component should have a clear purpose. Domain objects enforce invariants, the datastore manages session collections, services coordinate operations, pure queries filter and sort explicit inputs, and the console handles interaction. Keeping these responsibilities separate makes the application easier to test and maintain.|---|---|---|
| Appointment.cancel reads input | | |
| Service prints/reads the menu | | |
| Query sorts its source in place | | |
| Store prints Appointment saved | | |

### A4 Sorting comparison

**Using `appointments.sort(key=appointment_sort_key)`:**

This sorts the original list in place. The source order may change, and the method returns `None`. The list retains its identity because it is the same list object, now reordered.

**Using `result = sorted(appointments, key=appointment_sort_key)`:**

This creates a new sorted list without changing the original list's order. The returned list has a different identity from the source list, although it contains references to the same Appointment objects.

**Meaningful mutation check:**

Before sorting, save a snapshot of the original appointment ID order and the relevant appointment fields. After calling the query, compare them to confirm that the source list and its objects have not changed. Also check that `result is not appointments` and that the returned appointment IDs are correctly ordered.

**Score-example prediction:**

For the supplied example:

`[('Bea', 8), ('Ali', 8), ('Chen', 5)]`

Using `sorted(scores, key=score_key)` produces:

`[('Chen', 5), ('Ali', 8), ('Bea', 8)]`

The result is ordered by ascending score and then alphabetically by name when scores are equal. The original `scores` list remains unchanged.

**Why pass the named key rather than call it immediately?**

Writing `key=score_key` passes the function itself so Python can call it for each item being sorted. Writing `key=score_key()` would attempt to call the function immediately without the required item argument, causing an error. A named key can also be reused and tested independently.

### A5 Exit question

**Why does cancellation change a retained object's status rather than remove the appointment?**

Cancellation should update the existing Appointment object's status to `CANCELLED` instead of deleting it because SmartCare must preserve appointment history during the current session. Removing the object would make previous appointment information unavailable and violate the retained-history requirements.

**Checks demonstrating retained history:**

After creating and cancelling an appointment, retrieve it using its ID and confirm that the same stored Appointment object is returned with status `CANCELLED`.

Then list the practitioner's appointments without a status filter. The cancelled appointment should still appear because the default filter includes every appointment status.

Finally, list the practitioner's appointments with the explicit `SCHEDULED` filter. The cancelled appointment should be excluded from that result because its current status is `CANCELLED`.

These checks demonstrate that cancellation changes the appointment's state without deleting the record or changing its identity.

## B. Human design and contracts

**Human design decisions and reasoning:** The Stage 9 implementation will extend the existing SmartCare application without changing the domain model or adding persistence. The design separates responsibilities between domain objects, the datastore, services, pure query functions and console interaction.

The `appointment_sort_key()` function will return an appointment's date/time and ID as a deterministic sorting key. The `select_appointments()` function will receive an explicit appointment collection, practitioner ID and optional `AppointmentStatus` filter, then return a new sorted list without modifying the input.

Practitioner registration checks and filter validation will remain in the service layer. The console will convert user-entered status strings into enum values before calling the service. One shared datastore will be maintained throughout each console session.

These decisions are based on the existing SmartCare contracts and the Stage 9 requirements. They are proposed design decisions, not claims of completed implementation or verification.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | Appointment collection, practitioner ID | `select_appointments()` filters appointments for the requested practitioner | Only matching practitioner's appointments returned | `test_queries.py`: practitioner isolation with another practitioner as a control |
| QRY-02 | Appointments and optional `AppointmentStatus` | Pure query applies optional status filtering | `None` includes all statuses; explicit enum includes only that status; no matches returns `[]` | Tests for SCHEDULED, CANCELLED, COMPLETED and default all |
| QRY-03 | Appointment collection | `appointment_sort_key()` and `select_appointments()` sort by date/time and appointment ID | Ascending deterministic order; original source unchanged | Equal-time tie-break and source non-mutation tests |
| QRY-04 | Registered practitioner ID and optional enum status | `AppointmentService.list_practitioner_appointments()` validates and delegates to the query | New list for known practitioner; `LookupError` for unknown ID; `ValueError` for invalid ID or non-enum status | Service listing validation tests |
| FP-01 | Explicit appointment collection and filter values | Pure query with no hidden datastore access

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

### 1. Which integration concern was architectural rather than a filtering/sorting detail?

The main architectural concern was keeping responsibilities separate while allowing the components to work together. Domain objects should enforce business rules, the datastore should retain session records, services should coordinate operations, pure query functions should filter and sort appointments, and the console should handle user interaction.

Using one shared datastore throughout the menu session is particularly important. Creating a new datastore for each command would lose previously registered participants and appointments, even if the filtering and sorting functions were correct.

### 2. Which Copilot suggestion did you reject as over-engineering, and why?

**Pending actual Copilot review.** This reflection will be completed after examining the suggestions Copilot actually makes about Cassandra's Stage 9 implementation. We should not invent a rejected suggestion or claim a decision that has not occurred.

### 3. How did you prove cancelled appointments remain retrievable and listable in the same session?

The planned verification is to create an appointment, cancel it, and then retrieve it through the existing service. The returned appointment should be the same stored object with status `CANCELLED`.

The practitioner listing with no status filter should include that appointment, while a `SCHEDULED`-only listing should exclude it. These checks will establish that cancellation retains history rather than deleting the appointment.

**Actual test results:** Pending Cassandra's Stage 9 query and workflow verification.

## G. Ten formative answers

### 1. What makes `select_appointments` pure, and what side effect breaks purity?

**Response:** The function is pure when it receives all necessary information through its arguments, returns a predictable result for the same unchanged inputs, and does not modify the source list or Appointment objects. Sorting the original list in place, printing messages, reading user input or accessing a hidden global datastore would break purity.

### 2. Which explicit inputs are needed, and why avoid a global store?

**Response:** `select_appointments()` needs a list of Appointment objects, a practitioner ID and an optional `AppointmentStatus` filter. Using an explicit collection makes the function easier to test and reuse. A global store would create a hidden dependency and could produce different results depending on unrelated application state.

### 3. How can a new list reuse Appointment objects safely?

**Response:** The query can create a new list containing references to the existing Appointment objects without copying or changing them. This is safe because the query only reads their fields. The returned list has a different identity from the source list, while the contained appointment objects retain their original identities.

### 4. Why use a named key, and what breaks equal-time ties?

**Response:** The named `appointment_sort_key()` function makes the sorting rule clear, reusable and independently testable. It returns the appointment's date/time and ID. Appointments are ordered by date/time first, and appointment ID breaks ties when two appointments share the same time.

### 5. How do default and explicit status filters differ?

**Response:** When the status parameter is `None`, appointments of every status are included, including `SCHEDULED`, `CANCELLED` and `COMPLETED`. When a specific `AppointmentStatus` enum is supplied, only appointments with that status are returned. A valid filter that matches no appointments returns an empty list.

### 6. How do empty, unknown practitioner and invalid filter cases differ?

**Response:** A registered practitioner with no appointments, or no appointments matching a valid filter, receives a new empty list. A valid but unregistered practitioner ID raises `LookupError`. A blank or invalid ID raises `ValueError`. A non-enum status supplied directly to the service also raises `ValueError` rather than returning an empty result.

### 7. Which console errors recover, and how is unchanged state checked?

**Response:** The console should recover from invalid menu choices, blank or duplicate IDs, unknown participants, invalid date/time input, invalid status filters, scheduling conflicts and repeated cancellation. It should display a useful message and return to the menu. To check unchanged state, compare relevant records before and after a rejected action and confirm that a later valid action succeeds.

### 8. What is data integrity for registered participants, conflicts and history?

**Response:** Data integrity means appointments reference actual registered Patient and Practitioner objects, IDs remain valid and unique within their entity type, and conflicting scheduled bookings for the same practitioner are rejected. Cancellation changes an existing appointment's status without deleting its history, and rejected operations must not leave unintended changes in the datastore.

### 9. What is Copilot's review role, and who verifies findings?

**Response:** GitHub Copilot acts as a reviewer that can suggest potential problems involving query purity, validation, sorting, object identity and integration. Its suggestions are hypotheses rather than proof. The student team must inspect the code, compare findings with requirements, run meaningful tests and make the final decisions. Another human member also reviews the changes through GitHub.

### 10. How do pure functions and OOP responsibilities work together?

**Response:** Object-oriented components manage application state and business responsibilities, while pure functions process explicit collections without modifying them. Domain objects enforce invariants, the datastore retains in-memory records, services coordinate operations, queries select and sort appointments, and the console handles user interaction. This separation keeps business rules out of the interface and makes the system easier to test and maintain.

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
