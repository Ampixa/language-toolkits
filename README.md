# Ampixa Language Toolkits

This repository is the public index and shared engineering contract for Ampixa's
language technology work. The program target is **44 languages or named varieties**.
The implementation registry currently contains the six frontends demonstrated in the
SLT 650 work. A separate candidate inventory records **43 verified workspace/site
identities**: 40 from Nepal MatriBhasha plus Chamling, Chhiling, and Dumi workspace
entries. One of the 44 target slots is still unresolved and will not be invented merely
to make the count look complete.

The umbrella is deliberately not a dump of 44 codebases. Each mature language keeps
an independent implementation repository so releases, maintainers, data rights, and
model histories do not become entangled. This repository owns the cross-language
registry, readiness stages, evaluation contract, and links to runnable evidence.

## Current registry

| Toolkit | ISO 639-3 | Frontend | TTS | Public entry point |
| --- | --- | --- | --- | --- |
| Nepali | `nep` | implemented | demonstrated | [source](https://github.com/Ampixa/nepa-newa-text-frontend) |
| Limbu | `lif` | implemented | demonstrated | [reviewer source archive](https://huggingface.co/spaces/voidash/slt-650-reviewer-artifact/resolve/main/downloads/slt650_training_inference_source.zip) |
| Magar | `mgp`, `mrd` | implemented | demonstrated | [reviewer source archive](https://huggingface.co/spaces/voidash/slt-650-reviewer-artifact/resolve/main/downloads/slt650_training_inference_source.zip) |
| Bantawa | `bap` | implemented | demonstrated | [reviewer source archive](https://huggingface.co/spaces/voidash/slt-650-reviewer-artifact/resolve/main/downloads/slt650_training_inference_source.zip) |
| Gurung | `gvr` | implemented | demonstrated | [reviewer source archive](https://huggingface.co/spaces/voidash/slt-650-reviewer-artifact/resolve/main/downloads/slt650_training_inference_source.zip) |
| Dhimal | `dhi` | implemented | demonstrated | [source](https://github.com/Ampixa/dhimal-speech-toolkit) |

Runnable evidence and fixed examples are collected in the
[six-language demo](https://voidash-slt-650-reviewer-artifact.hf.space). A registry
entry records what exists; it is not a claim that every dataset or model can be
redistributed.

## Repository model

```text
Ampixa/language-toolkits          registry, standards, roadmap, shared evaluation
Ampixa/<language>-speech-toolkit  canonical language-specific implementation
Hugging Face                     checkpoints, demos, and large versioned artifacts
```

Do not copy a language implementation into this repository. Shared code should be
extracted only after at least two toolkits use the same stable interface; premature
abstraction would hide language-specific phonological decisions.

## Validate the registry

```bash
python scripts/validate_registry.py
```

The validator checks required fields, ISO-code syntax, unique identifiers, allowed
status values, Ampixa repository URLs, and candidate-inventory uniqueness/counts. CI
runs it on every change.

## Add a language

Read [the toolkit contract](docs/TOOLKIT_CONTRACT.md) and
[the contribution guide](CONTRIBUTING.md). A useful teaser is not an empty folder: it
must name the language/variety, state its script and phonological scope, link its
sources and rights status, include at least one executable test, and separate observed
results from planned work.

## Licensing

No repository-wide license has been selected yet. Individual linked repositories,
datasets, models, and references retain their own terms. Public visibility does not
override those terms.
