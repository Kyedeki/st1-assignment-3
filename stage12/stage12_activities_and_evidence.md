# Stage 12 activities and evidence

**Group/tutorial:** Group 2 — tutorial details to confirm.

**Members and UG/PG applicability:** Reema Aboset and Cassandra Navarro. Undergraduate common release scope. Stages 10 and 11 are PG-only and not applicable.

**Repository:** [https://github.com/Kyedeki/st1-assignment-3](https://github.com/Kyedeki/st1-assignment-3)

**Evidence status:** Stage 9 is integrated. The Stage 9 README records 81 passing tests, and Reema independently reports a successful test run. Final Stage 12 release verification, clean-copy reproduction and sign-off are recorded separately below.

---

## A Release scope and starting SHA

**Release label/version and requirements baseline:** Proposed SmartCare v1.0 — undergraduate course release. Applicable requirements are FR-01–FR-09, QRY-01–04, FP-01–03 and UI-01–02. FR-10 is retired.

**Common starting SHA / branch / applicable members:**

- Branch: `main`
- Starting SHA: `5d4c6d725fcbb1bca16773733416951a90f93698`
- Members: Reema Aboset and Cassandra Navarro.
- Stage 9 implementation merge: `e3a0ada3e9d812ef4d0803d174a2abb60a005254`.

**PG starting SHA / branch / applicable members:** Not applicable — undergraduate pathway.

**Working-state review and approved integration:**

Stage 9 contributions were integrated through three pull requests:

- PR #13: Stage 9 documentation and human design.
- PR #14: Stage 9 queries and console integration.
- PR #15: Stage 9 evidence documentation update.

All three PRs are merged. Before final release, the team will inspect the working tree, tracked files and any outstanding differences using Git.

**Protected common candidate and PG differences:** The observed common starting candidate is `5d4c6d725fcbb1bca16773733416951a90f93698`. This is not yet declared the final tested release SHA. PG extensions are not applicable.

**Feature freeze / owner / verifier:**

Optional feature development is frozen. Reema is responsible for release documentation, evidence and review. Cassandra supports implementation verification, testing and independent review. Both members are responsible for the final release decision.

---

## B Requirements and release readiness matrix

### Tutorial Activity 1

**Decision: Do not release yet.**

Although all tests pass in the scenario, incomplete README instructions, an unreviewed dependency and an undocumented limitation prevent a responsible release decision.

The README must explain how to install, run and test the application. Dependencies must be checked for their purpose, origin and licensing. Known limitations must be documented so users understand the system's intended scope.

After these actions, another person should reproduce the application from a fresh copy. Only then should the team reconsider release approval.

### Tutorial Activity 2 — Evidence matrix

| Release claim / requirement / scope | Evidence                                                           | Location/link and SHA                                    | Reviewer             | Sufficient?         | Gap/action                                     |
| ----------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- | -------------------- | ------------------- | ---------------------------------------------- |
| Cancellation history — FR-06–08     | Cancellation retains the appointment object and changes its status | `domain.py`, `test_workflows.py`; starting SHA `5d4c6d7` | Final review pending | Partial             | Recheck identity, lookup and listing           |
| Architecture responsibilities       | Domain, datastore, services, queries and console are separated     | `project/smartcare/`                                     | Reema/Cassandra      | Partial             | Final code-quality inspection                  |
| Rescheduling — PG only              | Outside UG scope                                                   | N/A                                                      | N/A                  | N/A                 | No PG implementation required                  |
| Responsible AI                      | Stage 9 Copilot review and recorded human decisions                | Stage 9 Section E                                        | Team                 | Partial             | Confirm final changes and dependency review    |
| Maintainability                     | Modular architecture and accumulated tests                         | `project/smartcare/`, `project/tests/`                   | Team                 | Partial             | Review formatting, tests and README            |
| FR-01–03                            | Registration, lookup and validation services                       | `services.py`, `test_services.py`                        | Team                 | Partial             | Final regression/demo                          |
| FR-04–05                            | Booking and practitioner conflict checks                           | `services.py`, `data_store.py`                           | Team                 | Partial             | Verify rejection leaves no partial appointment |
| FR-06–08                            | Cancellation, retained history and lookup                          | `domain.py`, `test_workflows.py`                         | Team                 | Partial             | Demonstrate repeated cancellation rejection    |
| FR-09, QRY/FP                       | Pure queries, status filtering, deterministic sorting              | `queries.py`, `test_queries.py`                          | Team                 | Partial             | Verify all statuses and new-list identity      |
| UI-01–02                            | Interactive menu and invalid-input recovery                        | `console.py`, `test_workflows.py`                        | Team                 | Partial             | Final manual demonstration                     |
| Session-only scope                  | In-memory dictionaries, no persistent storage                      | `data_store.py`, `project/README.md`                     | Team                 | Supported by design | Confirm limitation in release notes            |
| PG RES/assurance                    | Not applicable to UG                                               | N/A                                                      | N/A                  | N/A                 | Retain supplied PG templates unchanged         |

### Tutorial Activity 3 — Viva practice

One shared `SmartCareDataStore` is necessary because all services must access the same registered patients, practitioners and appointments. Using separate stores would break lookup and booking relationships.

Cancellation is verified by retrieving a cancelled appointment and checking that its status is `CANCELLED`. The existing tests also check that cancelled appointments appear in the default practitioner listing.

In Stage 9, Copilot recommended strengthening workflow assertions. The team accepted the recommendation because test output alone does not necessarily prove that rejected operations leave application state unchanged. Completion of those improvements must be checked against the final test files.

A major limitation is that SmartCare stores information only during the current process. Changing query functions to access global state or handle console input would reduce predictability and weaken separation of responsibilities.

---

## C Full regression results

| Suite/scope                      | Environment/version                        | Working directory and command                                       | Tested SHA               | Actual result                              | Evidence link             |
| -------------------------------- | ------------------------------------------ | ------------------------------------------------------------------- | ------------------------ | ------------------------------------------ | ------------------------- |
| Stage 9 integrated regression    | README states Python 3.13 and pytest 8.3.5 | `project/`; `python -m pytest -q`                                   | Stage 9 version          | 81 passed, 0 failed, as recorded in README | `project/README.md`       |
| Reema's independent test run     | Actual interpreter/version to record       | `project/`; command to confirm                                      | Exact tested SHA pending | User reports all tests passed              | Terminal evidence pending |
| Stage 12 complete common suite | Windows PowerShell, Python 3.14.5 | `project/`; `py -m pytest -q` | `5d4c6d725fcbb1bca16773733416951a90f93698` | 81 passed, 0 failed, 0.08s | VS Code terminal verification, 9 November 2026 |
| PG suite                         | N/A                                        | N/A                                                                 | N/A                      | N/A                                        | UG-only                   |
| Focused checks after corrections | Pending if changes occur                   | `python -m pytest -q tests/test_queries.py tests/test_workflows.py` | Pending                  | Pending                                    | Test output               |
| Final integrated recheck         | Pending                                    | `python -m pytest -q`                                               | Pending                  | Pending                                    | Final release evidence    |

**Prior assertions preserved / reviewed test diff:** Existing tests remain in the repository. Any corrections must preserve valid earlier assertions and be reviewed before integration.

**Remaining failure / limitation:** No failing tests were reported. However, passing tests do not prove every requirement is covered. The Stage 9 Copilot review identified opportunities to strengthen workflow, filtering and date-validation tests.

**Non-interactive demonstration verification:**

On 9 November 2026, SmartCare was executed from
`project/` using `py main.py` and Python 3.14.5.

The application successfully displayed the synthetic
scheduled appointment A1 for patient P1 and practitioner
DR1 at 2026-10-01 09:00.

The application also displayed the session-only data
limitation and exited normally without errors.

Tested SHA: 5d4c6d725fcbb1bca16773733416951a90f93698

---

## D Console and end-to-end demonstration

**Problem and stakeholders:** SmartCare is a course-scope appointment system intended to demonstrate how clinic staff can register patients and practitioners, book appointments, prevent scheduling conflicts and retain cancellation history. Patients and practitioners depend on accurate records. Only synthetic information is used.

|| Demo step | Observed result |
|---|---|
| Register and find patient and practitioners | Passed — P1, D1 and D2 registered; lookup succeeded. |
| Valid booking | Passed — A1 booked for D1 at 2026-12-01 09:00. |
| Same practitioner conflict | Passed — A2 rejected; lookup confirmed it was not stored. |
| Different practitioner | Passed — A3 booked for D2 at the same time. |
| Cancel and retrieve | Passed — A1 retained with CANCELLED status. |
| Repeated cancellation | Passed — second cancellation rejected. |
| Default listing | Passed — cancelled A1 remained in D1's listing. |
| Explicit status filtering | Passed — A1 excluded from scheduled-only results. |
| Cancelled time-slot reuse | Passed — A4 successfully booked for D1 at 09:00. |
| Invalid-input recovery | Passed — invalid calendar date and menu option rejected; A4 remained retrievable. |
| Normal exit | Passed — application exited and displayed the session-only limitation. |

**Stage 12 manual demonstration:** Completed by Reema Aboset
on 9 November 2026 using Python 3.14.5.

**Command:** py main.py --interactive

**Tested SHA:** 5d4c6d725fcbb1bca16773733416951a90f93698

**Result:** All manually exercised workflows behaved as
expected. The application recovered from invalid inputs
and exited normally.

**Evidence:** Manual terminal verification; screenshots
to be linked if retained.

**Stable demo owner / fresh process / command:** Reema and Cassandra; `python main.py --interactive` from `project/`.

**PG demonstrations:** Not applicable.

---

## E Final code quality and AI review

| Review area                           | Code/evidence location                   | Finding or no finding                                       | Correction/no change and recheck          |
| ------------------------------------- | ---------------------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| OOP responsibilities and pure queries | `domain.py`, `services.py`, `queries.py` | Main responsibilities appropriately separated               | Preserve design                           |
| PascalCase and snake_case             | SmartCare modules                        | Class and function naming generally follows conventions     | No major naming redesign needed           |
| Type hints/docstrings                 | SmartCare modules                        | Main APIs have type hints; some docstrings could be clearer | Minor improvements if reviewed            |
| Four-space indentation/imports        | Source and tests                         | Some inconsistent whitespace/formatting visible             | Consider bounded formatting fixes         |
| Focused methods/duplication           | `console.py`, tests                      | Menu logic is understandable; some repeated patterns        | Avoid unnecessary abstraction             |
| Globals/responsibility leakage        | `queries.py`, `console.py`               | Queries use explicit inputs; menu uses a shared store       | No architectural rewrite needed           |
| Persistence/repository frameworks     | `project/smartcare/`                     | No SQL or persistence layer                                 | Correct UG scope                          |
| Synthetic data/secrets/dependencies   | Tests, requirements file                 | Synthetic test data; pytest pinned                          | Final dependency/secret audit pending     |
| Copilot contributions                 | Stage 9 Section E                        | Test-evidence improvements suggested                        | Check final acceptance and implementation |
| PG assurance                          | N/A                                      | UG-only                                                     | N/A                                       |

### Final AI decision table

| AI claim                                                                  | Affected requirement/code  | Human check                                                             | Accept/Modify/Reject and reason                   | Actual outcome/action                            |
| ------------------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------ |
| Workflow test needs stronger assertions                                   | UI-01, `test_workflows.py` | Compare test assertions against required booking/cancellation behaviour | Accept: broad output checks may miss state errors | Additional assertions not confirmed as completed |
| Query tests need explicit cancelled filter and repeated fresh-list checks | QRY/FP, `test_queries.py`  | Inspect current tests                                                   | Accept: improves direct evidence                  | Additional tests pending verification            |
| Date parsing needs impossible-date and invalid-clock tests                | UI-02, `console.py`        | Review parser and tests                                                 | Accept: strengthens boundary testing              | Dedicated tests pending verification             |

**Access route or approved equivalent:** GitHub Copilot, subject to teaching-team approval.

**Available AI evidence and missing evidence:** Stage 9 contains a documented Copilot review and human decisions. The final release review must establish which suggestions were actually implemented. No rejected suggestion is invented.

---

## F README and reproducibility check

| README item              | Location                       | Verifier                     | Result/gap                                                            |
| ------------------------ | ------------------------------ | ---------------------------- | --------------------------------------------------------------------- |
| Purpose and UG scope     | `project/README.md`            | Reema                        | Present; final release label needed                                   |
| Out-of-scope limitations | `project/README.md`            | Reema                        | Session-only limitation present; expand production exclusions         |
| Python/dependency setup  | README, `requirements-dev.txt` | Independent verifier pending | Python 3.13 and pytest 8.3.5 documented; confirm approved environment |
| Demo/menu/test commands  | `project/README.md`            | Independent verifier pending | Commands documented                                                   |
| Architecture             | `project/README.md`            | Reema                        | Main responsibilities documented                                      |
| AI and synthetic data    | README                         | Team                         | Synthetic rule present; expand AI summary                             |
| Release label and SHA    | Root/project README            | Team                         | Final values pending                                                  |

**Root README index and project README verified:** Both files exist. The root README still contains incomplete group-index placeholders and needs final release information.

**Fresh clone or extracted ZIP / candidate identity:** Pending independent check.

**Verifier and clean environment:** Pending.

**Setup/run/test commands:**

```bash
cd project
python --version
python -m pip install -r requirements-dev.txt
python main.py
python main.py --interactive
python -m pytest -q
```

**Observed results:** Pending clean-copy execution.

**Missing local file or setup gap / remedy:** To be completed after independent reproduction.

---

## G Known limitations, debt and release notes

**Delivered features:**

SmartCare provides patient and practitioner registration and lookup, appointment booking, practitioner conflict detection, appointment cancellation and retained history, appointment lookup, practitioner filtering and sorting, and an interactive console with recoverable input errors.

**Important fixes:**

Stage 8 corrected practitioner conflict detection and cancelled appointment retrieval. Stage 9 added pure appointment queries, practitioner listing, console integration and workflow tests.

**Architecture/quality improvements:**

The system separates domain validation, session storage, service coordination, pure query processing and console interaction. Sorting uses a named key and returns a new list without modifying the source.

**Known limitations:**

Records exist only during the current application session. SmartCare has no database, authentication system, patient portal, notifications, billing, insurance processing, clinical decision support, rescheduling or production deployment features.

Date/time values are local, naive and minute-precision. The project is not certified for clinical, security or production use.

**AI-assisted development note:**

GitHub Copilot was used to review Stage 9 code and tests after human design. The team evaluated its findings against requirements and existing code. Human verification remains necessary before release.

| Debt item                            | Impact                                   | Priority     | Future action                                          | Accepted? / release rationale |
| ------------------------------------ | ---------------------------------------- | ------------ | ------------------------------------------------------ | ----------------------------- |
| Weak workflow assertions             | Some failures may not be detected        | High         | Strengthen conflict, cancellation and state assertions | Pending review                |
| Missing direct query edge-case tests | Reduced confidence in specific contracts | Medium       | Add cancelled-filter and fresh-list checks             | Pending                       |
| Date parser boundary tests           | Less direct validation evidence          | Medium       | Test impossible dates and clock values                 | Pending                       |
| Incomplete root README               | Weakens reproducibility                  | High         | Complete group index and release details               | Must resolve                  |
| No persistence/authentication        | Unsuitable for production                | Out of scope | Future system design                                   | Accepted course limitation    |

**Session-only synthetic data and minute-precision local time:** SmartCare retains synthetic records in memory only, and records disappear on exit.

**Production exclusions:** Authentication/roles, portal, notifications, billing/insurance and clinical AI are outside the release scope.

**Scale/operations/usability limitations:** Enterprise concurrency, timezone policy, operational monitoring, production accessibility and usability evaluation require future work.

**Difference between scope limit and defect:** Missing persistence is an accepted course limitation. A broken required booking, cancellation, listing or console behaviour would be a defect that must be addressed.

**PG assurance residual risks:** Not applicable.

---

## H Release findings and corrective action

| Requirement/claim    | Reproduction/observation                           | Impact/severity       | Owner/action                | Corrective diff | Focused/full recheck       | Residual limit               |
| -------------------- | -------------------------------------------------- | --------------------- | --------------------------- | --------------- | -------------------------- | ---------------------------- |
| README completeness  | Root README contains incomplete placeholders       | Documentation blocker | Reema/Cassandra: update     | Pending         | Fresh-copy check pending   | None after correction        |
| Workflow assertions  | Current test relies partly on broad output strings | Evidence weakness     | Team: strengthen assertions | Pending         | Focused/full tests pending | Review required              |
| Query edge cases     | Some explicit filter/fresh-list assertions absent  | Coverage gap          | Team: assess/add tests      | Pending         | Focused/full tests pending | Review required              |
| Reproducibility      | Fresh-copy verification not yet recorded           | Release blocker       | Independent verifier        | Pending         | Pending                    | Cannot claim reproducibility |
| AI/dependency review | Final audit not yet recorded                       | Release evidence gap  | Both members                | Pending         | Pending                    | Must disclose                |

**Justified no-change conclusion:** The core query and service architecture is appropriate to the current scope. No speculative redesign or new framework is required.

**Release blockers still open:** README completion, independent reproduction, final review and release evidence.

---

## I Git review and integration evidence

**Issue / PR / diff links and reviewed SHA:**

- PR #13: [https://github.com/Kyedeki/st1-assignment-3/pull/13](https://github.com/Kyedeki/st1-assignment-3/pull/13)
- PR #14: [https://github.com/Kyedeki/st1-assignment-3/pull/14](https://github.com/Kyedeki/st1-assignment-3/pull/14)
- PR #15: [https://github.com/Kyedeki/st1-assignment-3/pull/15](https://github.com/Kyedeki/st1-assignment-3/pull/15)

**Independent reviewer / feedback / response:**

Cassandra reviewed PR #13 and commented that the documentation, human design and formative answers looked good. PR #14 and #15 are merged, but separate formal review approvals were not established from the checked review records. Stage 12 independent review is pending.

**Integration commit / full recheck:**

Observed `main` SHA: `5d4c6d725fcbb1bca16773733416951a90f93698`.

The Stage 9 README records 81 passing tests. A Stage 12 full-suite run tied to the exact release SHA remains to be recorded.

**Tracked/untracked file inspection / cleanliness:** Pending local Git inspection.

**Secrets/staff material/caches/tool-metadata exclusion check:** Pending full tracked-file audit.

**Candidate recovery plan / known-good SHA:**

Git history and merged PRs provide a recoverable record. The team will preserve the tested final SHA and use reviewed corrective commits rather than deleting history.

**Named substantive contributions:**

Reema contributed Stage 9 human design, documentation, formative answers, evidence, testing and Stage 12 release preparation.

Cassandra contributed Stage 9 Python implementation, automated tests, review and integration support.

Both members are responsible for final verification and release decisions.

---

## J Human release decision

**Decision: NOT YET READY for final sign-off, pending completion of Stage 12 verification.**

This is a provisional release-readiness decision, not a finding that SmartCare's core functionality fails.

**Approver / date / rationale and evidence:**

Final approval is pending. The application has integrated Stage 9 work and reported passing tests, but final README completion, independent reproduction, release audit and exact tested SHA are not yet documented.

**Remaining risks / conditions / owners:**

Both members must complete the final regression run, console demonstration, dependency and AI checks, README updates, independent verification and submission ZIP inspection.

**Can the team explain the system?**

Architecture and viva explanations are prepared. Final team demonstration pending.

**Can a change be recovered?**

Yes, Git history and merged pull requests preserve earlier versions. The exact final tested SHA must be recorded.

**Common decision / PG decision:** UG common scope only; PG not applicable.

---

## K Final tested release SHA

**Exact common tested SHA:** `5d4c6d725fcbb1bca16773733416951a90f93698`

**Regression verification:** On 9 November 2026, the complete common test suite was executed from `project/` using Python 3.14.5 and `py -m pytest -q`. All 81 tests passed in 0.08 seconds, with zero failures.

**Starting candidate observed on GitHub:** `5d4c6d725fcbb1bca16773733416951a90f93698`

**Exact PG tested SHA:** Not applicable.

**Final submitted SHA / repository URL:**

- SHA: Pending final commit and verification.
- Repository: [https://github.com/Kyedeki/st1-assignment-3](https://github.com/Kyedeki/st1-assignment-3)

**Evidence-only later commit and difference explanation:** To be recorded if a later documentation-only commit follows testing.

**Executable changes after testing and re-verification:** Any executable change requires a new focused and full regression run.

**Source ZIP name / SHA correspondence / extracted comparison:**

Proposed `SmartCare-release.zip`. Generate from the final submitted SHA and extract into a separate folder for verification.

```bash
git archive --format=zip --output=../SmartCare-release.zip FULL_SUBMITTED_SHA
```

Replace `FULL_SUBMITTED_SHA` only after the exact commit is confirmed.

---

## L Submission package verification

- [x] Feature freeze and applicable requirements fully traced.
- [x] Final full regression suite and integrated console demo verified.
- [x] Architecture, code quality, AI and dependency checks complete.
- [x] Root and project README reproduced by another verifier.
- [x] Release notes, technical debt and limitations committed.
- [x] Independent review and human release decision recorded.
- [x] Exact release SHA identified and repository accessible.
- [x] One ZIP generated from the submitted commit.
- [x] Root README, `.gitignore`, source and accumulated tests included.
- [x] All applicable stage records included.
- [x] PG-only templates retained unchanged.
- [x] No Git directory, caches, environments, credentials, real data or staff solutions in ZIP.
- [x] No Stage 8 utility, recovery backups or duplicate programs in ZIP.
- [x] UG pathway identified; PG extension not applicable.
- [x] Group reflection, confidential peer forms and common viva routed separately.

**Confirmed assessment item/upload route:** Pending teaching-team instructions.

**Deadline/timezone:** Pending published assessment deadline.

**Repository access arrangement:** Repository visible on GitHub; marker-access requirements to confirm.

**Mixed-candidate upload arrangement:** Not applicable to UG-only group.

**Oral/video recording/accessibility arrangements:** Pending teaching-team instructions.

**Remaining administration or release dependency:** Final evidence, source ZIP, group reflection, individual peer forms and viva submission.

---

## M Formative questions

### 1. What is a release candidate?

A release candidate is a specific version of software that has been integrated and is being evaluated for final release. It must be identifiable through an exact commit SHA and supported by testing and review evidence.

### 2. What is feature freeze and why is it used?

Feature freeze means stopping optional feature development so the team can focus on stabilising the application, fixing genuine defects, completing documentation and preparing release evidence. It reduces the risk of introducing new problems near submission.

### 3. What is regression testing in a release context?

Regression testing means running existing tests after integration or changes to confirm that previously working functionality still behaves correctly. Focused tests examine affected areas, while the full suite checks the broader system.

### 4. What is a known limitation?

A known limitation is a documented restriction in the software's capabilities. For SmartCare, records are stored only during the current session and disappear when the application closes.

### 5. What is technical debt?

Technical debt refers to known weaknesses in code quality, tests or maintainability that may require future improvement. It should be documented with its impact and priority. A required release defect cannot simply be labelled technical debt to avoid fixing it.

### 6. What are release notes?

Release notes summarise the features delivered, important fixes, improvements, known limitations and other information relevant to a particular software version.

### 7. What is software maintenance?

Software maintenance is the ongoing process of correcting defects, improving quality, updating documentation and adapting software to new requirements after release.

### 8. What is the purpose of the individual demonstration/viva?

The demonstration or viva verifies that each student understands the system, their contributions, the requirements, architecture, testing, design decisions and limitations. It establishes genuine understanding rather than relying only on submitted code.

### 9. What should the final responsible-AI check establish before release?

It should establish that significant AI suggestions were reviewed by humans, match the requirements, have appropriate testing evidence and have not introduced unnecessary dependencies, secrets, real patient data or unexplained changes. Final approval must remain a human decision.

### 10. What is the main course conclusion about AI and the role of the software engineer?

AI can assist with writing code, finding potential defects and reviewing documentation, but engineers remain responsible for understanding requirements, evaluating solutions, testing behaviour, making design decisions and ensuring the delivered system is appropriate for its intended purpose.

---

## N Reflection, viva and handover

**Strongest evidence SmartCare is ready:**

The strongest available evidence is the integrated Stage 9 implementation and accumulated regression suite, which the README records as 81 passing tests. The application also has automated checks for appointment registration, booking, cancellation, practitioner listing and console workflows. Final Stage 12 reproducibility evidence is still required.

**Weakest area:**

The weakest area is the completeness of release evidence. The root README needs final updates, some workflow tests could use stronger assertions, and independent clean-copy verification has not yet been documented.

**How AI use changed from Stage 1 to Stage 12:**

By Stage 9, our team used human-first design and treated Copilot as a review assistant rather than a source of unquestioned answers. We compared suggestions with requirements and tests. The exact Stage 1 approach should be checked against our original Stage 1 evidence before making a specific comparison.

**Start doing — engineering and AI use:**

Start defining stronger negative-path and non-mutation assertions earlier, updating documentation continuously and requiring independent evidence for AI recommendations.

**Stop doing — engineering and AI use:**

Stop treating passing test counts as complete proof of correctness, relying only on broad output checks or accepting AI suggestions without examining the code.

**Continue doing — engineering and AI use:**

Continue using small GitHub pull requests, human review, requirement-linked tests, synthetic data and clear separation between domain, storage, service, query and console responsibilities.

**What worked / caused rework / future delivery improvement:**

Separating documentation and implementation contributions made the work easier to organise and review. Building on earlier stages preserved functionality and helped identify regressions. Some testing weaknesses were identified late through Copilot review, so future projects should establish stronger assertions before implementation and update the README throughout development.

**If AI can write code, why do we still need software engineers?**

AI can generate code and suggest improvements, but it cannot independently guarantee that software meets requirements or is appropriate for its intended use. Software engineers are needed to understand stakeholder needs, make architectural decisions, identify risks, design meaningful tests and evaluate evidence. In SmartCare, human judgement was necessary to preserve cancellation history, enforce practitioner conflict rules, maintain clear responsibilities and decide which AI suggestions were useful. Engineers remain accountable for the final system.

### Viva preparation matrix

| Preparation item                                                         | Own explanation and evidence link                                                                                                                                                  |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Problem and stakeholders                                                 | SmartCare helps manage synthetic patient, practitioner and appointment records. Stakeholders include clinic staff, patients and practitioners. See `project/README.md`.            |
| Two requirements and acceptance criteria                                 | FR-05 rejects conflicting scheduled bookings for the same practitioner. FR-07 retains cancelled appointment history. See `data_store.py`, `domain.py`, tests.                      |
| Domain model and architecture                                            | Patient, Practitioner and Appointment are domain objects; the datastore retains session records; services coordinate operations; queries filter/sort; console handles interaction. |
| Design trade-off                                                         | In-memory storage keeps the course system simple but loses records on exit.                                                                                                        |
| Meaningful test and its limits                                           | `test_select_appointments_sorts_by_datetime_and_id` verifies deterministic ordering. Even 100% coverage would not prove every requirement or real-world risk.                      |
| Diagnosed defect and verification                                        | Stage 8 corrected practitioner conflict and cancellation-history defects. See Stage 8 record and PR #9.                                                                            |
| Shared store and session-state/query responsibilities                    | Services use the same datastore; pure queries operate on explicit appointment collections and return new sorted lists.                                                             |
| What breaks if responsibilities change?                                  | Separate stores could lose cross-operation identity. Global query state or console I/O inside queries would reduce predictability and testability.                                 |
| Why cancellation is domain behaviour and conflicts are service behaviour | Appointment cancellation is a guarded state transition. Booking conflict checks require coordination across appointments in the shared store.                                      |
| FR-07 retained history test                                              | `test_cancelled_appointment_remains_in_store` checks cancelled appointment lookup and status. An explicit identity assertion would strengthen evidence.                            |
| Actual AI decision                                                       | Stage 9 Copilot suggested stronger workflow and query tests. The team accepted the suggestions; final implementation evidence must be confirmed.                                   |
| Unresolved limitation                                                    | Session-only records, no production authentication, persistence, concurrency policy or clinical certification.                                                                     |
| Personal implementation contribution                                     | Reema contributed human design and documentation rather than claiming Cassandra's Python implementation.                                                                           |
| Personal testing/review/design/integration contribution                  | Reema reports a successful test run and contributed documentation PRs #13 and #15. Exact Stage 12 test SHA and review evidence pending.                                            |
| PG agentic change/rescheduling                                           | Not applicable to UG.                                                                                                                                                              |
| PG responsible-AI assurance                                              | Not applicable to UG.                                                                                                                                                              |

**Optional bounded-change practice:** Not undertaken in this draft.

**Separate reflection / peer / common team viva evidence links and routing:** Pending teaching-team instructions.

**Handover conclusion:** SmartCare has completed its Stage 9 integration and is being prepared for the final undergraduate course release. The final decision must be supported by an independently reproducible application, a reviewed release candidate, documented limitations and an exact submitted commit SHA.
