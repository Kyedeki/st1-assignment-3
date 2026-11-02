# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | [response] | [response] | [response] |
| FR-05 Prevent practitioner conflict | [response] | [response] | [response] |
| FR-06 Cancel appointment | [response] | [response] | [response] |
| FR-07 Retain cancelled history | [response] | [response] | [response] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert appointment is not None`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert len(results) > 0`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: [response]

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [response] | [response] |
| 2 | [response] | [response] |
| 3 | [response] | [response] |
| 4 | [response] | [response] |
| 5 | [response] | [response] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[response]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour                                                                                                   | Test file/function                                       | Result                                                                                                                                                                        |
|---------|-------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1       | The patient construction accepts the valid values, it trims the surrounding whitespace                      | test_patient_valid_fields_are_trimmed                    | there are problems with the implementation and validation, but after fixing the problem the test result passed                                                                |
| 2       | The patient validation should reject any blank or invalid fields                                            | test_patient_rejects_invalid_required_test               | Passed                                                                                                                                                                        |
| 3       | The practitioner construction should accepd the valid values and should trim surrounding whitespace         | test_paractitioner_valid_fields_are_trimmed              | there are problems with the implementation and validation, but after fixing the problem the test result passed                                                                |
| 4       | The practitioner validation rejects any blank or invalid fields                                             | test_practitioner_rejects_invalid_required_test          | Passed                                                                                                                                                                        |
| 5       | The appointment construction still has the ID, participant objects, date/time and initial schedule status   | test_appointment_starts_scheduled_and_keeps_participants | there are problems with the implementation, the initial result of the test that it failed but after fixing the issue the test passed                                          |
| 6       | The appointment rejects the invalid participants objects                                                    | test_appointment_rejects_invalid_participant_objects     | Passed                                                                                                                                                                        |
| 7       | Appointment  rejects invalid values for date and time                                                       | test_appointment_rejects_invalid_status                  | Passed                                                                                                                                                                        |
| 8       | Appointment rejects an invalid status                                                                       | test_patient_valid_fields_are_trimmed                    | Passed                                                                                                                                                                        |
| 9       | Scheduled appointment can be cancelled, and a repeated cancellation is rejected without changing the status | test_scheduled_appointment_can_be_cancelled_again        | Initial erros have been encountered and it cancellation tests had been corrected and the final result of the test that it passed                                              |
| 10      | Completed appointment cannot be cancelled, and the status is still completed                                | test_completed_appointment_cannot_be_cancelled           | There are probles with the invalid transitions and state preservation and the initial result of it that it failed the testin, however after fixing the errors the test passed |


## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour                                                                           | Requirement / criterion                                    | Test file/function                                          | Result |
|---------|-------------------------------------------------------------------------------------|------------------------------------------------------------|-------------------------------------------------------------|--------|
| 1       | Find an existing patient and return the registered patient                          | FR-02- Patient Search                                      | test_find_patient                                           | pass   |
| 2       | Reject an unkniwn patient ID                                                        | FR-02- Patient Search                                      | test_find_unknown_patient                                   | pass   |
| 3       | Find an existing practitioner and return                                            | FR-03- Supporting practitioner lookup contract under       | test_find_practitioner                                      | pass   |
| 4       | Rejecting unknown practitioner ID                                                   | FR-03- Supporting practitioner lookup contract under       | test_find_unknown practitioner                              | pass   |
| 5       | Cancel a schedule appointment and retain it in the data store                       | FR-06- Cancel Appointment, FR-07- Retain Cancelled History | test_cancel_appointment                                     | pass   |
| 6       | Reject repeated cancallation without changing the cancelled status                  | FR-06- Cancel Appointment                                  | test_cancel_appointment_twice                               | pass   |
| 7       | Reject cancellation of a complete appointment without changing the status           | FR-06- Cancel Appointment                                  | test_cancel_completed_appointment                           | pass   |
| 8       | Reject cancellation of an unknown appointment while preservin existing appointments | FR-06- Cancel Appoitnment                                  | test_cancel_unknown_appointment_preserves_other_appointment | pass   |


## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour           | Boundary/invalid input                 | Expected result                                                        | Test ID |
|---------------------|----------------------------------------|------------------------------------------------------------------------|---------|
| Find Patient        | Blank patient ID                       | no patient search is performed                                         | 1       |
| Find Patient        | Unknown patient ID                     | raises look up error                                                   | 2       |
| Find Patient        | Non-string patient ID                  | raises value error                                                     | 3       |
| Find Practitioner   | Blank patient ID                       | no practitioner search is performed                                    | 4       |
| Find Practitioner   | Unknown patient ID                     | raises look up error                                                   | 5       |
| Find Practitioner   | Non-string patient ID                  | raises value error                                                     | 6       |
| Find Appointment    | Unknown appointment ID                 | raises look up error                                                   | 7       |
| Cancel Appointment  | Non-string appointment ID              | raises look up error                                                   | 8       |
| Cancel Appointment  | Unknown appointment ID                 | raises look up error                                                   | 9       |
| Cancel Appointment  | Cancelled appointment                  | raises value error and the status remains cancelled                    | 10      |
| Cancel Appointment  | Appointment ID with surrounding spaces | trim the ID and cancel the appointment                                 | 11      |
| Cancel Appointment  | Completed Appointment                  | Raises value error but status remains completed                        | 12      |
| Cancel Appointment  | Repeated cancellation                  | rejects the second cancellation and preserbe the original cancellation | 13      |
| Cancel Appointment  | Blanke appointment ID                  | raises value error                                                     | 14      |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
