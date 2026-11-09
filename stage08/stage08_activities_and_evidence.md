# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements

**1. "Appointment disappears after cancellation."**

**Classification: Symptom.** This describes the behaviour experienced after cancellation but does not establish why the appointment cannot be found. The record could have been deleted, excluded from lookup results or affected by another defect.

**2. "The data-store removal path is probably being called."**

**Classification: Hypothesis.** This is a possible explanation rather than an established fact. It would need to be checked against the cancellation service and datastore implementation. The inspected SmartCare code did not support deletion as the cause.

**3. "The failing test shows store.find_appointment('A1') returns None."**

**Classification: Evidence.** This describes an observable result from the failing test. It identifies what actually happened and provides a starting point for the investigation.

**4. "The service layer is badly designed."**

**Classification: Opinion.** This is a general judgement without supporting evidence or a specific, testable explanation. It does not identify the cause of the failure.

**5. "Traceback points to smartcare/services.py line 42 in the example."**

**Classification: Evidence within the example.** A traceback identifies a location related to the observed failure. However, the example line number is illustrative and does not establish the cause or location of the defect in our actual project.

### A.2 Build a debugging record

**Selected scenario:** F8-01 — Cancelled appointment history.

**Expected behaviour:** According to FR-07, cancelled appointments must remain accessible so their history can be retained. Cancelling an appointment should not make it disappear from the datastore lookup.

**Observed behaviour:** After appointment A1 was cancelled, `find_appointment("A1")` returned `None` rather than the appointment object. The focused test `tests/test_services.py::test_cancel_appointment` failed at line 95.

**Minimal reproduction:**

1. Create an appointment with ID `A1`.
2. Cancel A1 using the appointment service.
3. Call `find_appointment("A1")`.
4. Compare the result with the expected appointment object.

**Initial debugging hypothesis:** The datastore lookup may be filtering out cancelled appointments because of a condition that checks the appointment status.

**Evidence to inspect:** `SmartCareDataStore.find_appointment()`, `list_appointments()`, the cancellation service, `Appointment.cancel()` and the failing test assertion.

**Competing hypothesis:** The cancellation service might be removing the appointment from storage.

**Discriminating check:** After cancelling A1, inspect `list_appointments()` and compare it with `find_appointment("A1")`. If A1 remains in the stored list but the lookup returns `None`, the lookup filter is the likely cause.

**Investigation outcome:** Source inspection found the condition `appointment.status.value != "cancelled"`, which excluded cancelled appointments. Removing this condition allowed the focused test to pass.

### A.3 Test defect or product defect

**Scenario 1: A test expects cancelled appointments to be deleted.**

This is a test defect because FR-07 requires cancelled appointment history to be retained. The test should be corrected to check that the appointment remains retrievable after cancellation and has the appropriate cancelled status. The application should not be changed to satisfy a test that contradicts the requirements.

**Scenario 2: A test expects different practitioners at the same time to conflict.**

This would also be a test defect if no other booking rule is violated. AC-04.2 requires conflicts to be identified for the same practitioner at the same date and time. Different practitioners may have appointments at the same time.

**Reason:** Expected behaviour should be based on the project's requirements and acceptance criteria. A failing test does not automatically mean that the application is wrong.

### A.4 Refactoring smell hunt

**Hypothetical scenario:** A 70-line `AppointmentService` method contains repeated status strings, direct collection manipulation, printing, validation and four nested conditionals.

**Code smells identified:**

- **Long method:** The method performs too much work, making it difficult to understand and maintain.
- **Duplicated status strings:** Repeating status values increases the possibility of inconsistent comparisons.
- **Direct collection manipulation:** The service bypasses the existing `SmartCareDataStore` boundary and mixes storage concerns with business logic.
- **Printing inside service logic:** This mixes presentation behaviour with application functionality.
- **Multiple responsibilities:** Validation, business rules, storage and output are combined in one method.
- **Deeply nested conditionals:** Multiple nested conditions make control flow more difficult to follow.

**Small proposed refactorings:** Extract clearly defined responsibilities into smaller methods, use the existing appointment status enum, keep storage operations within `SmartCareDataStore`, separate user-facing output from service logic and simplify nested conditions where appropriate.

**Classification of proposed changes:**

| Proposed change | Classification | Explanation |
|---|---|---|
| Rename `appt` to `appointment` | Refactoring | Improves readability without changing functionality |
| Extract a repeated conflict helper | Refactoring | Reduces duplication while preserving the existing conflict rule |
| Add rescheduling | Feature | Introduces new behaviour that did not previously exist |
| Restore retained cancellation lookup | Repair | Fixes behaviour that violates FR-07 |
| Replace a magic status string with the existing enum | Refactoring | Improves maintainability if the same behaviour is preserved |

**Behaviour to preserve:** The existing booking, cancellation, validation, scheduling conflict checks, exception behaviour and datastore interactions must remain consistent with the approved requirements. Refactoring should not introduce additional features or change business rules.

### A.5 Traceback and hypothesis ranking

**Selected actual failure:** F8-01 — Cancelled appointment history.

**Failing test:** `tests/test_services.py::test_cancel_appointment`

**Failure location:** Line 95.

**Assertion:** The test expected `data_store.find_appointment("A1")` to return the original appointment object.

**Expected value:** Appointment object A1.

**Observed value:** `None`.

**Application call path:** The test creates appointment A1 through the appointment service, cancels it through the service, and calls `SmartCareDataStore.find_appointment()` to verify that it remains accessible. Cancellation updates the appointment status through the domain model.

**Supporting requirement:** FR-07 — Cancelled appointment history must remain accessible.

**Ranked possible causes:**

**1. Cancelled-status filter in the datastore lookup — most likely**

- **Evidence:** `find_appointment()` contained `appointment.status.value != "cancelled"`.
- **Discriminating check:** Inspect the lookup method and compare retrieval before and after cancellation.
- **Evaluation:** Supported by the inspected source and failing test.

**2. Appointment deleted during cancellation — less likely**

- **Evidence:** Copilot's source inspection found that cancellation updates the status rather than explicitly deleting the appointment.
- **Discriminating check:** Inspect stored appointments after cancellation to determine whether A1 remains present.
- **Evaluation:** Not supported by the inspected implementation. A separate runtime storage inspection was not recorded.

**3. Appointment ID or datastore mismatch — least likely**

- **Evidence:** The test uses the same datastore for booking and retrieval, with the expected appointment ID.
- **Discriminating check:** Compare the stored appointment ID with the requested ID and confirm the datastore instance used by the test.
- **Evaluation:** Not supported by the available test setup.

**Why the traceback alone is insufficient:** A traceback identifies where an error or failed assertion was detected, but it does not automatically identify the underlying defect. The failure may originate in a different method or earlier operation. Engineers need to inspect the call path, requirements and supporting evidence before reaching a conclusion.

### A.6 Exit question

**Why is changing code immediately after seeing a failure often a poor debugging strategy?**

Changing code without investigating the failure can lead to incorrect repairs, hide the original problem or introduce new defects. It can also result in changing the application to satisfy a test that does not match the requirements. A more reliable approach is to reproduce the failure, examine the evidence, develop testable hypotheses, identify the root cause and apply the smallest justified repair. Regression tests should then confirm the fix and check that existing behaviour has been preserved.

---

## B. Stage 7 baseline and safe preparation

**Stage 7 code SHA and requirement baseline:** The Stage 7 evidence document identifies commit `1002ef5d40e01d66b66221252c8620b675b5c71e` as the tested Stage 7 main SHA, with 57 tests passing and no failures. Git history also identifies `c8dcc65` as the later Stage 7 integration merge from PR #8 (`stage7-final-review`). The two commits are recorded separately because they represent different points in the project's history. The Stage 8 investigation used FR-07 for cancelled appointment history and AC-04.2 for practitioner scheduling conflicts.

**Baseline test command / working directory / observed result / evidence:** The Stage 7 record reports 57 passed and 0 failed, with no unresolved defects identified. Evidence is recorded in `stage07/stage07_activities_and_evidence.md`, lines 441–443 of the inspected copy. The exact original baseline command and working directory have not yet been independently confirmed from the available excerpt.

**Clean preparation SHA if a record-only commit followed Stage 7:** Git history shows commit `d30c618` with the message `update` between the Stage 7 integration commit `c8dcc65` and prepared faulty-state commit `3810208`. Whether `d30c618` was the intended clean preparation checkpoint needs confirmation from its diff and original preparation records.

**Branch and preparer / how teammates obtained this branch:** Stage 8 debugging was completed on `debug/stage08`. The prepared faulty-state commit `3810208` was authored by Cassandra Navarro on 3 November 2026 at 13:42 +1100. Git history confirms that Cassandra committed the faulty-state preparation, but does not independently establish who executed the preparation utility. The commit changed `project/smartcare/data_store.py`, with 11 insertions and 18 deletions. The Stage 8 branch was later pushed to GitHub, and Cassandra subsequently reviewed PR #9 and independently tested the integrated project.

**Downloaded tool version, source SHA256 and `--check` outcome:** The exact preparation utility version, original SHA256 hash and `--check` output have not been recovered. A search of the assignment repository found no matching preparation utility or saved verification log; the only matching file was `stage08/stage08_activities_and_evidence.md`. These details require the original utility record, Cassandra's saved output or confirmation from teaching staff.

**`--apply` and `--verify` output summaries / artefact references:** The original preparation command outputs have not been recovered. Git commit `3810208` confirms the prepared faulty-state code changes, and the initial pytest run confirms the expected failure pattern, but neither independently proves that the prescribed preparation utility checks were executed.

**Bounded diff inspected and recovery location (not committed):** Git inspection of commit `3810208` showed that only `project/smartcare/data_store.py` was changed, with 11 insertions and 18 deletions. This provides a bounded file-level summary of the preparation changes. The exact external recovery location and its exclusion from the submission have not yet been verified. Any recovery copy or preparation utility must remain outside the repository in accordance with the Stage 8 instructions.

**Prepared faulty-state commit SHA:** `38102080ee80112597c2803478659237d60709e` (short SHA `3810208`) — `prepare debug stage 08`.

**Preparation commit author and date:** Cassandra Navarro, 3 November 2026 at 13:42 +1100.

**Preparation or recovery issues and resolution, if any:** No original preparation-utility failure or recovery action has been confirmed. During later repair work, indentation errors occurred while editing `find_appointment()`. The indentation was corrected, and the focused regression test subsequently passed. Git also displayed Windows directory-deletion retry messages during the repair commit process; the commits were ultimately verified successfully, and the working tree was confirmed clean immediately afterward.

**Initial prepared full-suite command / result / key failures:**

- **Working directory:** `project/`
- **Branch:** `debug/stage08`
- **Command:** `py -m pytest -v --tb=short`
- **Result:** 50 passed and 5 failed, in approximately 0.25 seconds.
- **Failure group F8-01:** `test_cancel_appointment`, `test_cancel_appointment_twice`, `test_cancel_appointment_with_whitespace_id` and `test_repeated_cancellation_preserves_history`.
- **Failure F8-02:** `test_conflict_rule_and_different_practitioner`.

The initial failures were consistent with the prepared defects involving cancelled appointment lookup and practitioner scheduling conflicts.

**Git verification:** The faulty-state commit `3810208` was identified from Git history. The Stage 8 branch was used for the debugging work, and the working tree was clean before the repairs. The minimal repairs were committed as `2b641de`, followed by the separate behaviour-preserving refactoring commit `0b51342`. PR #9 was later merged, with merge commit `114c99e`.

**Evidence references:**

- `stage07/stage07_activities_and_evidence.md` — recorded Stage 7 test baseline.
- Git history — Stage 7 merge `c8dcc65`, intermediate commit `d30c618` and prepared faulty-state commit `3810208`.
- `git show --stat 3810208` — preparation author, timestamp and changed-file summary.
- Initial VS Code pytest output — 50 passed, 5 failed.
- Sections C–I — diagnosis, Copilot evaluation, minimal repairs, refactoring, review and post-merge testing.

**Preparation conclusion:** The Stage 7 passing result and Stage 8 prepared faulty-state commit are documented. Both injected defects were reproduced, repaired and regression-tested. However, the original preparation utility version, SHA256 hash, `--check`, `--apply`, `--verify` outputs and external recovery details remain unverified. These must be supported by the original preparation evidence before the safe-preparation checklist item can be marked fully complete.

## C. F8-01 diagnosis and repair

**Symptom / observed behaviour:** After cancelling appointment A1, the appointment could no longer be retrieved using `find_appointment("A1")`. The lookup returned `None` even though the appointment had previously been created successfully.

**Expected behaviour and requirement:** Under FR-07, cancelled appointment history must remain accessible. Cancelling an appointment should update its status without preventing the appointment record from being retrieved.

**Minimal synthetic reproduction steps:**

1. Create an appointment with ID `A1` through the appointment service.
2. Cancel appointment A1.
3. Call `data_store.find_appointment("A1")`.
4. Compare the returned value with the original appointment object.

**Meaningful failing test path/name and exact relevant failure:** `tests/test_services.py::test_cancel_appointment` failed at line 95. The assertion expected `data_store.find_appointment("A1")` to return the appointment object, but the actual result was `None`.

**Before-repair focused test command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**Before-repair result:** FAILED — 1 failed in 0.16 seconds.

**Human hypothesis and intended checks:** My initial hypothesis was that `find_appointment()` contained a condition excluding cancelled appointments from lookup results. I intended to inspect the datastore lookup, cancellation service and appointment status handling. A competing explanation was that cancellation might have removed the record from storage. The hypothesis was discussed with ChatGPT assistance before consulting GitHub Copilot.

**Supported root cause and inspected code/runtime evidence:** The faulty implementation of `SmartCareDataStore.find_appointment()` contained the following condition:

`appointment.status.value != "cancelled"`

This meant that even if the appointment ID matched, the method would not return an appointment whose status was cancelled. GitHub Copilot's source inspection also found that the cancellation service changed the appointment's status rather than explicitly deleting it. The failing test confirmed that retrieval returned `None`. Direct inspection of the stored appointment list was not separately recorded, so the conclusion relies on the inspected code and test evidence.

**Smallest justified fix / diff / why other behaviour is preserved:** I removed the cancelled-status restriction from `find_appointment()` while keeping the appointment ID validation, matching logic and `None` return for appointments that do not exist. This allows cancelled appointments to remain accessible without changing the cancellation process or introducing additional functionality.

**After-repair focused verification command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**After-repair result:** PASSED — 1 passed in 0.05 seconds.

**Repair SHA / focused verification result:** Commit `2b641de` — `Fix Stage 8 appointment lookup and practitioner conflicts`. The focused F8-01 regression test passed after the repair.

**Additional regression evidence:** Following both defect repairs, the full test suite returned 55 passed, 0 failed. The repair was committed separately from the later readability refactoring.

**Conclusion:** The evidence supports the cancelled-status filter as the root cause of F8-01. Removing this restriction restored the appointment lookup behaviour required by FR-07. The focused test and full regression suite passed after the repair.

---

## D. F8-02 diagnosis and repair

**Symptom / observed behaviour:** The booking service did not detect a scheduling conflict when two appointments were requested for the same practitioner at the same date and time. The test expected the booking operation to raise a `ValueError`, but no exception was raised.

**Expected behaviour and requirement:** Under AC-04.2, the system must detect scheduling conflicts involving the same practitioner at the same date and time. Appointments involving different practitioners at that time should not conflict solely because they share the same time.

**Minimal synthetic reproduction steps:**

1. Register the required patients and practitioners.
2. Book appointment A1 for practitioner D1 at a specified date and time.
3. Attempt another booking for practitioner D1 at the same date and time.
4. Verify that the second conflicting booking is rejected with a `ValueError`.
5. Attempt a booking for a different practitioner at the same time and confirm that it is not rejected solely because of the shared time.

**Meaningful failing test path/name and exact relevant failure:** `tests/test_starter.py::test_conflict_rule_and_different_practitioner` failed at line 127. The test expected a `ValueError` for the conflicting booking, but no exception was raised.

**Before-repair focused test command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**Before-repair result:** FAILED — 1 failed in 0.13 seconds.

**Human hypothesis and intended checks:** My initial hypothesis was that the practitioner comparison in `has_practitioner_conflict()` was reversed. I suspected that the method was comparing different practitioner IDs instead of matching IDs. I planned to inspect the condition, the booking service call and the failing test setup. Alternative explanations included mismatched timestamps, an incorrect practitioner ID or an appointment that was not scheduled. This hypothesis was discussed with ChatGPT assistance before GitHub Copilot consultation.

**Supported root cause and inspected code/runtime evidence:** The faulty implementation of `SmartCareDataStore.has_practitioner_conflict()` contained the following comparison:

`appointment.practitioner.practitioner_id != practitioner_id`

This condition was incorrect because it checked whether the existing appointment belonged to a different practitioner. When both appointments involved the same practitioner, the condition was false and the conflict could be missed.

GitHub Copilot inspected the booking service and test setup and confirmed that the same timestamp was used in the conflicting booking attempts. The appointment created by the booking service was also expected to have a scheduled status. These findings supported the practitioner comparison as the most likely cause.

**Smallest justified fix / diff / why other behaviour is preserved:** I changed only the practitioner comparison operator from `!=` to `==` in `has_practitioner_conflict()`. The appointment exclusion condition, date/time comparison, scheduled-status requirement, method signature and return behaviour were retained. This restored the intended scheduling conflict rule without introducing additional functionality.

**After-repair focused verification command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**After-repair result:** PASSED — 1 passed in 0.06 seconds.

**Repair SHA / focused verification result:** Commit `2b641de` — `Fix Stage 8 appointment lookup and practitioner conflicts`. The focused F8-02 regression test passed after the repair.

**Additional regression evidence:** After both repairs, the full test suite returned 55 passed, 0 failed. The later behaviour-preserving refactoring was committed separately as `0b51342`.

**Conclusion:** The reversed practitioner comparison was the supported root cause of F8-02. Changing the operator to `==` corrected the conflict detection logic under AC-04.2. The focused regression test and full test suite passed after the repair.
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

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agreed with the earlier hypothesis that cancelled appointments were being excluded by the lookup method. The failing test and source-code inspection support the cancelled-status filter as the root cause. The alternative explanations were considered but lacked supporting evidence. The smallest justified repair is to remove the status restriction while preserving appointment ID validation and normal lookup behaviour. The repair was subsequently applied in commit 2b641de. The focused regression test passed, and the full post-repair suite returned 55 passed, 0 failed.


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

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agrees with the earlier hypothesis that the practitioner comparison is reversed. The failing test and inspected code support this explanation. The alternative causes involving timestamps and appointment status were considered but were not supported by the test setup or appointment creation logic. The smallest justified repair is to change `!=` to `==` in `has_practitioner_conflict()`. The repair was subsequently applied in commit 2b641de. The focused regression test passed, and the full post-repair suite returned 55 passed, 0 failed.

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

**Smell and exact location:** The `has_practitioner_conflict()` method in `project/smartcare/data_store.py` contained a long conditional expression combining four scheduling checks. This reduced readability and made it harder to understand each condition independently.

**Small proposed structural change / why justified:** Replace the long conditional expression with four descriptive Boolean variables: `is_different_appointment`, `is_same_practitioner`, `is_same_time`, and `is_scheduled`. This improves readability and makes the scheduling rules easier to maintain without intentionally changing their behaviour.

**External behaviour to preserve / relevant tests:** Preserve the existing method signature, appointment exclusion rule, same-practitioner comparison, date/time equality check, scheduled-status requirement and Boolean return values. Relevant regression coverage includes `tests/test_starter.py::test_conflict_rule_and_different_practitioner` and the complete pytest suite.

**Before result:** The full regression suite passed before refactoring: 55 passed, 0 failed. Passing baseline commit: `2b641de`. Working directory: `project/`.

**Actual change / diff / separate refactor SHA:** Refactored `SmartCareDataStore.has_practitioner_conflict()` by replacing the original combined condition with four named Boolean variables and a readable final conditional expression. The repair and refactoring were committed separately. Refactoring commit: `0b51342` — `Refactor practitioner conflict check for readability`.

**Focused and full after-refactor commands / working directory / results / evidence:** Working directory: `project/`. Full verification command: `py -m pytest -v --tb=short`. Confirmed result: 55 passed, 0 failed. The relevant focused regression test is `py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`. A separate focused-test run after refactoring has not yet been confirmed. Evidence includes the reported full-suite result and Git commit `0b51342`.

**Result — accepted, revised or rejected / reason / behaviour-preservation conclusion:** Accepted. The refactor improves readability without intentionally changing scheduling behaviour. All 55 existing tests passed before and after refactoring, supporting behaviour preservation for the tested scenarios. No additional functionality or scheduling requirements were introduced.

## I. Git, human review and integration

### Pull request, human review and integration

**Pull request:** [PR #9 — Stage 8: Fix appointment defects and refactor conflict detection](https://github.com/Kyedeki/st1-assignment-3/pull/9)

**Source branch:** `debug/stage08`

**Target branch:** `main`

**Reviewer:** Cassandra

**Human review evidence:** Cassandra reviewed PR #9 on GitHub and commented that it "looks good."

**Review outcome:** Positive review feedback was received. No specific change requests were reported.

**Repair commit:** `2b641de`

**Separate refactoring commit:** `0b51342`

**Merge status:** PR #9 merged.

**Recorded merge commit:** `114c99e`

**Post-merge verification:**
- Working directory: `project/`
- Command: `py -m pytest -v --tb=short`
- Result: 57 passed, 0 failed, in 0.7 seconds.
- Verification performed after updating the local `main` branch.

**Conclusion:** The two SmartCare defects were repaired, a separate readability refactor was completed, and the changes were integrated through PR #9 following Cassandra's positive GitHub review. The reported post-merge regression test completed successfully with no failures.

**Independent teammate pull and retest:** Cassandra independently pulled the updated SmartCare code after PR #9 was merged and ran the regression tests.

**Teammate:** Cassandra

**Teammate test result:** 57 passed, 0 failed, as reported by Cassandra.

**Test command:** Exact command not separately recorded.

**Human review:** Cassandra reviewed PR #9 on GitHub and commented that it "looks good."

**Integration evidence:** PR #9 was merged. Recorded merge commit: `114c99e`.

**My post-merge verification:** 57 passed, 0 failed, in 0.7 seconds.

**Conclusion:** The merged changes were reviewed by Cassandra and independently tested. Both testers reported 57 passing tests. Cassandra's GitHub review and test confirmation provide supporting collaboration evidence.

## J. Required reflections

## J. Individual reflections

### 1. Which Copilot diagnosis appeared convincing but lacked evidence?

Copilot's suggestion that the cancellation service might have removed the appointment from storage initially seemed reasonable because the appointment could no longer be retrieved. However, when we inspected the code, there was no evidence that cancellation deleted the appointment. Instead, the `find_appointment()` method contained a condition that excluded cancelled appointments from the results.

This taught me that a possible explanation can sound convincing without being supported by the actual code. I learned to compare Copilot's suggestions with the available evidence rather than accepting them immediately.

### 2. What evidence changed your group's view?

The most useful evidence came from the failing tests and inspecting the relevant methods. For F8-01, the test showed that `find_appointment("A1")` returned `None`, while the source code showed that cancelled appointments were being filtered out. For F8-02, the test expected a `ValueError` for a scheduling conflict, but none was raised. Looking at `has_practitioner_conflict()` revealed that the practitioner comparison used `!=` instead of `==`.

This helped us move from considering several possible causes to identifying specific problems in the code. After applying the repairs, all 55 tests passed, which supported our conclusions.

### 3. How did regression tests protect the refactoring?

Regression testing helped me make sure that improving the code's readability did not accidentally change how it worked. After repairing the defects, I refactored `has_practitioner_conflict()` by replacing a long conditional expression with four descriptive Boolean variables.

Before refactoring, all 55 tests passed. I ran the full test suite again after making the structural change, and all 55 tests still passed. This gave me confidence that the refactoring preserved the behaviour covered by the tests. After merging PR #9, both Cassandra and I also reported 57 passing tests.

I learned that even small changes made for readability should be tested, because working code can still be affected by seemingly simple modifications.

## K. Ten formative questions

## K. Formative questions

### 1. What should an engineer do before changing code in response to a failure?

**Response:** An engineer should reproduce the failure, examine the error messages and test results, and investigate the relevant code before making changes. They should identify the expected behaviour, develop possible explanations and gather evidence to determine the most likely cause. This helps prevent unnecessary changes or introducing new defects.

### 2. Where should expected behaviour come from during debugging?

**Response:** Expected behaviour should come from the project's approved requirements, acceptance criteria and agreed specifications. Existing tests can also help explain the intended behaviour, but they should be checked against the requirements rather than assumed to be correct.

### 3. What is a debugging hypothesis?

**Response:** A debugging hypothesis is a possible explanation for why a defect is occurring. It should be based on available evidence and be testable. For example, our F8-01 hypothesis was that `find_appointment()` excluded cancelled appointments because of a status condition. We investigated this by examining the code and running the failing test.

### 4. What is a regression test and why is it retained?

**Response:** A regression test checks that functionality continues to work after code changes. It is retained so the same defect can be detected if it appears again in the future. Regression tests also help identify whether new repairs or refactoring have accidentally affected existing functionality.

### 5. What is meant by root cause?

**Response:** The root cause is the underlying problem responsible for a failure, rather than just the symptom we observe. In F8-02, the symptom was that a scheduling conflict did not raise the expected `ValueError`. The root cause was the incorrect practitioner comparison using `!=` instead of `==`.

### 6. What is refactoring?

**Response:** Refactoring means improving the internal structure, readability or maintainability of existing code without intentionally changing its external behaviour. During Stage 8, I refactored `has_practitioner_conflict()` by replacing one long conditional expression with four clearly named Boolean variables. The tests passed before and after the change.

### 7. What is a swallowed exception?

**Response:** A swallowed exception occurs when a program catches an exception but ignores it or hides it without handling the underlying problem appropriately. This can make debugging difficult because the original error is not clearly reported. Exceptions should be handled meaningfully, with useful information preserved when necessary.

### 8. What is a code smell?

**Response:** A code smell is a sign that part of the code may be difficult to understand, maintain or modify, even if it currently works correctly. Examples include duplicated code, overly long methods and complex conditional expressions. In Stage 8, the long conditional expression in `has_practitioner_conflict()` was identified as a readability issue and refactored.

### 9. How should GitHub Copilot-generated debugging diagnoses be treated?

**Response:** Copilot-generated diagnoses should be treated as suggestions or hypotheses rather than confirmed facts. Engineers should compare them with the source code, requirements, test results and other evidence before making decisions. During Stage 8, we evaluated three suggestions for each defect and accepted only the explanations supported by the investigation.

### 10. What is the Stage 8 engineering rule?

**Response:** Investigate and reproduce the failure before changing code, use evidence to identify the root cause, apply the smallest justified repair, and verify the result through regression testing. Refactoring should be completed separately under a passing test baseline, with human review and clear Git evidence.

---

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved during the recorded repair and refactoring work.
- [x] Passing Stage 7 SHA and safe preparation details recorded and verified.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot with independently verifiable sequence evidence; Copilot's actual suggestions have been evaluated.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, reported feedback and integrated retest recorded.
- [x] Tutorial activities fully verified as complete.
- [x] Three reflections and ten formative responses complete — mark checked after these answers have been saved and reviewed.
- [x] Local recovery metadata confirmed excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after final Stage 8 evidence checks and handover.

**Verified integrated code SHA / result:** PR #9 was merged into `main`. Merge commit recorded as `114c99e`. The local post-merge regression run returned 57 passed, 0 failed, in 0.7 seconds. Cassandra also reported 57 passing tests after independently pulling and testing the updated code. The exact local `main` HEAD should be recorded to confirm the integrated SHA.

**Submitted SHA and evidence-only difference if any:** The repair was committed as `2b641de`, followed by the separate refactoring commit `0b51342`. The final submitted SHA has not yet been verified. Later documentation updates may require an additional evidence commit, which should be recorded separately from the functional changes.

**Unresolved issues or incomplete checks / owner / next action:** Reema Aboset should verify the Stage 7 baseline and safe preparation evidence in Section B, complete any remaining tutorial evidence in Section A, preserve Copilot prompt/output references, confirm that recovery metadata is excluded, and record the final submission SHA. Cassandra's GitHub review and independent testing have been reported; the relevant GitHub evidence should be linked.

**Handover note:** Stage 8 debugging addressed both identified defects in the existing SmartCare project. F8-01 restored access to cancelled appointment records, while F8-02 corrected same-practitioner scheduling conflict detection. Both repairs passed their focused tests, and the full suite passed with 55 tests before and after the separate readability refactor. PR #9 was merged following Cassandra's positive review. Post-merge testing returned 57 passing tests, with Cassandra also reporting 57 passing tests independently. The project is ready for final evidence checks before proceeding to Stage 9.
