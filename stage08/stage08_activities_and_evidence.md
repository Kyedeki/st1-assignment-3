# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- **Stage 7 code SHA and requirement baseline:** Pending verification of the final integrated Stage 7 commit and requirements.

- **Baseline test command / working directory / observed result / evidence:** Stage 7 baseline result still needs to be confirmed from the earlier test records.

- **Clean preparation SHA if a record-only commit followed Stage 7:** Pending verification.

- **Branch and preparer / how teammates obtained this branch:** The Stage 8 debugging branch is `debug/stage08`. The branch is up to date with `origin/debug/stage08`. Teammate access and preparation ownership still need to be recorded.

- **Downloaded tool version, source SHA256 and --check outcome:** Pending verification from the Stage 8 preparation utility records.

- **--apply and --verify output summaries / artefact references:** Pending verification from the preparation utility output.

- **Bounded diff inspected and recovery location (not committed):** Pending verification.

- **Prepared faulty-state commit SHA:** `3810208` — `prepare debug stage 08`.

- **Preparation or recovery issues and resolution, if any:** Not yet confirmed.

- **Initial prepared full-suite command / result / key failures:** Executed the pytest suite from the `project/` directory on branch `debug/stage08`. The result was **50 passed and 5 failed** in approximately 0.25 seconds. Four failures involved cancelled appointment retrieval or repeated cancellation, and one involved practitioner conflict validation.

**Git verification:** The working tree was clean, with no uncommitted changes. The local Stage 8 branch was up to date with its remote branch.

**Evidence:** VS Code terminal screenshots showing the Git status, commit information and pytest failure summary.

## C. F8-01 diagnosis and repair

- **Symptom / observed behaviour:** A cancelled appointment could not be retrieved using its appointment ID.

- **Expected behaviour and requirement:** FR-07 requires cancelled appointment history to remain accessible. The lookup should return the appointment even after cancellation.

- **Minimal synthetic reproduction steps:** Create appointment A1, cancel it, then retrieve it using `find_appointment("A1")`.

- **Meaningful failing test path/name and exact relevant failure:** `tests/test_services.py::test_cancel_appointment`, line 95. The assertion expected the appointment object, but `find_appointment("A1")` returned `None`. The focused test result was 1 failed in 0.16 seconds.

- **Human hypothesis and intended checks:** The lookup might be excluding cancelled appointments. Inspect the status filtering in `find_appointment()` and compare the stored records with the lookup result. This hypothesis was discussed with AI assistance.

- **Supported root cause and inspected code/runtime evidence:** The provided faulty implementation contains a condition excluding appointments whose status is `cancelled`. The focused test confirms that retrieval returns `None`. The datastore contents still need to be inspected to establish whether the appointment remains stored.

- **Smallest justified fix / diff / why other behaviour is preserved:** Pending the required diagnosis and Copilot review.

- **Repair SHA / focused verification result:** Pending.
## D. F8-02 diagnosis and repair

- **Symptom / observed behaviour:** The practitioner conflict test failed because the booking operation did not raise the expected `ValueError`.

- **Expected behaviour and requirement:** Under AC-04.2, the booking system should detect scheduling conflicts involving the same practitioner at the same date and time. Different practitioners should be able to have appointments at the same time, provided no other booking rule is violated.

- **Minimal synthetic reproduction steps:** Create a scheduled appointment for practitioner P1 at a specified time. Attempt another booking for P1 at the same time and check whether a `ValueError` is raised. Also check a booking for practitioner P2 at that time to confirm that different practitioners do not incorrectly conflict.

- **Meaningful failing test path/name and exact relevant failure:** `tests/test_starter.py::test_conflict_rule_and_different_practitioner`, line 127. The test expected `ValueError`, but no exception was raised. The focused pytest result was 1 failed in 0.13 seconds.

- **Human hypothesis and intended checks:** The practitioner comparison in `has_practitioner_conflict()` may be reversed. Inspect the comparison operator and test same-practitioner and different-practitioner bookings at identical times. This hypothesis was discussed with AI assistance.

- **Supported root cause and inspected code/runtime evidence:** Inspection of `SmartCareDataStore.has_practitioner_conflict()` identified the condition `appointment.practitioner.practitioner_id != practitioner_id`. The focused failing test showed that the booking operation did not reject the conflicting appointment as expected. The reversed comparison is the leading cause, subject to confirming the complete test setup and requirement.

- **Smallest justified fix / diff / why other behaviour is preserved:** Pending completion of the required diagnosis and Copilot review.

- **Repair SHA / focused verification result:** Pending repair and testing.

## E. Human-first hypotheses

### F8-01 human entry

**Likely cause and why plausible:** The `find_appointment()` method appears to exclude cancelled appointments from lookup results because it contains the condition `appointment.status.value != "cancelled"`. This explains why the focused test returned `None` instead of the expected appointment object. The hypothesis is consistent with FR-07, which requires cancelled appointment history to remain accessible.

**Evidence intended to inspect:** The implementations of `find_appointment()`, `list_appointments()`, and `cancel_appointment()`, the appointment status after cancellation, and the failing assertion in `tests/test_services.py::test_cancel_appointment` at line 95.

**Competing explanation:** The cancellation service might have removed the appointment from the datastore rather than retaining it with a cancelled status.

**Discriminating check:** Compare the appointments returned by `list_appointments()` with the result of `find_appointment("A1")` after cancellation. If A1 remains in the stored list while the lookup returns `None`, this would support the lookup-filter hypothesis and rule out deletion as the immediate explanation.

**Member and saved sequence/time or commit:** Reema Aboset investigated F8-01 with ChatGPT assistance before consulting GitHub Copilot. The initial investigation involved inspecting the source code and reproducing the failing cancellation test. The actual timestamp or saved evidence reference should be added from the investigation record. The prepared faulty-state commit was `3810208`; this identifies the faulty code version, not the timestamp of the hypothesis.

### F8-02 human entry

**Likely cause and why plausible:** The `has_practitioner_conflict()` method uses `!=` rather than `==` when comparing practitioner IDs. This may cause the method to miss conflicts involving the same practitioner while incorrectly identifying different practitioners as conflicting.

**Evidence intended to inspect:** The practitioner ID comparison in `has_practitioner_conflict()`, the booking service's conflict-checking logic, and the test setup in `tests/test_starter.py`. The focused test failed at line 127 because the expected `ValueError` was not raised.

**Competing explanation:** The failure could be caused by different appointment times, an incorrect practitioner ID, an appointment that is not scheduled, or an issue in the test setup.

**Discriminating check:** Compare bookings for the same practitioner at the same time with bookings for different practitioners at the same time. Inspect the conflict-checking return values and compare them with AC-04.2.

**Member and saved sequence/time or commit:** Reema Aboset investigated F8-02 with ChatGPT assistance before consulting GitHub Copilot. The investigation involved examining the practitioner comparison and reproducing the failing test. The actual timestamp or saved evidence reference should be added from the investigation record.

---

## F. GitHub Copilot prompts, findings and human decisions

### F8-01 Copilot review

**Actual prompt / output reference and member:** Reema Aboset consulted GitHub Copilot Chat after the initial debugging investigation. The prompt included the observed cancelled-appointment lookup failure, expected behaviour under FR-07, reproduction steps, failing test, initial hypothesis, competing explanation and relevant source files. Copilot was instructed to identify three ranked possible causes with evidence checks, without modifying files, running commands, rewriting the application or inventing requirements.

**Copilot evidence reference:** The actual F8-01 Copilot conversation should be preserved in the Stage 8 evidence folder. Add the saved file path or accessible conversation reference once available.

**1. Ranked suggestion — Cancelled-status filter in the datastore lookup**

- **Evidence check:** Inspect `SmartCareDataStore.find_appointment()` and compare its conditions with the failing cancellation test.
- **Observed evidence:** The method contains `appointment.status.value != "cancelled"`, which prevents cancelled appointments from being returned. The focused test `tests/test_services.py::test_cancel_appointment` failed at line 95 because `find_appointment("A1")` returned `None` instead of the expected appointment object.
- **Evaluation:** Correct. The inspected source and failing test directly support this diagnosis.
- **Human decision:** Accept the diagnosis. The proposed minimal repair is to remove the cancelled-status filtering while preserving appointment ID validation and normal lookup behaviour.

**2. Ranked suggestion — Appointment removed from storage during cancellation**

- **Evidence check:** Inspect `AppointmentService.cancel_appointment()`, `Appointment.cancel()` and datastore storage operations.
- **Observed evidence:** Copilot identified that cancellation changes the appointment's status rather than explicitly deleting it. No public appointment-removal operation was found in the inspected implementation. Direct runtime confirmation of the stored A1 record is still pending.
- **Evaluation:** Unlikely. The inspected implementation does not support deletion as the cause of the observed lookup failure.
- **Human decision:** Reject this as the currently supported explanation, while retaining the proposed runtime check to confirm that A1 remains in storage.

**3. Ranked suggestion — Appointment ID or datastore mismatch**

- **Evidence check:** Inspect the test setup, appointment ID handling and datastore references used during creation, cancellation and retrieval.
- **Observed evidence:** Copilot found that the test uses the same datastore for booking and retrieval. The lookup request uses the expected appointment ID, and the available source evidence does not indicate an ID or datastore mismatch.
- **Evaluation:** Unsupported and very unlikely.
- **Human decision:** Reject this explanation because the inspected test setup and source code do not support it.

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agreed with the earlier hypothesis that cancelled appointments were being excluded by the lookup method. The failing test and source-code inspection support the cancelled-status filter as the root cause. The alternative explanations were considered but lacked supporting evidence. The smallest justified repair is to remove the status restriction while preserving appointment ID validation and normal lookup behaviour. The repair has not yet been applied, and passing regression verification is still required.

### F8-02 Copilot review

### F8-02 Copilot review

**Actual prompt / output reference and member:** Reema Aboset consulted GitHub Copilot Chat to investigate F8-02 after documenting the initial hypothesis. The prompt included the observed failure, expected practitioner-conflict behaviour under AC-04.2, reproduction steps, the failing test, the initial hypothesis and competing explanations. Copilot inspected the datastore, booking service and test code without changing files or running commands.

**Copilot evidence reference:** The actual F8-02 prompt and response should be saved in the Stage 8 evidence folder. Add the saved reference once available.

**1. Ranked suggestion — Reversed practitioner comparison**

- **Evidence check:** Inspect the practitioner ID comparison in `has_practitioner_conflict()` and verify how the booking service calls this method.
- **Observed evidence:** The method uses `appointment.practitioner.practitioner_id != practitioner_id`. This condition is false when an existing and requested appointment involve the same practitioner. Consequently, a conflicting appointment may be missed. Copilot also confirmed that `book_appointment()` calls the conflict checker with the requested practitioner ID and timestamp.
- **Evaluation:** Correct. Source inspection supports this diagnosis as the leading cause of the failing test.
- **Human decision:** Accept. The proposed minimal repair is to change the practitioner comparison from `!=` to `==` without modifying unrelated booking rules.

**2. Ranked suggestion — Different appointment timestamps**

- **Evidence check:** Inspect the timestamps used in `tests/test_starter.py::test_conflict_rule_and_different_practitioner`.
- **Observed evidence:** The test defines `when` once and passes the same value to both bookings involving practitioner D1. The conflict checker compares appointment timestamps using equality.
- **Evaluation:** Unlikely. The inspected test setup does not support a timestamp mismatch, although the runtime values were not separately inspected.
- **Human decision:** Reject as the currently supported cause.

**3. Ranked suggestion — Existing appointment is not scheduled**

- **Evidence check:** Inspect appointment creation, the default appointment status and the status condition in `has_practitioner_conflict()`.
- **Observed evidence:** The test creates A1 using `book_appointment()`. The `Appointment` domain model defaults its status to `SCHEDULED`, and the conflict checker considers scheduled appointments. Copilot did not find evidence that A1 changes status before the second booking.
- **Evaluation:** Unlikely. The inspected booking path indicates that A1 should be scheduled.
- **Human decision:** Reject as the currently supported cause, subject to runtime verification if needed.

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agrees with the earlier hypothesis that the practitioner comparison is reversed. The failing test and inspected code support this explanation. The alternative causes involving timestamps and appointment status were considered but were not supported by the test setup or appointment creation logic. The smallest justified repair is to change `!=` to `==` in `has_practitioner_conflict()`. The repair has not yet been applied, and passing regression verification is still required.

## G. Failing-to-passing regression evidence

### F8-01 — Cancelled appointment history

**Requirement:** FR-07 — Cancelled appointment history must remain accessible.

**Before repair:** The focused test `tests/test_services.py::test_cancel_appointment` failed at line 95 because `find_appointment("A1")` returned `None` instead of the appointment object.

**Root cause:** The datastore lookup excluded appointments with a status of `"cancelled"`.

**Minimal repair:** Removed the cancelled-status restriction from `SmartCareDataStore.find_appointment()` while preserving appointment ID validation and normal lookup behaviour.

**Focused test command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**After repair:** PASSED — 1 test passed in 0.05 seconds.

**Repair commit:** `2b641de`

### F8-02 — Practitioner scheduling conflict

**Requirement:** AC-04.2 — Scheduling conflicts must be detected for the same practitioner at the same date and time.

**Before repair:** The focused test `tests/test_starter.py::test_conflict_rule_and_different_practitioner` failed at line 127 because the expected `ValueError` was not raised.

**Root cause:** The practitioner comparison in `has_practitioner_conflict()` used `!=` instead of `==`.

**Minimal repair:** Changed the comparison to `appointment.practitioner.practitioner_id == practitioner_id` while preserving the other scheduling conditions.

**Focused test command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**After repair:** PASSED — 1 test passed in 0.06 seconds.

**Repair commit:** `2b641de`

### Full regression verification before refactoring

**Repository branch:** `debug/stage08`

**Working directory:** `project/`

**Faulty-state commit:** `3810208`

**Repair commit:** `2b641de`

**Full-suite baseline before repairs:** 50 passed, 5 failed.

**Verification command:**

`py -m pytest -v --tb=short`

**Full-suite result after repairs:** 55 passed, 0 failed, in 0.12 seconds.

**Environment:** Windows, Python 3.14.5, pytest 8.3.5.

**Evidence:** VS Code terminal outputs recorded the focused failures before repair, focused passing tests after repair, and full-suite passing result before refactoring. The Git log confirmed repair commit `2b641de`, and `git status --short` returned no changes immediately after the commit.

**Conclusion:** Both defects were repaired using minimal changes. Their focused regression tests passed, and the complete existing test suite passed with no reported failures. This provides the verified passing baseline for the separate behaviour-preserving refactoring activity in Section H.

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
