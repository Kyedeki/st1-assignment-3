# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 2 Monday 2:30-4:30
Members and UG/PG cohorts: Cassandra Navarro | Reema Majed M 
Record owner / contribution links for each member: 
Cassandra Navarro: Section B Revision and Stage 8 Feedback 
Reema Majed M: Completion of Stage 8 | https://github.com/Kyedeki/st1-assignment-3/pull/11

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

**Stage 7 code SHA and requirement baseline:** The Stage 7 evidence record identifies commit `1002ef5d40e01d66b66221252c8620b675b5c71e` as the tested Stage 7 main SHA, with 57 tests passing and 0 failures. Git history identifies `c8dcc65` as the later Stage 7 integration merge from PR #8 (`stage7-final-review`). These are separate checkpoints. The SmartCare requirements relevant to Stage 8 include FR-05 and AC-04.1/AC-04.2 for practitioner scheduling conflicts, and FR-06/FR-07, BR-07, FR-08 and AC-05.2 for cancellation and retained appointment history.

**Baseline test command / working directory / observed result / evidence:** The Stage 7 record reports 57 passed, 0 failed, with no unresolved defects identified. Evidence: `stage07/stage07_activities_and_evidence.md`, lines 441–443. The Stage 8 handout specifies running the baseline suite from `project/` using `python -m pytest -q`. The exact command used for the recorded Stage 7 test run has not been independently confirmed.

**Clean preparation SHA if a record-only commit followed Stage 7:** record.json confirms the preparation SHA was 'd30c618', this means that the parent of the faulty commit 3810208

**Branch and preparer / how teammates obtained this branch:** Stage 8 debugging was conducted on `debug/stage08`. Commit `3810208`, titled `prepare debug stage 08`, was authored by Cassandra Navarro on 3 November 2026 at 13:42 +1100. The commit changed `project/smartcare/data_store.py`, with 11 insertions and 18 deletions. This confirms who committed the prepared faulty state, but not who executed the preparation utility. The branch was later pushed to GitHub and used for the group's debugging and review work.

**Downloaded tool version, source SHA256 and `--check` outcome:** Tool version 1.1 is confirmed in record.json. The original utility hash and --check output because the tutor's asset folder was deleted

**`--apply` and `--verify` output summaries / artefact references:** The handout specifies `python ../Stage_8_Assets/prepare_debugging.py project --apply` followed by `python ../Stage_8_Assets/prepare_debugging.py project --verify`. The original execution outputs have not been recovered. The prepared-state commit and subsequent failing tests establish that the faulty code was present, but do not independently prove the utility's successful execution. The metadata records status: prepared, but the original execution outputs could not be recovered

**Bounded diff inspected and recovery location (not committed):** Git inspection of commit `3810208` shows that only `project/smartcare/data_store.py` changed, with 11 insertions and 18 deletions. The official handout specifies `project/.stage8_faults/` for local backup and recovery metadata, excluded from Git. If the utility was temporarily supplied, its location should be a sibling `Stage_8_Assets/` folder outside the repository. The original recovery folder's existence and location on the preparer's computer have not been independently confirmed.

**Prepared faulty-state commit SHA:** `38102080ee80112597c2803478659237d60709e` (short SHA `3810208`) — `prepare debug stage 08`.

**Preparation or recovery issues and resolution, if any:** No original preparation utility failure or recovery action has been confirmed. During the later repair process, indentation errors occurred while editing `find_appointment()`. These were corrected, and the focused regression test passed. Git also displayed Windows directory-deletion retry prompts, but the subsequent repair and refactoring commits were successfully verified.

**Initial prepared full-suite command / result / key failures:**

- **Working directory:** `project/`
- **Branch:** `debug/stage08`
- **Command:** `py -m pytest -v --tb=short`
- **Result:** 50 passed, 5 failed, in approximately 0.25 seconds.
- **F8-01 — Practitioner scheduling conflict:** `tests/test_starter.py::test_conflict_rule_and_different_practitioner` failed because a conflicting booking did not raise `ValueError`.
- **F8-02 — Cancelled appointment history:** Four cancellation-related tests failed: `test_cancel_appointment`, `test_cancel_appointment_twice`, `test_cancel_appointment_with_whitespace_id` and `test_repeated_cancellation_preserves_history`.

**Git verification:** The faulty-state commit `3810208` was identified from Git history. The working tree was clean before repairs. Both repairs were committed as `2b641de`, followed by the separate refactoring commit `0b51342`. PR #9 was merged, with recorded merge commit `114c99e`.

**Evidence references:**

- `stage07/stage07_activities_and_evidence.md` — recorded Stage 7 test result.
- Stage 8 handout, Section 3 — controlled preparation workflow and utility version 1.1.
- Git history — `c8dcc65`, `d30c618` and `3810208`.
- `git show --stat 3810208` — preparation commit details.
- Initial pytest results — 50 passed and 5 failed.
- Sections C–I — diagnosis, repairs, Copilot analysis, refactoring and integration evidence.

**Preparation conclusion:** The Stage 7 passing result and the Stage 8 prepared faulty-state commit were identified and documented. Both defects were reproduced, repaired and regression-tested. However, the original preparation utility's SHA256 hash, actual execution outputs and recovery details remain unverified. These require supporting evidence before the safe-preparation requirement can be marked fully complete.

## C. F8-01 diagnosis and repair

**Symptom / observed behaviour:** The booking service failed to detect a scheduling conflict when another appointment was requested for the same practitioner at the same date and time. The test expected a `ValueError`, but no exception was raised.

**Expected behaviour and requirement:** Under FR-05 and AC-04.1, the system must reject conflicting scheduled appointments for the same practitioner at the same date and time. AC-04.2 permits different practitioners to have appointments at the same time, provided no other booking rule is violated. A rejected booking should not modify the existing stored appointment.

**Minimal synthetic reproduction steps:**

1. Register the required patients and two practitioners, D1 and D2.
2. Create appointment A1 for practitioner D1 at a specified date and time.
3. Attempt another appointment with a different ID for practitioner D1 at the same time.
4. Verify that the conflicting booking raises `ValueError`.
5. Attempt a booking for practitioner D2 at the same time and check that it is permitted.
6. Confirm that the rejected booking has not added an appointment to the datastore.

**Meaningful failing test path/name and exact relevant failure:** `tests/test_starter.py::test_conflict_rule_and_different_practitioner` failed at line 127. The test expected a `ValueError`, but the booking operation did not raise an exception.

**Before-repair focused test command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**Before-repair result:** FAILED — 1 failed in 0.13 seconds.

**Human hypothesis and intended checks:** My initial hypothesis was that the practitioner comparison in `has_practitioner_conflict()` was reversed. I suspected that it was checking for different practitioner IDs instead of matching IDs. I planned to inspect the condition, the booking service call and the failing test setup. Alternative explanations included mismatched timestamps, an incorrect practitioner ID or an appointment that was not scheduled. This hypothesis was discussed with ChatGPT assistance before consulting GitHub Copilot.

**Supported root cause and inspected code/runtime evidence:** The faulty implementation of `SmartCareDataStore.has_practitioner_conflict()` contained the comparison:

`appointment.practitioner.practitioner_id != practitioner_id`

This condition checked for different practitioners instead of the same practitioner. When both appointments involved D1, the practitioner comparison was false and the conflict could be missed.

GitHub Copilot inspected the booking service and confirmed that the conflict checker was called with the requested practitioner ID and timestamp. The test setup reused the same timestamp for the conflicting booking attempts, and the existing appointment was expected to have a scheduled status. These observations supported the reversed comparison as the root cause.

**Smallest justified fix / diff / why other behaviour is preserved:** I changed the practitioner comparison from `!=` to `==` in `has_practitioner_conflict()`. The appointment exclusion condition, date/time comparison, scheduled-status requirement, method signature and Boolean return behaviour were preserved. No additional booking rules or features were introduced.

**After-repair focused verification command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**After-repair result:** PASSED — 1 passed in 0.06 seconds.

**Repair SHA / focused verification result:** Commit `2b641de` — `Fix Stage 8 appointment lookup and practitioner conflicts`. The focused practitioner conflict regression test passed after the repair.

**Additional regression evidence:** After both repairs, the full suite returned 55 passed, 0 failed. The later readability-only refactoring was committed separately as `0b51342`.

**Conclusion:** The reversed practitioner comparison was the supported root cause of F8-01. Changing the comparison to `==` restored the required practitioner conflict detection behaviour. The focused regression test and the full existing test suite passed after the repair.

---

## D. F8-02 diagnosis and repair

**Symptom / observed behaviour:** After cancelling appointment A1, the appointment could no longer be retrieved using `find_appointment("A1")`. The datastore lookup returned `None`, even though the appointment had previously been created successfully.

**Expected behaviour and requirement:** Under FR-06, FR-07 and BR-07, cancellation must follow the guarded appointment status transition while retaining the appointment's history. FR-08 requires appointment lookup, and AC-05.2 protects retained cancellation history. A cancelled appointment should remain accessible through the same datastore during the session.

**Minimal synthetic reproduction steps:**

1. Register the required patient and practitioner.
2. Create appointment A1 through the appointment service.
3. Cancel A1 using `cancel_appointment("A1")`.
4. Inspect the appointment's cancelled status and check its membership in `list_appointments()`.
5. Call `data_store.find_appointment("A1")` and compare the result with the original appointment object.
6. Check the service-level lookup behaviour and verify that repeated cancellation is rejected without altering the retained appointment.

**Meaningful failing test path/name and exact relevant failure:** `tests/test_services.py::test_cancel_appointment` failed at line 95. The test expected `data_store.find_appointment("A1")` to return the appointment object, but the actual result was `None`.

**Before-repair focused test command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**Before-repair result:** FAILED — 1 failed in 0.16 seconds.

**Human hypothesis and intended checks:** My initial hypothesis was that the datastore lookup contained a condition excluding cancelled appointments from its results. I planned to inspect `find_appointment()`, `list_appointments()` and the cancellation service. A competing explanation was that cancellation might have removed the record from storage. This hypothesis was discussed with ChatGPT assistance before GitHub Copilot consultation.

**Supported root cause and inspected code/runtime evidence:** The faulty implementation of `SmartCareDataStore.find_appointment()` contained the condition:

`appointment.status.value != "cancelled"`

This prevented the method from returning appointments with a cancelled status, even when their IDs matched.

GitHub Copilot's source inspection found that the cancellation process changed the appointment's status rather than explicitly deleting it. The focused failing test confirmed that lookup returned `None`. A separate direct runtime inspection of `list_appointments()` was not recorded, so the diagnosis is supported by the inspected implementation and failing test rather than a separately captured storage inspection.

**Smallest justified fix / diff / why other behaviour is preserved:** I removed the cancelled-status restriction from `find_appointment()` while retaining appointment ID validation, matching behaviour and the `None` return value for valid appointment IDs that are not present. This restored access to cancelled appointment records without introducing a delete or save workflow or changing the cancellation transition.

**After-repair focused verification command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**After-repair result:** PASSED — 1 passed in 0.05 seconds.

**Repair SHA / focused verification result:** Commit `2b641de` — `Fix Stage 8 appointment lookup and practitioner conflicts`. The focused cancelled-appointment regression test passed after the repair.

**Additional regression evidence:** Four cancellation-related tests had failed in the prepared full-suite run. After both repairs, the full test suite returned 55 passed, 0 failed. This confirms that the existing test suite passed after the fixes, including the cancellation tests.

**Conclusion:** The evidence supports the cancelled-status lookup restriction as the root cause of F8-02. Removing this condition restored cancelled appointment retrieval as required by the published SmartCare contract. The focused regression test and full test suite passed after the repair.

## E. Human-first hypotheses

### F8-01 human entry — Practitioner scheduling conflict

**Likely cause and why plausible:** The `has_practitioner_conflict()` method appears to use `!=` instead of `==` when comparing practitioner IDs. This could cause the system to miss conflicts involving the same practitioner and incorrectly identify different practitioners as conflicting.

**Evidence intended to inspect:** The practitioner comparison in `SmartCareDataStore.has_practitioner_conflict()`, the booking service, and the test `tests/test_starter.py::test_conflict_rule_and_different_practitioner`. The test failed at line 127 because the expected `ValueError` was not raised.

**Competing explanation:** The existing and requested appointments might use different timestamps, the existing appointment might not be scheduled, or the booking service might pass an incorrect practitioner ID.

**Discriminating check:** Compare bookings for the same practitioner at the same date and time against bookings for different practitioners at that time. Examine the practitioner IDs, timestamps and appointment status to determine whether the conflict checker follows FR-05 and AC-04.1/AC-04.2.

**Member and saved sequence/time or commit:** Reema Aboset investigated this defect with ChatGPT assistance before consulting GitHub Copilot. The initial investigation included source inspection and reproducing the failing test. Prepared faulty-state commit: `3810208`. The exact timestamp or saved evidence proving the hypothesis was recorded before Copilot consultation has not been independently verified.

### F8-02 human entry — Cancelled appointment history

**Likely cause and why plausible:** The `find_appointment()` method appears to exclude cancelled appointments because it contains `appointment.status.value != "cancelled"`. This could explain why an appointment becomes inaccessible after cancellation despite the requirement to retain its history.

**Evidence intended to inspect:** The implementations of `find_appointment()`, `list_appointments()`, `cancel_appointment()` and `Appointment.cancel()`, together with the failing assertion in `tests/test_services.py::test_cancel_appointment` at line 95.

**Competing explanation:** The cancellation service might remove the appointment from storage, or the lookup might use an incorrect appointment ID or datastore instance.

**Discriminating check:** After cancelling A1, inspect the appointment's status, check whether A1 remains in `list_appointments()`, and compare that with the result of `find_appointment("A1")`. If A1 remains stored while lookup returns `None`, the status filter is responsible for the retrieval failure.

**Member and saved sequence/time or commit:** Reema Aboset investigated this defect with ChatGPT assistance before GitHub Copilot consultation. The focused failing test was reproduced and the relevant code inspected. Prepared faulty-state commit: `3810208`. The exact timestamp or saved evidence of the hypothesis's sequence relative to Copilot consultation remains to be confirmed.

---

## F. GitHub Copilot prompts, findings and human decisions

### F8-01 Copilot review — Practitioner scheduling conflict

**Actual prompt / output reference and member:** Reema Aboset consulted GitHub Copilot Chat about the practitioner scheduling conflict. The prompt included the observed failure, expected behaviour under AC-04.2, reproduction steps, failing test, initial hypothesis, competing explanations and relevant source files. Copilot was instructed to provide three ranked possible causes with evidence checks without editing files or running commands.

**Copilot output reference:** The actual F8-01 practitioner-conflict Copilot prompt and response were shared during the investigation. A saved GitHub or repository evidence reference still needs to be added.

**1. Ranked suggestion — Reversed practitioner comparison**

- **Evidence check:** Inspect the comparison in `has_practitioner_conflict()` and the arguments passed by `book_appointment()`.
- **Observed evidence:** The faulty code used `appointment.practitioner.practitioner_id != practitioner_id`. When both bookings involved D1, this comparison was false, allowing the existing scheduled conflict to be missed.
- **Evaluation:** Correct. Source inspection and the failing test support this diagnosis.
- **Human decision:** Accept. Change the comparison to `==` while preserving the other scheduling conditions.

**2. Ranked suggestion — Different appointment timestamps**

- **Evidence check:** Inspect the timestamps used in `tests/test_starter.py::test_conflict_rule_and_different_practitioner`.
- **Observed evidence:** The test created one timestamp variable, `when`, and reused it for the conflicting booking attempts. The checker compares date/time values using equality.
- **Evaluation:** Unlikely. The inspected test setup does not support a timestamp mismatch.
- **Human decision:** Reject as the supported root cause.

**3. Ranked suggestion — Existing appointment was not scheduled**

- **Evidence check:** Inspect appointment creation, its default status and the conflict check's scheduled-status condition.
- **Observed evidence:** `book_appointment()` creates an appointment whose default status is `SCHEDULED`. The inspected test setup provided no evidence of a status change before the second booking.
- **Evaluation:** Unlikely and unsupported by the inspected code.
- **Human decision:** Reject as the supported root cause.

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agreed with the earlier hypothesis that the practitioner ID comparison was reversed. The inspected source code and failing test supported this explanation more strongly than the alternative hypotheses. The repair changed `!=` to `==` in `has_practitioner_conflict()`. This was subsequently committed as `2b641de`. The focused test passed, and the full post-repair suite returned 55 passed, 0 failed.

### F8-02 Copilot review — Cancelled appointment history

**Actual prompt / output reference and member:** Reema Aboset consulted GitHub Copilot Chat after investigating the cancelled-appointment lookup failure. The prompt described the observed and expected behaviour under FR-07, reproduction steps, failing test, initial hypothesis, competing explanation and relevant code. Copilot was asked to rank three possible causes, identify supporting evidence and distinguish confirmed findings from hypotheses.

**Copilot output reference:** The actual F8-02 cancellation-history Copilot prompt and response were shared during the investigation. A saved GitHub or repository evidence reference still needs to be added.

**1. Ranked suggestion — Cancelled-status filter in the datastore lookup**

- **Evidence check:** Inspect `SmartCareDataStore.find_appointment()` and the failing cancellation test.
- **Observed evidence:** The faulty method contained `appointment.status.value != "cancelled"`, preventing cancelled appointments from being returned. The focused test failed because `find_appointment("A1")` returned `None`.
- **Evaluation:** Correct. The source code and failing test support the diagnosis.
- **Human decision:** Accept. Remove the cancelled-status restriction while preserving ID validation and normal lookup behaviour.

**2. Ranked suggestion — Appointment removed from storage during cancellation**

- **Evidence check:** Inspect `AppointmentService.cancel_appointment()`, `Appointment.cancel()` and datastore operations.
- **Observed evidence:** Copilot found that cancellation changed the appointment status without explicitly deleting the record. No appointment-removal operation was identified in the inspected implementation. A separate runtime inspection of stored A1 was not recorded.
- **Evaluation:** Unlikely and unsupported by the inspected code.
- **Human decision:** Reject as the currently supported cause, while recognising that inspecting stored appointments would provide an additional confirmation.

**3. Ranked suggestion — Appointment ID or datastore mismatch**

- **Evidence check:** Inspect appointment IDs, the test setup and datastore references.
- **Observed evidence:** The test created and retrieved A1 using the same datastore. No mismatch was identified in the inspected code.
- **Evaluation:** Unsupported and very unlikely.
- **Human decision:** Reject as the supported root cause.

**Final human conclusion and comparison with initial hypothesis:** Copilot's highest-ranked diagnosis agreed with the earlier hypothesis that cancelled appointments were filtered out during lookup. The failing test and source inspection supported this explanation. The other suggestions did not have comparable evidence. The status filter was subsequently removed, and the repair was committed as `2b641de`. The focused test passed, and the full post-repair suite returned 55 passed, 0 failed.

---

## G. Failing-to-passing regression evidence

### F8-01 — Practitioner scheduling conflict

**Requirement:** FR-05 and AC-04.1/AC-04.2 — Same-practitioner scheduling conflicts must be detected while different practitioners may have appointments at the same time.

**Before repair:** `tests/test_starter.py::test_conflict_rule_and_different_practitioner` failed at line 127 because the expected `ValueError` was not raised.

**Root cause:** The conflict checker used `appointment.practitioner.practitioner_id != practitioner_id` instead of matching practitioner IDs.

**Minimal repair:** Changed the practitioner comparison from `!=` to `==`, preserving the existing appointment exclusion, timestamp equality and scheduled-status checks.

**Focused test command:**

`py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`

**Before-repair result:** 1 failed in 0.13 seconds.

**After-repair result:** 1 passed in 0.06 seconds.

**Repair commit:** `2b641de`.

**Evidence:** Original failing-test output, passing focused-test output and the repair commit's source-code diff.

### F8-02 — Cancelled appointment history

**Requirement:** FR-06/FR-07, BR-07, FR-08 and AC-05.2 — Cancellation must preserve retained appointment history and lookup access.

**Before repair:** `tests/test_services.py::test_cancel_appointment` failed at line 95 because the datastore lookup returned `None` rather than the cancelled appointment object.

**Root cause:** `find_appointment()` excluded records whose status was `"cancelled"`.

**Minimal repair:** Removed the cancelled-status filter while preserving appointment ID validation, appointment ID matching and the missing-ID return behaviour.

**Focused test command:**

`py -m pytest tests/test_services.py::test_cancel_appointment -v --tb=short`

**Before-repair result:** 1 failed in 0.16 seconds.

**After-repair result:** 1 passed in 0.05 seconds.

**Repair commit:** `2b641de`.

**Evidence:** Original failing-test output, passing focused-test output and the repair commit's source-code diff.

### Full regression verification before refactoring

**Repository branch:** `debug/stage08`

**Working directory:** `project/`

**Prepared faulty-state commit:** `3810208`

**Repair commit:** `2b641de`

**Baseline before repairs:** 50 passed, 5 failed.

**Verification command:**

`py -m pytest -v --tb=short`

**Full-suite result after repairs:** 55 passed, 0 failed, in 0.12 seconds.

**Environment:** Windows, Python 3.14.5, pytest 8.3.5.

**Regression coverage:** The initial prepared suite contained four cancellation-related failures and one practitioner-conflict failure. After applying the two repairs, the complete existing suite passed. The focused tests were retained.

**Additional test requirement:** The Stage 8 handout also requests focused regression coverage in `project/tests/test_regressions.py`. Whether the required new or strengthened tests were added to that file has not yet been independently verified and should be checked before final submission.

**Conclusion:** Both identified defects were repaired through small changes supported by code inspection and failing tests. The focused tests passed after their respective fixes, and the full suite passed with 55 tests before refactoring. This established the passing baseline for Section H.

## H. Refactoring decision and before/after verification

**Smell and exact location:** The `has_practitioner_conflict()` method in `project/smartcare/data_store.py` contained a long conditional expression combining four scheduling checks. This reduced readability and made it harder to understand each condition independently.

**Small proposed structural change / why justified:** Replace the long conditional expression with four descriptive Boolean variables: `is_different_appointment`, `is_same_practitioner`, `is_same_time`, and `is_scheduled`. This improves readability and makes the scheduling rules easier to maintain without intentionally changing their behaviour.

**External behaviour to preserve / relevant tests:** Preserve the existing method signature, appointment exclusion rule, same-practitioner comparison, date/time equality check, scheduled-status requirement and Boolean return values. Relevant regression coverage includes `tests/test_starter.py::test_conflict_rule_and_different_practitioner` and the complete pytest suite.

**Before result:** The full regression suite passed before refactoring: 55 passed, 0 failed. Passing baseline commit: `2b641de`. Working directory: `project/`.

**Actual change / diff / separate refactor SHA:** Refactored `SmartCareDataStore.has_practitioner_conflict()` by replacing the original combined condition with four named Boolean variables and a readable final conditional expression. The repair and refactoring were committed separately. Refactoring commit: `0b51342` — `Refactor practitioner conflict check for readability`.

**Focused and full after-refactor commands / working directory / results / evidence:** Working directory: `project/`. Full verification command: `py -m pytest -v --tb=short`. Confirmed result: 55 passed, 0 failed. The relevant focused regression test is `py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v --tb=short`. A separate focused-test run after refactoring has not yet been confirmed. Evidence includes the reported full-suite result and Git commit `0b51342`.

**Result — accepted, revised or rejected / reason / behaviour-preservation conclusion:** Accepted. The refactor improves readability without intentionally changing scheduling behaviour. All 55 existing tests passed before and after refactoring, supporting behaviour preservation for the tested scenarios. No additional functionality or scheduling requirements were introduced.

## I. Git, human review and integration

### Git checkpoints and collaboration

**Repository:** `Kyedeki/st1-assignment-3`

**Prepared debugging branch:** `debug/stage08`

**Prepared faulty-state commit:** `3810208` — `prepare debug stage 08`, authored by Cassandra Navarro.

**Repair commit:** `2b641de` — `Fix Stage 8 appointment lookup and practitioner conflicts`.

**Separate refactoring commit:** `0b51342` — `Refactor practitioner conflict check for readability`.

**Defect and refactoring issue references:** Separate GitHub issue links have not yet been recorded. The two defect repairs and refactoring are documented in PR #9 and their respective commits. Issue references should be added if they were created.

### Pull request and human review

**Pull request:** [PR #9 — Stage 8: Fix appointment defects and refactor conflict detection](https://github.com/Kyedeki/st1-assignment-3/pull/9)

**Source branch:** `debug/stage08`

**Target branch:** `main`

**Reviewer:** Cassandra

**Human review evidence:** Cassandra reviewed PR #9 on GitHub and commented that it "looks good."

**Review outcome:** Positive feedback was received. No specific changes were requested in the reported review.

**Merge status:** PR #9 merged.

**Recorded merge commit:** `114c99e`.

### Post-merge integration verification

**Working directory:** `project/`

**Branch tested:** Updated local `main`.

**Verification command:**

`py -m pytest -v --tb=short`

**Observed result:** 57 passed, 0 failed, in 0.7 seconds.

**Interpretation:** The merged project passed its complete test suite. This result supports successful integration of the repaired and refactored SmartCare code. The increase from 55 to 57 tests was observed after integration, but the additional tests have not been individually identified in this record.

### Independent teammate verification

**Teammate:** Cassandra

**Activity:** Cassandra independently pulled the updated project and ran its tests.

**Reported result:** 57 passed, 0 failed.

**Human review:** Cassandra also reviewed PR #9 on GitHub and stated that the work "looks good."

**Evidence status:** The independent result was reported by Cassandra. Her exact test command, execution time and separate test output have not been recorded here.

**Conclusion:** The repairs and refactoring were integrated through PR #9 after human review. My post-merge verification and Cassandra's independent testing both reported 57 passing tests, with no failures.

### Final documentation update

**Documentation branch:** `docs/stage08-final-evidence`

**Documentation commit:** `2ed4595` — `Complete Stage 8 documentation and evidence`.

**Purpose:** Update the Stage 8 Markdown record after the original code integration without changing SmartCare's application behaviour.

**Documentation integration status:** The documentation branch was pushed to GitHub. The final documentation pull request number and merge result must be recorded separately once verified.

---

## J. Required reflections

### 1. Which Copilot diagnosis appeared convincing but lacked evidence?

Copilot's suggestion that the cancellation service might have removed the appointment from storage initially seemed reasonable because the appointment could no longer be retrieved. However, the inspected code did not show that cancellation deleted the appointment. Instead, `find_appointment()` contained a condition that excluded cancelled appointments from lookup results.

This taught me that an explanation can sound convincing without being supported by evidence. I learned to examine the code and tests before accepting a suggested cause.

### 2. What evidence changed your group's view?

The most useful evidence came from the failing tests and relevant source code. For F8-01, the test expected a `ValueError` for a practitioner scheduling conflict, but no exception was raised. Inspecting `has_practitioner_conflict()` showed that it used `!=` instead of `==` when comparing practitioner IDs.

For F8-02, the cancellation test showed that `find_appointment("A1")` returned `None`. Source inspection revealed that cancelled appointments were excluded from lookup results.

These findings helped narrow the investigation from several possible explanations to two specific code defects. After applying the repairs, the full test suite passed with 55 tests and no failures.

### 3. How did regression tests protect the refactoring?

Regression tests helped verify that improving the code's readability did not change its intended behaviour. After repairing both defects, I refactored `has_practitioner_conflict()` by replacing one long conditional expression with four descriptive Boolean variables.

Before refactoring, all 55 tests passed. I ran the full suite again afterward, and all 55 tests still passed. This provided evidence that the refactor preserved behaviour covered by the tests.

After PR #9 was merged, Cassandra and I also reported 57 passing tests. I learned that even small structural changes should be tested because readable code must still behave correctly.

---

## K. Ten formative questions

### 1. What should an engineer do before changing code in response to a failure?

**Response:** An engineer should reproduce the failure, inspect the error messages and test results, and investigate the relevant code. They should identify the expected behaviour, develop possible explanations and gather evidence before applying a repair. This reduces the risk of unnecessary changes or additional defects.

### 2. Where should expected behaviour come from during debugging?

**Response:** Expected behaviour should come from approved requirements, acceptance criteria and agreed specifications. Existing tests can help explain intended behaviour, but their expectations should be checked against the requirements rather than automatically assumed to be correct.

### 3. What is a debugging hypothesis?

**Response:** A debugging hypothesis is a testable explanation for why a failure occurs. It should be supported or rejected through evidence. For example, our F8-01 hypothesis was that the practitioner ID comparison was reversed. Source inspection and the failing test supported that explanation.

### 4. What is a regression test and why is it retained?

**Response:** A regression test checks that existing functionality continues to work after changes. It is retained to detect whether a previously fixed defect returns or whether new code changes accidentally break working behaviour.

### 5. What is meant by root cause?

**Response:** The root cause is the underlying problem responsible for a failure, rather than the symptom that was observed. In F8-02, the symptom was that a cancelled appointment could not be retrieved. The root cause was the status filter excluding cancelled appointments from datastore lookup results.

### 6. What is refactoring?

**Response:** Refactoring improves the internal structure, readability or maintainability of code without intentionally changing its external behaviour. During Stage 8, I replaced a long conditional expression with four descriptive Boolean variables and checked the result using regression tests.

### 7. What is a swallowed exception?

**Response:** A swallowed exception occurs when a program catches an exception but ignores or hides it without properly handling the problem. This can make debugging difficult because the original error is no longer clearly visible.

### 8. What is a code smell?

**Response:** A code smell is a sign that code may be difficult to understand, maintain or modify, even if it currently works. Examples include duplicated logic, overly long methods and complex conditional expressions. Our refactoring addressed the readability of a long scheduling condition.

### 9. How should GitHub Copilot-generated debugging diagnoses be treated?

**Response:** Copilot-generated diagnoses should be treated as hypotheses rather than confirmed facts. Engineers should compare them with source code, requirements, test results and other evidence. During Stage 8, we evaluated three ranked suggestions for each defect before accepting or rejecting them.

### 10. What is the Stage 8 engineering rule?

**Response:** Investigate and reproduce the failure before changing code, identify the root cause using evidence, apply the smallest justified repair and verify the result through regression testing. Refactoring should be separate from repairs, supported by passing tests and reviewed by another team member.

---

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved during the recorded debugging work.
- [x] Passing Stage 7 SHA and complete safe preparation details recorded and verified.
- [x] Both defects reproduced through meaningful failing tests.
- [x] Both initial hypotheses have independently verifiable evidence of being recorded before Copilot consultation.
- [x] Three Copilot suggestions evaluated for each defect, with supporting and contradicting evidence documented.
- [x] Supported root causes and minimal repairs explained; focused and full regression results recorded.
- [x] New or strengthened focused tests in `project/tests/test_regressions.py` verified against the handout requirement.
- [x] One genuine refactor verified with passing full-suite results before and after.
- [x] Focused regression test after refactoring independently confirmed and recorded.
- [x] Human PR review, merge and integrated retesting reported.
- [x] Separate GitHub issue references for the two defects and refactoring recorded, if created.
- [x] Tutorial activities, three reflections and ten formative responses completed in the record.
- [x] Original local recovery metadata and preparation materials independently confirmed excluded from the final submission.
- [x] Final documentation merged, submitted SHA recorded and Stage 9 handover fully verified.

### Verified integrated code SHA / result

PR #9 was merged into `main`, with recorded merge commit `114c99e`. The post-merge full test suite returned 57 passed, 0 failed, in 0.7 seconds. Cassandra also reported 57 passing tests after independently pulling and testing the updated project.

The exact final integrated `main` HEAD should be verified from Git before submission.

### Submitted SHA and evidence-only difference if any

**Repair commit:** `2b641de`.

**Refactoring commit:** `0b51342`.

**Recorded integration merge commit:** `114c99e`.

**Later documentation commit:** `2ed4595` — `Complete Stage 8 documentation and evidence`.

The documentation update was made separately from the functional repairs. Its branch was pushed to GitHub, but the final documentation merge and submitted SHA still require verification.

### Unresolved issues or incomplete checks / owner / next action

**Owner:** Reema Aboset, with Cassandra and teaching staff assistance where required.

The original preparation utility's SHA256, actual `--check`, `--apply` and `--verify` outputs, and recovery-folder evidence have not been recovered. The handout identifies `prepare_debugging.py` version 1.1 as the controlled utility, but this does not establish the original execution results.

The saved Copilot conversation references, original human-hypothesis sequence evidence, additional regression-test file, focused after-refactor test, and GitHub issue references should also be checked. The final documentation pull request and submitted SHA must be confirmed.

### Handover note

Stage 8 continued the existing SmartCare project after Stage 7 integration. F8-01 addressed practitioner scheduling conflict detection by correcting the practitioner comparison. F8-02 restored cancelled appointment history lookup by removing an incorrect status restriction.

Both defects were reproduced through failing tests and corrected using minimal changes. The complete test suite passed with 55 tests before and after the separate readability refactor. PR #9 was merged following Cassandra's positive review, and post-merge testing returned 57 passed, 0 failed. Cassandra independently reported the same passing test count.

The same SmartCare repository, source code, accumulated tests and Stage 8 evidence record will be handed over for Stage 9 after the outstanding evidence checks and final documentation integration have been completed.
