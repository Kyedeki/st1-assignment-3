# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 2 | Mon 2:30
- Members, GitHub usernames and cohorts: 
  - Cassandra Navarro | Username: Kyedeki
  - Reema Majed M | Username: reema-aboset
- Repository URL: (https://github.com/Kyedeki/st1-assignment-3)
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Patient Search by ID
- Context: SmartCare needs to retrieve existing patients using patient IDs
- Requirement: System should allow patient to be found by using the IDs
- Acceptance criteria: 
  - A valid and existing patient ID
  - Patient IDs are case sensitive 
  - Blank and non-string IDs raise "ValueError"
  - Leading and trailing whitespace is removed from the ID
- Scope: Implementing PatientService.find_patient and add unit tests for a succesful lookup, invalid IDs, unknown IDs, and case sensitivity  
- Definition of Done: The criteria is met, tests are passed and feedback from other team members
- Owner: Cassandra Navarro | Kyedeki 
- Actual issue link: https://github.com/Kyedeki/st1-assignment-3/issues/1 

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implementing Appointment Cancellation and Retained History
- Context: SmartCare needs to cancel schedule appointments while preserving appointment records for history and tracking
- Requirement: Implementing AppointmentService.cancel_appointment so that it cancels an eligible appointment without deleting it from the data store
- Acceptance criteria:
  - cancel a scheduled appointment change and change the status to cancelled 
  - the appointment remains in the data store after cancellation 
  - blank or non-string appointment ID raise ValueError 
  - A valid but unknown appointment ID raises LookupError 
  - cancelling an appointment that is already canceled raises ValueError
a rejected cancellation will not change a appointments existing status
- Scope: implement appointment cancellation in the service layer and have relevant tests, do not make unrelated changes
- Definition of Done: 
  - criteria is met 
  - met the relevant test 
  - got feedback from other groupmates and any changes have been done
- Owner: Cassandra Navarro | Kyedeki
- Actual issue link: https://github.com/Kyedeki/st1-assignment-3/issues/2

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                         |
|---|---------------|------------------------------------------------------------------------------------------------|
| changes | Weak          | The comments is too general so the groupmates shoould inspect the code to understand the change |
| final version | Weak          | Does not explain what was added or fixed                                                       |
| Add patient search by ID | Strong        | The developer added a feature and it clearly identifies the feature that was added             |
| fix stuff | Weak          | The message does not tell what was fixed                                                       |
| Prevent cancellation of completed appointments | Strong        | It describes a specific behaviour and shows the the change                                     |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: 
  - Unrelated changes with appointment cancellation has been included in the pull request. The PR makes it harder to review and has increased risk of defects in the functionality 
- Responsibility and architecture concerns: 
  - renaming the unrelated patient fields and constructing the unrelated code can affect on other parts of SmartCare. The changes should be justified by the requirements than just combining with the appointment cancellaton
- Testing and review concerns:
  - the reviewer should check functionality that includes the cancellation as well as the unrelated patient-field changes, restructing the code and the new dependency. Additional tests can be done to double confirm about the functionality if it still works. 
- Changes to remove or separate, with reasons: 
  -  separating the patient-field renaming another PR linked to its own requirement
  - separate the unrelated code and it should be reviewed first and should be tested
  - remove the unncessary dependency. If the new dependency is required it should be documented like its purpose and should be assessed in terms of security and maintenance implications 
  - The cancellation should be PR focused on cancelling eligble appointments, and it should retain the appointment history and a test should be done to test the behaviur

## D Challenge a weak Copilot review


GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The response does not identify which requirements were checked, which tests were executed, whether the assertions verify the expected behaviour, or whether the changes follow the existing SmartCare architecture. Passing tests alone does not prove the implementation is correct.

- Follow-up review question 1: Does PatientService.find_patient return the correct registered patient when a valid existing ID is provided?

- Follow-up review question 2: How does the implementation handle blank, non-string, case-sensitive and unknown patient identifiers?

- Follow-up review question 3: Does AppointmentService.cancel_appointment change an eligible appointment's status to CANCELLED while retaining its record in the data store?

- Follow-up review question 4: Are invalid or repeated cancellation attempts rejected using the exceptions specified in the service contract without changing existing appointment state?

- Follow-up review question 5: Are the changes limited to the relevant service methods and tests, without unrelated refactoring, new dependencies or weakened test assertions?

- Additional questions if useful: Which specific assertions prove each acceptance criterion? Were the full supplied and newly added tests run? Are practitioner lookup and other previously working behaviours preserved?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use descriptive feature branches, such as feature/patient-lookup and feature/appointment-cancellation. |
| Commit message convention | Write short, meaningful messages describing the actual change, such as "Add patient lookup validation tests". |
| PR size | Each pull request should address one focused requirement or closely related behaviour. Unrelated changes must be separated. |
| Another-member review requirement | Cassandra and Reema will review each other's actual code changes and test assertions before approving a pull request. |
| Merge rule | Merge only after the linked acceptance criteria are met, tests have been run, human review is completed, feedback is resolved and the reviewer has approved. |
| Significant Copilot disclosure rule | Record significant Copilot assistance, including its purpose, suggestions, human evaluation and decisions. Copilot does not replace human review. |

Note: This is the proposed team agreement and must be confirmed by both members.

## F Issue and backlog index

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/Kyedeki/st1-assignment-3/issues/1 | FR-02 Patient Search | Cassandra Navarro (Kyedeki) | Existing patient lookup, case-sensitive IDs, input validation and whitespace handling; see Issue #1. | [TO VERIFY ON GITHUB] |
| https://github.com/Kyedeki/st1-assignment-3/issues/2 | FR-06 Cancellation / FR-07 Retained History | Cassandra Navarro (Kyedeki) | Cancellation changes status, retains history, rejects invalid or unknown IDs and repeated cancellation; see Issue #2. | [TO VERIFY ON GITHUB] |
| [TO ADD ISSUE LINK OR TUTOR-AGREED CRITERION] | Practitioner lookup service target | [AGREE OWNER] | Exact supporting service contract and acceptance criteria from the Stage 6 handout. | [TO COMPLETE] |

## G Pull request evidence

### Pull Request #3 — Stage 6 Documentation

- **PR link and title:** https://github.com/Kyedeki/st1-assignment-3/pull/3 — Complete Stage 6 written activities and test evidence
- **Linked requirement:** Stage 6 documentation and verification evidence.
- **Feature branch:** docs/reema-stage6-record
- **Author:** Reema Majed M (reema-aboset)
- **Changed behaviour:** Documentation changes only; no SmartCare application behaviour changed.
- **Meaningful commits:**
  - 26f60d5 — Complete Stage 6 written activities and test evidence
  - ec057c4 — Update Reema Stage 6 contribution evidence
- **Test command:** py -m pytest
- **Working directory:** project/
- **Observed result:** 24 passed in 0.06 seconds, 0 failures.
- **Test environment:** Python 3.14.5, pytest 8.3.5.
- **Another-member reviewer:** Cassandra Navarro (Kyedeki) — review requested, pending.
- **Human observations before Copilot:** Pending Cassandra's actual review.
- **Requirement and scope checks:** Documentation-only PR; written answers, issue references, contribution evidence and remaining placeholders require review.
- **Key feedback:** Pending.
- **Author response and verification:** Pending reviewer feedback.
- **Reviewer recheck and approval:** Pending.
- **Merge outcome and SHA:** Not yet merged.
- **Significant Copilot assistance:** Record actual GitHub Copilot use and human verification when completed.
- **Linked issue closure:** Not applicable to this documentation-only PR unless a dedicated documentation issue is linked.
- **Each member updated main:** Pending merge.
- **Integrated verification after merge:** Pending.

### Cassandra Navarro — Kyedeki

- **Implementation:** Prepared the implementation scope and functional requirements for Patient Search (FR-02), Appointment Cancellation (FR-06) and Retained History (FR-07).
- **Testing:** Defined expected validation behaviour and testing requirements for patient lookup, appointment cancellation, invalid identifiers and retained appointment history.
- **Review:** Analysed an over-scoped pull request in Section C, identifying unrelated modifications, architectural concerns and testing risks. Requested reviewer for documentation PR #3; approval remains pending.
- **Issue refinement:** Prepared GitHub Issues #1 and #2 with requirement descriptions, acceptance criteria, scope and Definition of Done.
- **Design and responsibility discussion:** Documented the expected service behaviour, including input validation, exception handling and retention of cancelled appointments.
- **Debugging or integration:** No individual debugging or integration activity recorded yet.
- **Documentation or team support:** Completed Sections A–C of the Stage 6 activities and evidence record.

**Evidence:**
- https://github.com/Kyedeki/st1-assignment-3/issues/1
- https://github.com/Kyedeki/st1-assignment-3/issues/2
- https://github.com/Kyedeki/st1-assignment-3/pull/3 

### Pull request 1 — Patient Search

- PR link and title: [TO COMPLETE]
- Linked issue and requirement: Issue #1 — FR-02 Patient Search
- Feature branch: [ACTUAL BRANCH]
- Changed behaviour: [DESCRIBE VERIFIED CODE CHANGES]
- Meaningful commits: [ACTUAL COMMIT LINKS]
- Test command, directory and observed result: [ACTUAL RESULTS]
- Another-member reviewer: [ACTUAL REVIEWER]
- Human observations recorded before Copilot: [ACTUAL REVIEW LINK AND TIME]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [ACTUAL FINDINGS]
- Key feedback: [ACTUAL FEEDBACK]
- Author response/change and verification: [ACTUAL CHANGES AND RESULTS]
- Reviewer recheck and approval: [ACTUAL REVIEW LINK]
- Merge outcome and SHA: [ACTUAL MERGE DETAILS]
- Significant Copilot assistance: [ACTUAL USE OR NONE]
- Linked issue closure: [VERIFY]
- Each member updated main: [ACTUAL CONFIRMATIONS]
- Integrated verification after merge: [COMMAND, WORKING DIRECTORY, RESULT AND SHA]

### Pull request 2 — Appointment Cancellation

- PR link and title: [TO COMPLETE]
- Linked issue and requirement: Issue #2 — FR-06 / FR-07
- Feature branch: [ACTUAL BRANCH]
- Changed behaviour: [DESCRIBE VERIFIED CODE CHANGES]
- Meaningful commits: [ACTUAL COMMIT LINKS]
- Test command, directory and observed result: [ACTUAL RESULTS]
- Another-member reviewer: [ACTUAL REVIEWER]
- Human observations recorded before Copilot: [ACTUAL REVIEW LINK AND TIME]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [ACTUAL FINDINGS]
- Key feedback: [ACTUAL FEEDBACK]
- Author response/change and verification: [ACTUAL CHANGES AND RESULTS]
- Reviewer recheck and approval: [ACTUAL REVIEW LINK]
- Merge outcome and SHA: [ACTUAL MERGE DETAILS]
- Significant Copilot assistance: [ACTUAL USE OR NONE]
- Linked issue closure: [VERIFY]
- Each member updated main: [ACTUAL CONFIRMATIONS]
- Integrated verification after merge: [COMMAND, WORKING DIRECTORY, RESULT AND SHA]

## H Copilot collaboration record

- Member and task: [ACTUAL MEMBER AND TASK]
- Prompt/purpose and relevant issue/diff: [ACTUAL PROMPT OR LINK]
- Summary of output: [ACTUAL COPILOT SUGGESTIONS]
- Human check against actual code, requirements and tests: [VERIFIED OBSERVATIONS]
- Decision — Accept / Modify / Reject: [ACTUAL DECISION]
- Reason: [EVIDENCE-BASED REASON]
- Verification/evidence: [ACTUAL LINK AND RESULT]

Repeat for each significant interaction.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [ACTUAL HUMAN-FIRST OBSERVATIONS]
- Copilot noticed: [ACTUAL COPILOT OBSERVATIONS]
- Overlap: [FINDINGS BOTH IDENTIFIED]
- What did the human reviewer notice that Copilot did not: [ACTUAL DIFFERENCE]
- What did Copilot identify that the human reviewer initially missed: [ACTUAL DIFFERENCE]
- Unsupported or incorrect Copilot suggestion: [ACTUAL EXAMPLE OR EXPLAIN NONE IDENTIFIED]
- Human judgement accepted, modified or rejected, and why: [ACTUAL DECISION AND REASON]
- Which evidence justified merge approval: [TEST RESULTS, REVIEW AND REQUIREMENT TRACE]

## J Contributions

### Cassandra Navarro — Kyedeki

- **Implementation:** Prepared the implementation scope and functional requirements for Patient Search (FR-02), Appointment Cancellation (FR-06) and Retained History (FR-07).
- **Testing:** Defined expected validation behaviour and testing requirements for patient lookup, appointment cancellation, invalid identifiers and retained appointment history.
- **Review:** Analysed an over-scoped pull request in Section C, identifying unrelated modifications, architectural concerns and testing risks. Requested reviewer for documentation PR #3; approval remains pending.
- **Issue refinement:** Prepared GitHub Issues #1 and #2 with requirement descriptions, acceptance criteria, scope and Definition of Done.
- **Design and responsibility discussion:** Documented the expected service behaviour, including input validation, exception handling and retention of cancelled appointments.
- **Debugging or integration:** No individual debugging or integration activity recorded yet.
- **Documentation or team support:** Completed Sections A–C of the Stage 6 activities and evidence record.

**Evidence:**
- https://github.com/Kyedeki/st1-assignment-3/issues/1
- https://github.com/Kyedeki/st1-assignment-3/issues/2
- https://github.com/Kyedeki/st1-assignment-3/pull/3 

### Reema Majed M — reema-aboset

- **Implementation:** No Python service implementation claimed. Contributed to the Stage 6 documentation and verification activities.
- **Testing:** Ran the SmartCare test suite using `py -m pytest` from `project/`. All 24 tests passed with 0 failures using Python 3.14.5 and pytest 8.3.5.
- **Review:** Created documentation Pull Request #3 and requested Cassandra as reviewer. Awaiting her review.
- **Issue refinement:** Updated the issue and backlog index using GitHub Issues #1 and #2 and identified outstanding practitioner-lookup evidence.
- **Design and responsibility discussion:** Drafted the two-person GitHub workflow agreement for confirmation with Cassandra.
- **Debugging or integration:** Resolved the local Python command issue by using the Python launcher and installed the required pytest dependency. Successfully ran the existing tests.
- **Documentation or team support:** Completed Sections D–F and K–L, prepared evidence fields and created a documentation pull request for review.

**Evidence:** https://github.com/Kyedeki/st1-assignment-3/pull/3 

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not automatically represent meaningful contribution because commits vary in size, complexity and importance. One student may make many small formatting changes, while another may resolve a difficult defect, develop meaningful tests or identify a significant design problem during review. Contribution should be evaluated through the quality and relevance of the work, requirement coverage, testing, review feedback, integration and documented decisions rather than the number of commits alone.

## L Stage 6 formative questions

### 1. What is version control?

Version control is a system that records changes to files over time. It allows developers to track modifications, compare versions, restore earlier work and collaborate without losing important changes. Git is the version control system used for SmartCare.

### 2. Why is a feature branch useful?

A feature branch allows a developer to work on a specific change without directly modifying the shared main branch. It separates unfinished work from reviewed code and allows changes to be tested and reviewed before integration.

### 3. What makes a commit a good engineering commit?

A good engineering commit contains a focused and meaningful change, has a clear description, and avoids unrelated modifications. It should be understandable to another developer and should preserve a useful history of the project's development.

### 4. What is a pull request?

A pull request is a request to integrate changes from one Git branch into another. It provides a space for teammates to inspect the differences, discuss concerns, review tests and approve changes before merging them into main.

### 5. What is the purpose of code review?

Code review helps identify defects, incorrect assumptions, weak tests and unnecessary modifications before changes become part of the shared application. It also supports knowledge sharing, maintainability and accountability.

### 6. What does a Git diff show?

A Git diff shows the differences between versions of files, including added, removed and modified lines. It helps developers and reviewers understand exactly what changed and identify unexpected modifications.

### 7. What is a Definition of Done?

A Definition of Done is a set of conditions that must be satisfied before a task can be considered complete. For SmartCare, this includes meeting the acceptance criteria, running meaningful tests, completing the required review, resolving important feedback and integrating the approved work.

### 8. What is the appropriate role of GitHub Copilot in pull-request review?

GitHub Copilot should assist reviewers by suggesting possible defects, edge cases, missing tests and improvements. Its suggestions must be checked against the actual requirements, code and test results. Human reviewers remain responsible for deciding which suggestions are valid and whether a change should be approved.

### 9. Why should individual contribution not be judged only by commit count?

Commit count does not measure the difficulty, quality or importance of a person's work. Testing, debugging, reviewing pull requests, discussing requirements and resolving integration problems are also meaningful contributions. Evidence of actual engineering work provides a better assessment than the number of commits.

### 10. What is the Stage 6 engineering rule?

Stage 6 requires changes to be traceable, focused, tested and reviewed before they are integrated. Each significant change should link to a requirement, be implemented on a feature branch, include meaningful verification, receive another member's human review and be merged only after the required checks are satisfied.

## M Completion and handover

- Starting SHA: [ACTUAL STARTING SHA]
- Final Stage 6 code SHA: [ACTUAL TESTED SHA]
- Test command: python -m pytest
- Working directory: project/
- Observed result: [ACTUAL PASS/FAIL COUNTS]
- PR and another-member reviewer: [ACTUAL LINKS AND REVIEWERS]
- Unresolved issue or none: [ACTUAL STATUS]
- Stage 7 handover status: [READY FOR TUTOR CHECKPOINT / UNRESOLVED WORK]
- Final submitted SHA if later than tested SHA: [ACTUAL SHA AND EVIDENCE-ONLY DIFFERENCE]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting. 