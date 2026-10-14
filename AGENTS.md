# AI Development Instructions

## 1. General Principles
- Treat the project requirements as authoritative.
- Do not invent requirements or silently make significant assumptions.
- Prefer simple, readable, maintainable solutions.
- Avoid unnecessary abstractions, dependencies, and features.
- Do not rewrite working code without a clear reason.
- Explain important trade-offs before making significant design changes.
- For ambiguities that could materially affect the result, follow the clarification rule in §8.

## 2. Before making changes
- Inspect the relevant existing code and documentation.
- Understand the current behavior before modifying it.
- Identify ambiguities, missing requirements, and potential edge cases.
- Ask questions when unresolved issues could materially affect the result.
- For nontrivial tasks, propose an implementation plan before coding.
- Identify the files expected to change.

## 3. Implementation
- The implementation plan should indentify the exact tasks to be performed, the order in which they will be executed, and the expected changes to the codebase.
- Dont implement all tasks at once; focus on one small, manageable change at a time.
- Review and test each change before moving on to the next task.
- Make small, focused changes.
- Follow the existing project conventions.
- Keep functions focused on a clear responsibility.
- Validate external input.
- Handle errors explicitly and provide useful error messages.
- Avoid unrelated refactoring.
- Do not add dependencies without explaining why they are needed.
- Do not introduce features that were not requested.

## 4. Testing
- Derive tests from the approved requirements.
- Include relevant normal cases, boundary cases, and error cases.
- Do not change expected test results merely to make tests pass.
- Do not remove or weaken tests without justification.
- Run relevant tests after making changes.
- Report which checks were run and their actual results.
- Never claim that a test passed if it was not executed.

## 5. Safety
- Do not expose secrets, credentials, or private data.
- Do not execute destructive operations without authorization.
- Do not delete or overwrite user data without understanding the consequences.
- Ask before making irreversible changes.
- Do not modify unrelated files.
- Do not install packages or change the environment unnecessarily.

## 6. Review
Before considering a task complete:

- Inspect the final diff.
- Check for regressions and unintended changes.
- Check error handling and relevant security concerns.
- Verify the acceptance criteria.
- Update documentation when necessary.

## 7. Final report

The final report is always required. Keep it compact: one short
bullet per category below unless more detail is requested.

Summarize:
- What changed and why.
- Which files were modified.
- Which tests and checks were executed and their results.
- Known limitations or unresolved questions.
- Any decisions that require user approval.

## 8. Context and Token Efficiency

- Read the project instructions before starting work.
- Do not repeatedly restate information already documented.
- Load only the documentation, source files, and tests
  relevant to the current task.
- Inspect existing code before proposing replacements.
- Prefer targeted inspection over dumping entire files
  or the entire repository into context.
- Reuse established project conventions and decisions.
- If an ambiguity would materially affect implementation, correctness,
  safety, or scope, stop and seek clarification before proceeding.
  For minor ambiguities with an obviously reasonable interpretation,
  proceed, and state the assumption in the final report.
- Do not generate lengthy explanations unless requested.
- Prefer concise plans that identify the proposed changes,
  relevant files, risks, and verification steps.
- Implement the smallest change that fully satisfies the approved requirements — including required validation, error handling, and tests — and nothing beyond them.
- Avoid unrelated refactoring and speculative features.
- Do not repeat successful test output unnecessarily.
- Summarize completed work, verification results,
  and unresolved issues concisely.
- Never omit essential context or verification merely
  to reduce token usage.
- 'Essential' minimally includes: the requirements being
  implemented, the code and tests being modified, verification
  commands and their actual results, and anything required by §7.
- If context is insufficient, inspect the relevant files
  or ask for clarification rather than guessing.

## 9. SPEC.md requirements

Every project must have a `SPEC.md` containing the following
sections unless the developer explicitly waives a section.

Do not omit, combine, or replace a required section merely because
you consider it unnecessary. Only the developer can waive a section.

### Required sections

1. **Purpose**
   - What we are building.
   - Who will use it.
   - What problem it solves.

2. **Scope**
   - What is included.
   - What is explicitly excluded.

3. **Requirements and Acceptance Criteria**
   - Expected behavior.
   - How we determine that each requirement is satisfied.

4. **Inputs, Outputs, and Errors**
   - Inputs the program accepts.
   - Expected outputs and observable side effects.
   - Expected error behavior and relevant edge cases.

5. **Constraints and Limitations**
   - Important restrictions, assumptions, and known limitations.

6. **Program Flow and Component Relationships**
   - Where program execution starts.
   - The main logical steps in execution order.
   - The responsibilities of the main functions or modules.
   - Which components call or depend on other components.
   - How data moves between components.
   - Where important decisions and error handling occur.

### Rules for creating and maintaining SPEC.md

- Work with the developer to develop and validate the specification.
  Do not invent requirements or silently make significant assumptions.
- If information is missing and materially affects requirements,
  ask the developer rather than deciding on their behalf.
- If a required section is incomplete, identify what is missing.
  A section may explicitly state that something is undecided,
  not applicable, or intentionally out of scope, where appropriate.
- If you believe a section should be omitted, explain why and ask
  the developer for explicit permission. Do not omit it while waiting
  for a response.
- A waiver applies only to the section explicitly identified by
  the developer. Do not interpret it as permission to omit other
  sections.
- Keep SPEC.md concise. Do not add unnecessary documentation or
  duplicate information without a clear reason.

### Program Flow and Component Relationships

- Include the program's logical flow and the relationships between
  its main components. This section is mandatory unless explicitly
  waived by the developer.
- Keep the level of detail proportional to the project's complexity.
- Describe the intended logical flow before implementation when
  enough information is available. Do not invent function names,
  modules, or implementation details that have not been decided.
- When the design or implementation becomes clearer, update the
  section to reflect the agreed-upon structure.
- Explain the entry point, main execution steps, component
  responsibilities, dependencies, and data flow as appropriate.
- Use Mermaid diagrams when they materially improve understanding.
  Do not add diagrams merely for decoration.
- Ensure that the description remains consistent with the agreed
  requirements and the actual implementation.
- If implementation reveals a necessary change to the agreed design,
  explain the discrepancy and seek developer input when the change
  affects requirements or an important design decision.

### Additional sections

- Additional sections may be proposed when they provide clear value.
- Explain why an additional section is useful and obtain the
  developer's approval before adding it.
- Do not expand the specification with unnecessary sections.