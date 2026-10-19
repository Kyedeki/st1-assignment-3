Stage 6 activities and evidence

Group/tutorial: Group 2 | Monday 2:30
Members: Cassandra Navarro (Kyedeki); Reema Majed M (reema-aboset)
Shared repository: https://github.com/Kyedeki/st1-assignment-3
Starting baseline SHA: f1f35ad (shared SmartCare Assignment 3 starter)
Service implementation SHA: 31486b1
Tested integration SHA: 680e407 (documentation PR #3 merge)
This record distinguishes observed evidence from activities still requiring verification. Passing tests do not establish coverage of every acceptance criterion, and a documentation review is not a substitute for a service-code review.

## A Requirement to issue activities
FR-02 Patient Search
- Title: Patient Search by ID.
- Context: SmartCare must retrieve an existing patient by ID.
- Requirement: Search for an existing patient using the supplied identifier.
- Acceptance criteria proposed in the group record: Existing, matching ID returns the patient; matching is case-sensitive; blank and non-string IDs raise ValueError; leading/trailing whitespace is removed; an unknown valid ID raises LookupError.
- Scope: PatientService.find_patient and focused positive, negative and boundary tests.
- Definition of Done: Requirement-specific tests pass, changes are linked to the issue, reviewed by another member and integrated with evidence.
- Issue owner: Cassandra Navarro (Kyedeki).
- Issue: https://github.com/Kyedeki/st1-assignment-3/issues/1
FR-06 Appointment Cancellation and FR-07 Retained History
- Title: Appointment Cancellation and Retained History.
- Context: SmartCare cancels eligible scheduled appointments without deleting their history.
- Requirement: AppointmentService.cancel_appointment changes an eligible appointment to cancelled and retains the stored record.
- Acceptance criteria proposed in the group record: Scheduled appointment becomes CANCELLED; appointment stays in the data store; blank and non-string IDs raise ValueError; unknown valid IDs raise LookupError; repeated cancellation raises ValueError; rejected attempts leave existing status unchanged.
- Scope: Cancellation service method and relevant tests, without unrelated refactoring.
- Definition of Done: Meaningful tests and acceptance criteria satisfied, another-member review recorded, feedback resolved, change integrated.
- Issue owner: Cassandra Navarro (Kyedeki).
- Issue: https://github.com/Kyedeki/st1-assignment-3/issues/2
Additional service target: Practitioner lookup (PractitionerService.find_practitioner) is present in the inspected code, but an independently linked issue or tutor-agreed criterion has not been verified from supplied records.

## B Commit quality
Original message	Strong or weak?	Reason
changes	Weak	Does not explain what changed.
final version	Weak	Gives no technical scope or purpose.
Add patient search by ID	Strong	Identifies the specific feature.
fix stuff	Weak	Does not identify the defect or fix.
Prevent cancellation of completed appointments	Strong	Identifies the intended change in behaviour.


## C Over-scoped PR review
Scenario: A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a dependency.
- Scope concern: These changes are unrelated to the cancellation requirement, increase review effort and introduce avoidable risk.
- Architecture/responsibility concern: Renaming patient fields or restructuring other services could break existing consumers and should be handled under its own justified task.
- Testing/review concern: Reviewers would need to assess unrelated data-model changes and dependency effects, not just cancellation assertions.
- Recommended action: Keep cancellation and retained-history behaviour in its own focused PR. Split any justified refactoring into separately linked changes; remove an unnecessary dependency or document and review its rationale.

## D Challenge a weak Copilot review
Copilot statement: “Looks good; tests pass.”
Missing evidence: It does not identify actual commands, test results, acceptance criteria, assertions, changed lines, invalid inputs, architectural responsibilities, or whether unrelated changes were introduced. Passing tests alone cannot prove correctness.
1. Does patient lookup return the correct registered patient for an exact existing ID?
2. Does lookup trim surrounding whitespace but preserve case-sensitive matching, rejecting invalid and unknown IDs with the correct exception?
3. Does cancellation change an eligible appointment to CANCELLED while retaining the same stored record?
4. Do repeated or invalid cancellations raise the specified exception without changing the existing appointment state?
5. Are the implementation and tests focused on the relevant service contracts without unrelated changes, weak assertions or dependencies?
Additional question: Which exact assertions support each acceptance criterion, including practitioner lookup?

## E Team workflow agreement
Practice	Proposed agreement
Branch naming	One descriptive task branch, e.g. feature/patient-lookup or docs/reema-stage6-record.
Commit messages	Short, specific and meaningful; avoid changes or final.
PR size	Focus on one requirement or closely related evidence change.
Another-member review	Cassandra and Reema review one another's changes; the author does not approve their own PR.
Merge rule	Merge after human review, relevant tests and feedback resolution; record the result.
Copilot disclosure	Record substantive prompts, findings and human Accept/Modify/Reject decisions. Copilot cannot approve a PR.


Agreement status: Drafted in the group record; explicit agreement by both members is not independently evidenced here.

## F Issue and backlog index

| Issue / Source | Requirement | Owner | Acceptance criteria / Supporting contract | Status |
|---|---|---|---|---|
| [Issue #1](https://github.com/Kyedeki/st1-assignment-3/issues/1) | FR-02 Patient Search | Cassandra Navarro | Retrieve existing patients using valid IDs; validate identifiers and handle unknown patients. | Open |
| [Issue #2](https://github.com/Kyedeki/st1-assignment-3/issues/2) | FR-06 Appointment Cancellation / FR-07 Retained History | Cassandra Navarro | Cancel scheduled appointments, retain history, reject invalid IDs and illegal transitions. | Open |
| Requirements Baseline Revision 2 | FR-03 Practitioner Registration / Supporting Practitioner Lookup | Group — owner to confirm | Practitioner lookup is a supporting operation. Identifiers are trimmed, non-blank and case-sensitive. Invalid identifiers raise ValueError; unknown valid identifiers raise LookupError. | Baseline verified; separate Stage 6 criterion/issue pending confirmation |

### Practitioner Lookup verification

- **Source:** SmartCare A3 Requirements Baseline 2026, Revision 2.
- **Implementation:** `PractitionerService.find_practitioner()`.
- **Test evidence:** Tests cover valid, unknown, blank, whitespace-padded, case-sensitive and non-string identifiers.
- **Result:** 28 tests passed, 0 failed, from `project/`.
- **Traceability:** FR-03 baseline confirmed. A separate Stage 6 criterion or approved issue remains unverified.



## G Pull request evidence
PR #3 — Stage 6 documentation (merged)
- PR link and title: https://github.com/Kyedeki/st1-assignment-3/pull/3 — Complete Stage 6 written activities and test evidence.
- Linked task: Stage 6 activity record and testing/review documentation; not a functional implementation PR.
- Branch and author: docs/reema-stage6-record; Reema Majed M (reema-aboset).
- Changed behaviour: Documentation only; no SmartCare service behaviour changed in this PR.
- Meaningful commits: 26f60d5 (Stage 6 documentation), ec057c4 (Reema contribution evidence), and additional changes recorded in the PR history. See PR commits for authoritative list.
- Original test command, directory and observed result: py -m pytest from project/; 24 passed on integrated main, 0.11 seconds (Python 3.14.5; pytest 8.3.5).
- Another-member reviewer: Cassandra Navarro (Kyedeki).
- Human observations before Copilot: Cassandra commented that the documentation additions were consistent and suitable for merging. This is documentation-review evidence, not independent code-review findings.
- Requirement, responsibility, assertions and scope check: This PR changed only written evidence, so code/test-diff review was not part of its changes.
- Key feedback: Cassandra's recorded comment recommended merging the changes; no specific corrections were requested in that comment.
- Author response and verification: Documentation PR merged. Local main was fast-forward updated and pytest passed.
- Reviewer recheck / formal review state: GitHub review state was COMMENTED, not formal APPROVED (per Copilot's retrieved PR review data).
- Merge outcome/SHA: Merged at 680e407.
- Significant Copilot assistance: A later, real Copilot review was performed; see H and I.
- Issue closure: Not automatically linked to a requirement issue; Issues #1/#2 were still open when Copilot checked.
- Each member updated main: Reema confirmed update of local main at 680e407; Cassandra's local update not verified.
- Integrated verification: 24 passed on the original integrated snapshot, from project/.
Original service implementation — actual history (not a separate PR)
- Relevant requirements: FR-02, Practitioner Lookup, FR-06 and FR-07.
- Implementation commit: 31486b1 — Implement SmartCare service methods and tests.
- Changed behaviour: Patient and practitioner lookup and appointment cancellation, with associated tests and supporting document changes.
- Branch/PR: Copilot's GitHub check did not find an implementation PR for this commit; the implementation was committed to the shared history prior to PR #3.
- Test evidence: Earlier 24-test suite passed. See later remediation test changes below.
- Human observations before Copilot / reviewer approval: PENDING: no independently documented human review of the implementation diff was available.
- Author response / reviewer recheck / merge SHA: No distinct implementation PR review/merge chain was located; do not fabricate one.
- Issue closure: Issues #1 and #2 still open at Copilot's last check; update only after confirming criteria.
- Remediation: Request a documented review of the actual service diff and ask tutor whether retroactive review suffices, since the original code bypassed the agreed PR process.
Final test and documentation corrections — awaiting PR
- Branch: feature/stage6-final-fixes.
- Current commit: 68521ac — Fix Stage 6 tests and complete review documentation.
- Changes: Fixed practitioner non-string lookup test; added tests for cancellation with unknown, non-string and whitespace-padded appointment IDs and repeated cancellation with retained history; revised Stage 6 evidence.
- Requirements linked: Practitioner Lookup; FR-06 cancellation; FR-07 retained history. FR-02 existing tests retained.
- Test command / directory: py -m pytest from project/.
- Actual most recent observed result: 28 passed, 0 failed (user-confirmed after corrections; exact duration not recorded).
- Reviewer, human-first observations and review link: PENDING: request Cassandra to review the actual test diff and documentation. Human-first review must describe real observations, not copy Copilot's suggestions as if independently discovered.
- Review changes, recheck, merge outcome and tested integration SHA: PENDING. Branch was pushed to GitHub but no PR/approval/merge is confirmed.
- Linked issue closure / both members pull/check: PENDING.

## H Copilot collaboration record
- Member and task: Reema Majed M — inspect Stage 6 SmartCare implementation, tests, requirements and evidence record.
- Actual prompt/purpose: Asked Copilot Chat inside the VS Code SmartCare workspace for a single evidence-grounded technical report. Scope: review project/smartcare/ services, project/tests/, commits 31486b1 and 680e407, PR #3, and the Stage 6 record; report defects, missing tests, requirement traceability and review provenance. The first browser-based attempt could not access the files; the subsequent workspace review succeeded.
- Relevant requirements/diff: FR-02 Patient Search, Practitioner Lookup, FR-06 cancellation, FR-07 retained history; actual implementation commit 31486b1; documentation PR #3.
- Copilot output, important finding 1: test_find_practitioner_with_non_string_id was named for practitioner lookup but called PatientService.find_patient() instead. This did not test the intended practitioner input guard (project/tests/test_services.py, around original line 163).
- Copilot output, important finding 2: Cancellation had no explicit tests for unknown and non-string IDs or whitespace-padded valid IDs. Repeated cancellation lacked an assertion that the cancelled appointment remained stored and unchanged.
- Copilot output, important finding 3: Stage 6 documentation described some review/comparison tasks as completed without matching evidence. PR #3 was a documentation review only and did not establish review of the implementation diff.
- Copilot output, important finding 4: Practitioner Lookup lacked a recorded issue or tutor-approved acceptance-criterion reference; Issues #1/#2 remained open at the time of review.
- Copilot positive finding: No critical defects were found in the three reviewed service implementations. Cancellation delegates legal state transitions to the domain model and retains the record.
- Copilot test execution: py -m pytest from project/ → 24 passed in 0.08 seconds, on its reviewed snapshot. An earlier run from repository root failed during import collection due to wrong working directory; do not conflate that with a functional test failure.
- Human check against actual code, requirements and tests: Reema used the existing working test setup and verified SmartCareDataStore.find_appointment() as the correct retained-history lookup. An earlier drafted test incorrectly used get_appointment()/appointments; these were corrected and re-tested. The final four additional test cases were run successfully, bringing the suite to 28 passed.
- Decision — Accept/Modify/Reject: Actual actions support ACCEPT/MODIFY for the incorrect practitioner test and focused cancellation-test improvements: Reema corrected the test and added coverage, with passing verification. PENDING: a separately recorded group decision on documentation and practitioner traceability; a human code reviewer still must inspect the diff.
- Reason: Focused tests improve checks of the existing service contract without changing production architecture or introducing unrelated features.
- Verification/evidence: Copilot review output preserved in the conversation; code/test changes committed as 68521ac; user-confirmed 28 passing tests. A PR review and integration SHA for these changes are not yet evidenced.

## I Human versus Copilot review comparison
- Human reviewer noticed before consulting Copilot: Cassandra reviewed PR #3's documentation and said the changes appeared consistent and could be merged. The current evidence does not contain a pre-Copilot independent human inspection of the service-code diff.
- Copilot noticed: Wrong service called by practitioner non-string test; missing cancellation negative/boundary tests and retained-state assertions; incomplete traceability and mismatched completion claims; PR #3 did not review the original Python implementation.
- Overlap: Both assessed the Stage 6 documentation in some form. There is no verified code-review overlap to report.
- What the human reviewer noticed that Copilot did not: Cassandra explicitly judged the documentation PR suitable to merge. No uniquely human, code-specific pre-Copilot finding is evidenced.
- What Copilot identified that the human reviewer initially missed: Its report contains technical testing/traceability gaps absent from Cassandra's documentation comment. Whether Cassandra had independently found them elsewhere is unknown.
- Unsupported or incorrect Copilot suggestion: Copilot did not substantiate a required production-code refactor. Its optional style/cleanup suggestions were not adopted because the review found no functional implementation defect requiring them. Separately, preliminary assistant-authored test examples used invalid appointment construction and nonexistent lookup methods; those were corrected by using the project's passing examples. Do not misattribute those example errors to Copilot.
-
### Human evaluation of Copilot recommendations

| Decision | Copilot recommendation | Human evaluation and evidence |
|---|---|---|
| Accept | Correct the practitioner non-string-ID test. | The original test called PatientService instead of PractitionerService. It was corrected to test PractitionerService.find_practitioner(). |
| Accept | Add tests for cancellation using unknown and non-string IDs. | Both tests were added and passed. |
| Accept | Test whitespace handling and retained history after repeated cancellation. | Additional tests were added with assertions checking appointment status and the retained stored object. |
| Modify | Improve Practitioner Lookup requirement traceability. | The official Requirements Baseline Revision 2 identifies Practitioner Lookup as a supporting operation under FR-03. |
| Reject | Perform unrelated implementation refactoring. | No critical implementation defect requiring such refactoring was identified. Focused test corrections were preferred. |

**Verification:** Reema ran `py -m pytest` from `project/` after the test corrections. All 28 tests passed.

**Review status:** These decisions reflect Reema's implemented corrections and evaluation of Copilot's findings. Cassandra's independent code review and final approval are still pending.


## J Contributions
Cassandra Navarro — Kyedeki
- Implementation: Prepared requirement scope and acceptance criteria for FR-02 Patient Search and FR-06/FR-07 Cancellation/History. The implementation commit is recorded above; exact personal Python authorship should be attributed only from actual commit/history evidence.
- Testing: Specified expected positive/negative lookup, invalid identifier, cancellation and retention behaviour in requirement work.
- Review: Commented on PR #3 that Reema's Stage 6 documentation changes were consistent and could merge. PENDING: review of final test-fix PR and original implementation diff.
- Issue refinement: Prepared Issue #1 and Issue #2, including acceptance criteria and scope.
- Design and responsibility discussion: Described validation, exception behaviours and retention requirements in issues and Sections A–C.
- Debugging/integration: No separate individual debugging result independently recorded.
- Documentation/team support: Drafted original Stage 6 Sections A–C; participated in documentation review.
- Evidence: Issues #1/#2 and PR #3 linked above.
Reema Majed M — reema-aboset
- Implementation: Documentation, focused test corrections and verification; no original production service implementation personally claimed.
- Testing: Ran original 24-test suite, corrected wrong practitioner non-string test, added four cancellation test cases and confirmed 28 passed, 0 failed, from project/.
- Review: Created documentation PR #3, requested Cassandra review, obtained Copilot's workspace-based technical report and used its findings to guide focused test corrections.
- Issue refinement: Maintained issue/backlog record and identified missing Practitioner Lookup requirement trace.
- Design and responsibility discussion: Drafted proposed two-member Git/PR/review workflow.
- Debugging/integration: Resolved local Python launcher/pytest setup, corrected invalid test fixtures to use real service registration and booking, fixed stored-history assertions using data_store.find_appointment, updated local main after PR #3 and pushed branch feature/stage6-final-fixes.
- Documentation/team support: Completed Sections D–F and K–L, drafted H/I based on real Copilot review and updated final evidence.
- Evidence: PR #3, implementation review record, commit 68521ac.

## K Exit question
Why is a high commit count not necessarily evidence of strong contribution?
A large commit count does not necessarily represent meaningful work because commits vary in complexity and importance. One student may make numerous formatting changes while another designs thorough tests, diagnoses a significant defect, reviews risky code or resolves integration failures. Assess contribution through requirement coverage, code/test quality, review feedback, debugging, integration and traceable decisions, not commit totals alone.

## L Stage 6 formative questions
1. What is version control? Git tracks file revisions so developers can compare changes, restore earlier states and coordinate work across a team.
2. Why is a feature branch useful? It isolates a focused change from the shared main and supports testing and review before merging.
3. What makes a commit a good engineering commit? It has a focused, understandable diff and a specific message explaining the change.
4. What is a pull request? It proposes integrating one branch into another and gives the team a place to inspect changes, discuss requirements, review checks and approve them.
5. What is the purpose of code review? To detect errors, missing cases, weak assertions, architecture concerns and unnecessary modifications while sharing understanding of the code.
6. What does a Git diff show? Added, deleted and modified lines between two versions or commits.
7. What is a Definition of Done? The agreed conditions for considering a task complete, including criteria, tests, required review and integration evidence.
8. What is the appropriate role of GitHub Copilot in pull-request review? It suggests possible issues and test improvements, which a human must validate against the actual code, requirements and assertions. Copilot does not replace human approval.
9. Why should individual contribution not be judged only by commit count? Valuable work also includes design, testing, debugging, human review, requirement clarification and integration; commit number alone cannot measure impact.
10. What is the Stage 6 engineering rule? Make requirement-linked, focused changes; test them; independently review the actual diff before merge; record Copilot's assistance accurately; integrate and verify the shared checkpoint.

## M Completion and handover
- Starting SHA: f1f35ad — shared SmartCare starter.
- Original implementation SHA: 31486b1 — SmartCare service methods and tests.
- Original integrated documentation SHA: 680e407 — PR #3 merge into main.
- Current final-fixes branch commit: 68521ac — feature/stage6-final-fixes, pushed to GitHub, not yet verified as merged.
- Original test verification: 24 passed from project/ (post PR #3), Python 3.14.5 / pytest 8.3.5.
- Latest observed test verification: 28 passed, 0 failed, from project/ after correction; duration not captured in final user confirmation.
- Test command: py -m pytest run inside project/.
- Documentation PR and reviewer: PR #3 — Cassandra commented positively (GitHub state COMMENTED); merged at 680e407.
- Copilot collaboration: A real workspace-based technical review completed; important findings documented in Sections H and I. Earlier failed access attempt was not a substantive review.
- New test/documentation PR: PENDING creation and Cassandra's human review of feature/stage6-final-fixes.
- Original service-code review: PENDING independent recorded review/tutor-approved remediation for direct-to-main original code.
- Practitioner Lookup trace: PENDING exact handout acceptance criterion and issue or tutor-approved trace reference.
- GitHub issues: #1 and #2 were open when Copilot checked; verify resolution and update deliberately.
- Environment support: Verify whether Python 3.14.5 is accepted for the course; reference guide mentions testing with Python 3.13.
- Both members updated/tested merged main: Reema did so for PR #3; Cassandra's subsequent confirmation is PENDING.
- Final integrated submitted SHA: PENDING after the new PR is reviewed, merged and tested; do not present 68521ac as a merge commit.
- Stage 7 handover: Pending review, traceability, final merge and verification evidence.
Completion checklist
- [x] Stage 6 service implementations present and inspected against available service contracts.
- [x] Original tests retained and practitioner/cancellation tests corrected and expanded; 28 passed locally.
- [x] Two requirement-linked GitHub issues documented.
- [x] Copilot actually reviewed the local implementation and tests; findings captured.
- [x] Documentation PR #3 received Cassandra's comment, merged and verified.
- [x] Tutorial activity answers and formative answers drafted.
- [x] Reema committed and pushed focused Stage 6 test/documentation changes (68521ac).
- [ ] Practitioner Lookup independently traceable to full Stage 6 handout criterion / approved issue reference.
- [ ] New test/documentation branch reviewed by Cassandra through an actual PR and merged.
- [ ] Original implementation diff independent human review evidenced or tutor-approved remediation recorded.
- [ ] Final human review judgement and Accept/Modify/Reject decisions confirmed; Section I finalized if necessary.
- [ ] New merged main SHA recorded and entire pytest suite rerun on that SHA.
- [ ] Each member's final update/check and any issue closure statuses verified.
- [ ] Unit's supported Python runtime confirmed if required by assessment instructions.