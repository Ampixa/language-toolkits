# Contributing a toolkit

Before adding a registry entry:

1. Verify the language or named variety and its ISO 639-3 code where one exists.
2. Create or identify one canonical implementation repository.
3. Document scripts, orthographic conventions, phonological sources, and known gaps.
4. Add executable frontend tests, including at least one contrast a generic shared-
   script baseline can collapse.
5. Record data provenance, redistribution terms, and speaker-consent requirements.
6. Separate development-set, held-out, and listening-test results.
7. Run `python scripts/validate_registry.py`.

Do not commit raw audio, checkpoints, corpus dumps, dictionary exports, copyrighted
PDFs, credentials, or generated text manifests unless redistribution rights are
documented and the repository is designed to carry them.

Use one pull request for one language or one contract change. Registry claims must
link to the exact repository, artifact, or evaluation output that supports them.
