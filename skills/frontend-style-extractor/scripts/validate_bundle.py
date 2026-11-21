#!/usr/bin/env python3
"""Validate the Portable Design System Bundle v1.0.0 (Python stdlib only)."""

import argparse
import json
from pathlib import Path
import sys

VERSION = "1.0.0"
REQUIRED = [
    "manifest.json", "tokens.json", "rules.json", "README.md", "typography.md",
    "layout-rules.md", "component-rules.md", "interaction-rules.md", "responsive-rules.md",
]
GROUPS = {"color", "spacing", "typography", "radius", "shadow", "motion", "breakpoint", "zIndex"}
CATEGORIES = {"typography", "layout", "component", "interaction", "responsive", "accessibility", "asset"}
CONFIDENCE = {"high", "medium", "low"}
ORIGINS = {"observed", "inferred"}
PRIORITIES = {"required", "recommended", "optional"}
EVIDENCE_KINDS = {"code", "runtime", "visual"}


def good_string(v):
    return isinstance(v, str) and bool(v.strip())


def string_array(v, nonempty=False):
    return isinstance(v, list) and (bool(v) or not nonempty) and all(good_string(s) for s in v)


def read_json(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        errors.append(f"{path.name}: unable to parse JSON: {exc}")
        return None


def validate_evidence(owner, record, errors, warnings):
    origin = record.get("origin")
    conf = record.get("confidence")
    evidence = record.get("evidence")
    if origin not in ORIGINS:
        errors.append(f"{owner}.origin must be observed|inferred")
    if conf not in CONFIDENCE:
        errors.append(f"{owner}.confidence must be high|medium|low")
    if not isinstance(evidence, list):
        errors.append(f"{owner}.evidence must be an array")
        return
    if conf == "high" and not evidence:
        errors.append(f"{owner}: high confidence requires evidence")
    if origin == "inferred" and conf == "high":
        warnings.append(f"{owner}: inferred item marked high confidence; check justification")
    if not evidence and not good_string(record.get("notes", "")):
        warnings.append(f"{owner}: missing evidence and explanatory notes")
    for i, ev in enumerate(evidence):
        if not isinstance(ev, dict):
            errors.append(f"{owner}.evidence[{i}] must be an object")
            continue
        if ev.get("kind") not in EVIDENCE_KINDS or not good_string(ev.get("reference")):
            errors.append(f"{owner}.evidence[{i}]: expected kind=code|runtime|visual and nonempty reference")
        if "detail" in ev and not isinstance(ev["detail"], str):
            errors.append(f"{owner}.evidence[{i}].detail must be a string")


def validate(root):
    errors, warnings = [], []
    for required in REQUIRED:
        path = root / required
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing regular file: {required}")
        elif path.suffix == ".md" and not path.read_text(encoding="utf-8").strip():
            errors.append(f"empty Markdown file: {required}")
    if errors:
        return errors, warnings, 0, 0
    manifest = read_json(root / "manifest.json", errors)
    token_data = read_json(root / "tokens.json", errors)
    rule_data = read_json(root / "rules.json", errors)
    if errors:
        return errors, warnings, 0, 0
    for fname, data in (("manifest", manifest), ("tokens", token_data), ("rules", rule_data)):
        if not isinstance(data, dict):
            errors.append(f"{fname}.json must be a JSON object")
        elif data.get("schemaVersion") != VERSION:
            errors.append(f"{fname}.json schemaVersion must equal {VERSION}")
    if errors:
        return errors, warnings, 0, 0

    if not good_string(manifest.get("producer")):
        errors.append("manifest.producer must be a nonempty string")
    source = manifest.get("source")
    if not isinstance(source, dict) or any(not good_string(source.get(k)) for k in ("project", "framework", "styling")):
        errors.append("manifest.source needs project, framework, styling as nonempty strings")
    scope = manifest.get("scope")
    if not isinstance(scope, dict) or not string_array(scope.get("inspected"), nonempty=True) or not string_array(scope.get("notInspected")):
        errors.append("manifest.scope needs inspected (nonempty string array), notInspected (string array)")
    if manifest.get("visualVerification") not in {"performed", "partial", "not_performed"}:
        errors.append("manifest.visualVerification must be performed|partial|not_performed")
    if not string_array(manifest.get("limitations")):
        errors.append("manifest.limitations must be a string array")

    tokens = token_data.get("tokens")
    n_tokens = 0
    token_refs = set()
    if not isinstance(tokens, dict):
        errors.append("tokens.tokens must be an object of groups")
        tokens = {}
    for group, entries in tokens.items():
        if group not in GROUPS:
            errors.append(f"unknown token group: {group}")
        if not isinstance(entries, dict):
            errors.append(f"tokens.{group} must be an object")
            continue
        for name, tok in entries.items():
            owner = f"tokens.{group}.{name}"
            n_tokens += 1
            token_refs.add(f"{group}.{name}")
            if not good_string(name) or not isinstance(tok, dict):
                errors.append(f"{owner} must be a named object")
                continue
            if not good_string(tok.get("value")) or not good_string(tok.get("type")):
                errors.append(f"{owner} needs nonempty value and type strings")
            validate_evidence(owner, tok, errors, warnings)
    if n_tokens == 0:
        warnings.append("no tokens exported; adapter may have little to apply")

    rules = rule_data.get("rules")
    if not isinstance(rules, list):
        errors.append("rules.rules must be an array")
        rules = []
    ids = set()
    for i, rule in enumerate(rules):
        owner = f"rules[{i}]"
        if not isinstance(rule, dict):
            errors.append(f"{owner} must be an object")
            continue
        rid = rule.get("id")
        if not good_string(rid):
            errors.append(f"{owner}.id missing")
        elif rid in ids:
            errors.append(f"duplicate rule id: {rid}")
        else:
            ids.add(rid)
        if rule.get("category") not in CATEGORIES:
            errors.append(f"{owner}.category invalid")
        if not string_array(rule.get("appliesTo"), nonempty=True):
            errors.append(f"{owner}.appliesTo must contain one or more strings")
        if not good_string(rule.get("requirement")):
            errors.append(f"{owner}.requirement missing")
        if rule.get("priority") not in PRIORITIES:
            errors.append(f"{owner}.priority must be required|recommended|optional")
        if not string_array(rule.get("exceptions")):
            errors.append(f"{owner}.exceptions must be a string array")
        refs = rule.get("tokenRefs")
        if not string_array(refs):
            errors.append(f"{owner}.tokenRefs must be a string array")
        else:
            for ref in refs:
                if ref not in token_refs:
                    errors.append(f"{owner}.tokenRefs unknown token: {ref}")
        validate_evidence(owner, rule, errors, warnings)
    if not rules:
        warnings.append("rules array empty; no structured component/layout behavior to apply")
    return errors, warnings, n_tokens, len(rules)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("bundle", type=Path)
    args = p.parse_args()
    if not args.bundle.is_dir():
        p.error(f"bundle directory not found: {args.bundle}")
    errors, warnings, count_tokens, count_rules = validate(args.bundle)
    for warning in warnings:
        print("WARN:", warning)
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        print(f"INVALID bundle | errors={len(errors)} warnings={len(warnings)}", file=sys.stderr)
        raise SystemExit(1)
    print(f"VALID bundle v{VERSION} | tokens={count_tokens} rules={count_rules} warnings={len(warnings)}")


if __name__ == "__main__":
    main()
