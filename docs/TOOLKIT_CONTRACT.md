# Language toolkit contract

The contract is intentionally small. A language-specific repository may use any
architecture, but it must make these boundaries inspectable.

## Required identity

- language and named variety;
- ISO 639-3 code where applicable;
- supported scripts and orthographic conventions;
- maintainers and current lifecycle stage.

## Required frontend behavior

- a documented text-to-phone or text-normalization entry point;
- deterministic handling of Unicode normalization;
- explicit behavior for unknown graphemes—silent deletion is not acceptable;
- unit tests for language-specific contrasts and shared-script failure modes.

## Required evidence

- source and version for every pronunciation or phonology claim;
- exact evaluation split and metric definition;
- aggregate accuracy plus contrast-conditioned diagnostics where relevant;
- explicit separation of gold, silver, development, and held-out evidence;
- runnable examples that do not require restricted inputs.

## Required release boundaries

- code, data, model, and demo versions are tracked independently;
- restricted corpora, speaker audio, and checkpoints are never implied to be public;
- model cards record training-data provenance and consent/rights status;
- large artifacts live in a versioned artifact store, not Git history.

## Lifecycle stages

- `planned`: identity and evidence sources are known; implementation has not started.
- `scaffolded`: repository and tests exist, but the core path is incomplete.
- `implemented`: the component runs and has documented evaluation.
- `demonstrated`: a fixed or interactive artifact shows the component operating.
- `released`: the implementation and required runtime artifacts are publicly reusable
  under stated terms.

These stages are per component. A toolkit can have a released frontend and only a
demonstrated TTS model.
