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