#!/usr/bin/env python3
"""Validate the Ampixa language-toolkit registry without third-party packages."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "registry/toolkits.json"
DEFAULT_CANDIDATES = REPO_ROOT / "registry/candidates.tsv"
ISO_CODE = re.compile(r"^[a-z]{3}$")
ID = re.compile(r"^[a-z][a-z0-9-]*$")
VISIBILITIES = {"public", "private"}
STAGES = {"planned", "scaffolded", "implemented", "demonstrated", "released"}
COMPONENTS = {"frontend", "evaluation", "tts"}
REQUIRED_FIELDS = {
    "id",
    "name",
    "iso_639_3",
    "scripts",
    "canonical_repository",
    "repository_visibility",
    "public_entrypoint",
    "components",
}


class RegistryError(ValueError):
    """Raised when a registry invariant is violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryError(message)


def is_https_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def load_registry(registry_path: Path) -> dict[str, Any]:
    try:
        with registry_path.open(encoding="utf-8") as registry_file:
            payload = json.load(registry_file)
    except OSError as exc:
        raise RegistryError(f"cannot read registry {registry_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"invalid JSON in {registry_path}: {exc}") from exc
    require(isinstance(payload, dict), "registry root must be a JSON object")
    return payload


def validate_registry(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == 1, "schema_version must be 1")
    program = payload.get("program")
    require(isinstance(program, dict), "program must be an object")
    target = program.get("target_language_count")
    declared_count = program.get("registered_toolkit_count")
    require(isinstance(target, int) and target > 0, "target_language_count must be positive")

    toolkits = payload.get("toolkits")
    require(isinstance(toolkits, list), "toolkits must be an array")
    require(declared_count == len(toolkits), "registered_toolkit_count does not match toolkits")
    require(target >= len(toolkits), "target_language_count is smaller than the registry")

    seen_ids: set[str] = set()
    seen_iso_codes: set[str] = set()
    for index, toolkit in enumerate(toolkits):
        label = f"toolkits[{index}]"
        require(isinstance(toolkit, dict), f"{label} must be an object")
        missing = REQUIRED_FIELDS.difference(toolkit)
        require(not missing, f"{label} missing fields: {sorted(missing)}")

        toolkit_id = toolkit["id"]
        require(isinstance(toolkit_id, str) and ID.fullmatch(toolkit_id) is not None, f"{label}.id is invalid")
        require(toolkit_id not in seen_ids, f"duplicate toolkit id: {toolkit_id}")
        seen_ids.add(toolkit_id)

        iso_codes = toolkit["iso_639_3"]
        require(isinstance(iso_codes, list) and iso_codes, f"{label}.iso_639_3 must be non-empty")
        for iso_code in iso_codes:
            require(isinstance(iso_code, str) and ISO_CODE.fullmatch(iso_code) is not None, f"{label} has invalid ISO code: {iso_code!r}")
            require(iso_code not in seen_iso_codes, f"duplicate ISO code: {iso_code}")
            seen_iso_codes.add(iso_code)

        scripts = toolkit["scripts"]
        require(isinstance(scripts, list) and all(isinstance(item, str) and item for item in scripts), f"{label}.scripts must contain names")

        repository = toolkit["canonical_repository"]
        require(is_https_url(repository), f"{label}.canonical_repository must be an HTTPS URL")
        require(repository.startswith("https://github.com/Ampixa/"), f"{label}.canonical_repository must be under Ampixa")
        require(toolkit["repository_visibility"] in VISIBILITIES, f"{label}.repository_visibility is invalid")
        require(is_https_url(toolkit["public_entrypoint"]), f"{label}.public_entrypoint must be an HTTPS URL")

        components = toolkit["components"]
        require(isinstance(components, dict), f"{label}.components must be an object")
        require(set(components) == COMPONENTS, f"{label}.components must be {sorted(COMPONENTS)}")
        for component, stage in components.items():
            require(stage in STAGES, f"{label}.components.{component} has invalid stage: {stage!r}")


def validate_candidates(candidates_path: Path, target_count: int) -> int:
    try:
        with candidates_path.open(encoding="utf-8", newline="") as candidates_file:
            rows = list(csv.DictReader(candidates_file, delimiter="\t"))
    except OSError as exc:
        raise RegistryError(f"cannot read candidates {candidates_path}: {exc}") from exc

    expected_fields = ["id", "name", "source", "origin"]
    if rows:
        require(list(rows[0]) == expected_fields, f"candidate fields must be {expected_fields}")
    require(rows, "candidate inventory must not be empty")
    require(len(rows) <= target_count, "candidate inventory exceeds target_language_count")

    seen_ids: set[str] = set()
    for index, row in enumerate(rows):
        label = f"candidates[{index}]"
        candidate_id = row["id"]
        require(ID.fullmatch(candidate_id) is not None, f"{label}.id is invalid")
        require(candidate_id not in seen_ids, f"duplicate candidate id: {candidate_id}")
        seen_ids.add(candidate_id)
        require(bool(row["name"]), f"{label}.name is empty")
        require(row["origin"] in {"nepal-matribhasha", "local-workspace"}, f"{label}.origin is invalid")
        if row["origin"] == "nepal-matribhasha":
            require(is_https_url(row["source"]), f"{label}.source must be an HTTPS URL")
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    args = parser.parse_args()
    try:
        payload = load_registry(args.registry)
        validate_registry(payload)
        candidate_count = validate_candidates(
            args.candidates, payload["program"]["target_language_count"]
        )
    except RegistryError as exc:
        print(f"registry validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"registry valid: {len(payload['toolkits'])} implemented toolkits, "
        f"{candidate_count} verified candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
