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

- Missing evidence: [response]
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

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
