#!/usr/bin/env python3
"""Plan and assemble a traceable contest submission without changing source files."""

import argparse
import contextlib
import contextvars
import os
import stat
import ast
import datetime as dt
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote


AUDITS = {
    "consistency": "paper/audits/cross_media_consistency_audit.md",
    "completeness": "paper/audits/completeness_audit.md",
    "quality_assurance": "paper/qa_report.md",
}
GOOD = {"PASS", "PASSED", "SUCCESS", "SUCCEEDED", "COMPLETE", "COMPLETED", "OK"}
IMAGE = re.compile(r"(!\[[^\]]*\]\()([^\s)]+)([^)]*\))")
TEX_IMAGE = re.compile(r"(\\includegraphics\*?(?:\[[^]]*\])?\{)([^}]+)(\})")
DATA_LITERAL = re.compile(r"(?:workspace/)?data_(?:clean|raw)/[\w. /\\-]+\.(?:csv|xlsx|xls|mat|txt|json)")
VERDICT = re.compile(r"^\s*(?:verdict|final verdict|结论|审计结论)\s*[:：]\s*(\w+)", re.I | re.M)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for part in value:
            yield from strings(part)
    elif isinstance(value, dict):
        for part in value.values():
            yield from strings(part)


_PATH_SOURCES = contextvars.ContextVar("packager_path_sources", default=None)


@contextlib.contextmanager
def _path_scope():
    existing = _PATH_SOURCES.get()
    if existing is not None:
        yield existing
        return
    events = []
    token = _PATH_SOURCES.set(events)
    try:
        yield events
    finally:
        _PATH_SOURCES.reset(token)

def _path_record(ws, value, origin, kind="file", allow_missing=False):
    """Batch A observations only: not a lock or a publication guarantee."""
    import ctypes as ct
    from ctypes import wintypes as wt
    if sys.platform != "win32":
        raise ValueError("C2_A_DECISION_REQUIRED: safe discovery is qualified only for Windows/local fixed NTFS")
    if not isinstance(value, str) or not value or value != value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f"C2_A_INVALID_PATH: {origin}: {value!r}")
    path = Path(value)
    if path.drive and (not path.root or path.drive.startswith("\\\\")):
        raise ValueError(f"C2_A_DECISION_REQUIRED: drive-relative/UNC/device path: {origin}: {value!r}")
    if any(c in value for c in '<>"|?*') or ":" in value[2:] or value.startswith(("\\\\", "//")):
        raise ValueError(f"C2_A_INVALID_PATH: device/ADS/illegal path: {origin}: {value!r}")
    if any(part.rstrip(". ") != part or part.split(".")[0].upper() in
           {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1,10)), *(f"LPT{i}" for i in range(1,10))}
           for part in path.parts[1 if path.anchor else 0:] if part not in {".", ".."}):
        raise ValueError(f"C2_A_DECISION_REQUIRED: Windows name alias: {origin}: {value!r}")
    lexical = path if path.is_absolute() else (Path(ws) if ws is not None else Path.cwd()) / path
    normalized = Path(os.path.abspath(lexical))  # lexical normalization, not resolve
    if ws is not None and not normalized.is_relative_to(Path(os.path.abspath(ws))):
        raise ValueError(f"C2_A_ESCAPE: {origin}: {value!r}")
    # Inspect the uncollapsed lexical chain; a junction before '..' must not vanish.
    chain = list(reversed(lexical.parents)) + [lexical]
    observations = []
    missing = False
    for node in chain:
        try:
            info = node.lstat()
        except FileNotFoundError:
            missing = True
            if allow_missing:
                continue
            raise ValueError(f"C2_A_MISSING: {origin}: {value!r}; component={node}")
        if missing:
            raise ValueError(f"C2_A_AMBIGUOUS_ANCESTRY: {origin}: {value!r}")
        if info.st_file_attributes & 0x400:
            raise ValueError(f"C2_A_REPARSE: {origin}: {value!r}; component={node}")
        observations.append((str(node), info.st_dev, info.st_ino))
    probe = next((p for p in [lexical] + list(lexical.parents) if p.exists()), None)
    k = ct.WinDLL("kernel32", use_last_error=True)
    k.GetVolumePathNameW.argtypes = [wt.LPCWSTR, wt.LPWSTR, wt.DWORD]
    k.GetVolumeInformationW.argtypes = [wt.LPCWSTR, wt.LPWSTR, wt.DWORD, ct.POINTER(wt.DWORD), ct.POINTER(wt.DWORD), ct.POINTER(wt.DWORD), wt.LPWSTR, wt.DWORD]
    k.GetDriveTypeW.argtypes = [wt.LPCWSTR]
    root, fs = ct.create_unicode_buffer(1024), ct.create_unicode_buffer(1024)
    serial, limit, flags = wt.DWORD(), wt.DWORD(), wt.DWORD()
    if probe is None or not k.GetVolumePathNameW(str(probe), root, len(root)) or not k.GetVolumeInformationW(root.value, None, 0, ct.byref(serial), ct.byref(limit), ct.byref(flags), fs, len(fs)):
        raise ValueError(f"C2_A_VOLUME_UNVERIFIABLE: {origin}; winerror={ct.get_last_error()}")
    if fs.value != "NTFS" or k.GetDriveTypeW(root.value) != 3:
        raise ValueError(f"C2_A_DECISION_REQUIRED: local fixed NTFS required, actual={fs.value!r}; {origin}")
    canonical = lexical.resolve(strict=not allow_missing)
    if ws is not None and not canonical.is_relative_to(Path(ws).resolve()):
        raise ValueError(f"C2_A_ESCAPE: canonical target: {origin}: {value!r}")
    _no_reparse(probe)
    info = None if missing else canonical.stat()
    if info is not None and ((kind == "file" and not stat.S_ISREG(info.st_mode)) or (kind == "dir" and not stat.S_ISDIR(info.st_mode))):
        raise ValueError(f"C2_A_WRONG_KIND: {origin}: expected {kind}: {value!r}")
    if info is not None and stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
        raise ValueError(f"C2_A_DECISION_REQUIRED: hardlink/alias count={info.st_nlink}: {origin}: {value!r}")
    identity = None if info is None else (info.st_dev, info.st_ino)
    if info is not None and not info.st_ino:
        raise ValueError(f"C2_A_IDENTITY_UNVERIFIABLE: {origin}: {value!r}")
    event = dict(raw=value, origin=origin, lexical=str(lexical), canonical=canonical,
                 identity=identity, fingerprint=None if info is None else
                 (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns),
                 ancestors=observations, volume=serial.value, filesystem=fs.value)
    events = _PATH_SOURCES.get()
    if events is not None:
        for previous in events:
            if previous.get("canonical") == canonical and previous.get("identity") != identity:
                raise ValueError(f"C2_A_IDENTITY_CHANGED: {origin}: {value!r}")
            if previous.get("canonical") == canonical and previous.get("fingerprint") != event["fingerprint"]:
                raise ValueError(f"C2_A_SOURCE_CHANGED: {origin}: {value!r}")
            if identity and previous.get("identity") == identity and previous.get("canonical") != canonical:
                raise ValueError(f"C2_A_ALIAS_AMBIGUITY: {origin}: {value!r}")
        events.append(event)  # retain every origin, including equivalent spelling
    return event

def _read_source(ws, value, origin):
    before = _path_record(ws, str(value), origin)
    with before["canonical"].open("rb") as stream:
        a = os.fstat(stream.fileno())
        data = stream.read()
        b = os.fstat(stream.fileno())
    after = _path_record(ws, str(value), origin + " [after read]")
    # Windows stat/fstat ctime may use different underlying time semantics.
    # Compare ctime within each API, and common identity/size/mtime across APIs.
    fingerprint = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    if before["fingerprint"][:4] != fingerprint(a) or fingerprint(a) != fingerprint(b) or a.st_ctime_ns != b.st_ctime_ns or before["fingerprint"] != after["fingerprint"] or len(data) != b.st_size:
        raise ValueError(f"C2_A_SOURCE_CHANGED_DURING_READ: {origin}: {value!r}")
    # This detects sampled changes; no deny-write handle or ABA guarantee is claimed.
    return data.decode("utf-8")


def source_path(ws, value, problems, label):
    try:
        return _path_record(ws, value, label)["canonical"]
    except (OSError, ValueError, RuntimeError) as exc:
        problems.append(str(exc))
        return None


def passed_audit(path):
    if not path.is_file():
        return False
    match = VERDICT.search(path.read_text(encoding="utf-8"))
    return bool(match and match.group(1).upper() in {"PASS", "PASSED"})


def waiver_is_human(ws, decision_id):
    ledgers = [ws / "planning/framing_decisions.jsonl"]
    ledgers += sorted((ws / "methods").glob("Q*/q*_decisions.jsonl"))
    for ledger in ledgers:
        if not ledger.is_file():
            continue
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (row.get("decision_id") == decision_id and row.get("decided_by") == "human"
                    and row.get("status") == "DECIDED" and row.get("rationale")
                    and row.get("choice") and row.get("evidence_refs")
                    and row.get("decision_type") == "packaging_waiver"):
                return str(ledger.relative_to(ws))
    return None


def gate_evidence(ws, questions, waiver, paper, problems):
    cfg = ws / "planning/session_config.json"
    try:
        profile = read_json(cfg).get("rigor_profile")
    except (OSError, ValueError):
        profile = None
    if profile != "submission":
        problems.append("planning/session_config.json must set rigor_profile to submission")
    evidence = {}
    for qx in questions:
        path = ws / f"planning/manifests/{qx}.json"
        try:
            manifest = read_json(path)
        except (OSError, ValueError):
            manifest = {}
            problems.append(f"{qx}: unreadable planning manifest")
        if not isinstance(manifest, dict):
            manifest = {}
            problems.append(f"{qx}: planning manifest must be an object")
        ok = manifest.get("current_gate") == "G6" and manifest.get("allowed", {}).get("final_assembly") is True
        evidence[f"{qx}_G6"] = "PASS" if ok else "FAIL"
        if not ok and not waiver:
            problems.append(f"{qx}: G6/final_assembly has not passed")
    for name, rel in AUDITS.items():
        audit = ws / rel
        ok = passed_audit(audit)
        evidence[name] = "PASS" if ok else "FAIL"
        if not ok and not waiver:
            problems.append(f"{rel}: explicit Verdict: PASSED is required")
        if ok and not waiver:
            material = [paper] + [ws / f"results/{qx}/reports/frozen_numbers.json" for qx in questions]
            stale = [p for p in material if p.is_file() and p.stat().st_mtime > audit.stat().st_mtime + 2]
            if stale:
                evidence[name] = "STALE"
                problems.append(f"{rel}: newer paper or freeze requires an updated audit")
    if waiver:
        ledger = waiver_is_human(ws, waiver)
        if not ledger:
            problems.append(f"waiver {waiver}: no human DECIDED packaging_waiver with rationale")
        evidence["waiver"] = {"decision_id": waiver, "ledger": ledger}
    return evidence


def frozen_claims(ws, qx, problems):
    path = ws / f"results/{qx}/reports/frozen_numbers.json"
    if not path.is_file():
        problems.append(f"{qx}: frozen_numbers.json is missing")
        return [], None
    try:
        raw = read_json(path)
    except (OSError, ValueError):
        problems.append(f"{qx}: frozen_numbers.json is unreadable")
        return [], path
    if not isinstance(raw, (list, dict)):
        problems.append(f"{qx}: frozen_numbers.json must be a list or object")
        return [], path
    claims = raw if isinstance(raw, list) else raw.get("claims", raw.get("numbers", []))
    if not isinstance(claims, list) or not claims:
        problems.append(f"{qx}: frozen_numbers.json has no claims")
        return [], path
    rounds = set()
    for claim in claims:
        if not isinstance(claim, dict):
            problems.append(f"{qx}: malformed frozen claim")
            continue
        src = source_path(ws, claim.get("source_file"), problems, f"{qx} frozen source")
        if not src:
            continue
        parts = src.relative_to(ws).parts
        if len(parts) < 5 or parts[:3] != ("results", qx, "experiments"):
            problems.append(f"{qx}: frozen source is not in an experiment round: {src.relative_to(ws)}")
            continue
        rounds.add(parts[3])
        timestamp = claim.get("frozen_at")
        try:
            frozen_at = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if frozen_at.tzinfo is None:
                frozen_at = frozen_at.replace(tzinfo=dt.timezone.utc)
            if src.stat().st_mtime > frozen_at.timestamp() + 2:
                problems.append(f"{qx}: frozen source changed after freeze: {src.relative_to(ws)}")
        except (AttributeError, TypeError, ValueError):
            problems.append(f"{qx}: invalid frozen_at for {src.relative_to(ws)}")
        try:
            current = json_locator(src, claim.get("source_locator"))
            if current is not None and current != claim.get("value"):
                problems.append(f"{qx}: frozen value disagrees with its source: {src.relative_to(ws)}")
        except (OSError, KeyError, IndexError, TypeError, ValueError):
            problems.append(f"{qx}: frozen source locator cannot be read: {src.relative_to(ws)}")
    if len(rounds) != 1:
        problems.append(f"{qx}: frozen claims must identify one experiment round, found {sorted(rounds)}")
    return claims, path


def _matlab_lexical(text, label):
    """Narrow code/comment/string scan; offsets refer to original Unicode text."""
    code, literals, i, size, square_depth = list(text), [], 0, len(text), 0
    while i < size:
        char = text[i]
        if char == "%":
            line_start = text.rfind("\n", 0, i) + 1
            line_end = text.find("\n", i)
            line_end = size if line_end < 0 else line_end
            marker = text[line_start:line_end].strip()
            end = line_end
            if marker == "%}":
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: unmatched block close at offset {i}")
            if marker == "%{":
                cursor, closed = min(line_end + 1, size), False
                while cursor < size:
                    stop = text.find("\n", cursor)
                    stop = size if stop < 0 else stop
                    boundary = text[cursor:stop].strip()
                    if boundary == "%{":
                        raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: nested block comment at offset {cursor}")
                    if boundary == "%}":
                        end, closed = stop, True
                        break
                    cursor = min(stop + 1, size)
                if not closed:
                    raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: unclosed block comment at offset {i}")
            for pos in range(i, end):
                if text[pos] not in "\r\n":
                    code[pos] = " "
            i = end
            continue
        if char in "'\"":
            previous = i - 1
            while previous >= 0 and text[previous] in " \t":
                previous -= 1
            last = text[previous] if previous >= 0 else ""
            expression_end = bool(last) and (last.isalnum() or last in "_)]}.'\"")
            if char == "'" and expression_end:
                # Immediate A' and A.' are recognized postfix transposes only.
                if previous == i - 1 and (last.isalnum() or last in "_)]}." ):
                    i += 1
                    continue
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: ambiguous quote/transpose at offset {i}")
            if square_depth:
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: string array/concatenation at offset {i}")
            start, quote, value = i, char, []
            i += 1
            while i < size:
                if text[i] in "\r\n":
                    raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: multiline string at offset {start}")
                if text[i] == quote:
                    if i + 1 < size and text[i + 1] == quote:
                        value.append(quote)
                        i += 2
                        continue
                    i += 1
                    break
                value.append(text[i])
                i += 1
            else:
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: unclosed string at offset {start}")
            tail = i
            while tail < size and text[tail] in " \t":
                tail += 1
            if (tail < size and text[tail] == "+") or (last == "+"):
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: string expression at offset {start}")
            literals.append(("".join(value), start, i))
            for pos in range(start, i):
                code[pos] = " "
            continue
        if text.startswith("...", i):
            raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: continuation/expression at offset {i}")
        if char == "[":
            square_depth += 1
        elif char == "]":
            square_depth -= 1
            if square_depth < 0:
                raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: unmatched bracket at offset {i}")
        i += 1
    if square_depth:
        raise ValueError(f"C2_A_MATLAB_REVIEW_REQUIRED: {label}: unclosed bracket")
    return "".join(code), literals


def local_dependencies(entry, ws):
    with _path_scope():
        entry = _path_record(ws, str(entry), "dependency entry")["canonical"]
        found, queue = set(), [entry]
        probes, matlab_directories = [], []

        def probe(value, origin, kind="file", allow_missing=False):
            # Retain this finite discovery's positive AND negative probes with
            # their original arguments; _path_scope does not store allow_missing.
            record = _path_record(ws, value, origin, kind, allow_missing)
            probes.append((value, origin, kind, allow_missing, record))
            return record
        parts = entry.relative_to(ws).parts
        root = ws.joinpath(*parts[:3 if len(parts) > 2 and parts[1] == "matlab" else 2])
        _path_record(ws, str(root), "dependency code root", "dir")

        def module_files(base, dotted, origin):
            location = base.joinpath(*dotted.split(".")) if dotted else base
            if not Path(os.path.abspath(location)).is_relative_to(root):
                raise ValueError(f"C2_A_IMPORT_ESCAPE: {origin}: {dotted!r}")
            result, primary = set(), []
            for candidate in (location.with_suffix(".py"), location / "__init__.py"):
                if not Path(os.path.abspath(candidate)).is_relative_to(root):
                    continue  # a root package's sibling is not its initializer
                record = probe(str(candidate), origin, allow_missing=True)
                if record["identity"] is not None:
                    primary.append(record["canonical"])
                    result.add(record["canonical"])
            if len(set(primary)) > 1:
                raise ValueError(f"C2_A_AMBIGUOUS_LOCAL_IMPORT: module and package: {origin}")
            if not primary:
                return result  # unresolved external imports must not inherit unrelated inits
            folder = location if location.is_dir() else location.parent
            while folder.is_relative_to(root):
                record = probe(str(folder / "__init__.py"), origin + " package init", allow_missing=True)
                if record["identity"] is not None:
                    result.add(record["canonical"])
                if folder == root:
                    break
                folder = folder.parent
            return result

        while queue:
            path = queue.pop()
            if path in found:
                continue
            text = _read_source(ws, str(path), f"dependency source {path.relative_to(ws)}")
            found.add(path)
            if path.suffix == ".py":
                try:
                    tree = ast.parse(text, filename=str(path))
                except SyntaxError as exc:
                    raise ValueError(f"invalid Python source {path.relative_to(ws)}: {exc}") from exc
                # Finite, scope-conservative known API bindings, not runtime
                # object inference. Rebinding/escaping these names needs review.
                dynamic_names = {"__import__"}
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and not node.level:
                        for alias in node.names:
                            if ((node.module == "importlib" and alias.name == "import_module")
                                    or (node.module == "builtins" and alias.name == "__import__")):
                                dynamic_names.add(alias.asname or alias.name)
                            if node.module in {"importlib", "builtins"} and alias.name == "*":
                                raise ValueError(f"C2_A_DYNAMIC_IMPORT_REVIEW_REQUIRED: wildcard API binding: {path}:{node.lineno}")
                for node in ast.walk(tree):
                    related_name = (isinstance(node, ast.Name) and node.id in dynamic_names)
                    related_binding = (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in dynamic_names) or (isinstance(node, ast.arg) and node.arg in dynamic_names)
                    if related_name or related_binding or (isinstance(node, ast.Attribute) and node.attr in {"import_module", "__import__"}):
                        raise ValueError(f"C2_A_DYNAMIC_IMPORT_REVIEW_REQUIRED: known API use/rebinding: {path}:{node.lineno}")
                    if not isinstance(node, (ast.Import, ast.ImportFrom)):
                        continue
                    origin = f"Python {path.relative_to(ws)}:{node.lineno} {ast.get_source_segment(text,node)}"
                    base = path.parent
                    level = getattr(node, "level", 0)
                    for _ in range(max(level - 1, 0)):
                        base = base.parent
                    bases = (base,) if level else tuple(dict.fromkeys((path.parent, root)))
                    if isinstance(node, ast.Import):
                        search_groups = [[alias.name] for alias in node.names]
                    else:
                        names = [node.module or ""]
                        names += [f"{node.module}.{a.name}" if node.module else a.name for a in node.names if a.name != "*"]
                        search_groups = [names]  # Keep ImportFrom's base/member association.
                    for names in search_groups:
                        matches = []
                        for candidate_base in bases:
                            current = set()
                            for name in names:
                                current.update(module_files(candidate_base, name, origin))
                            if current:
                                matches.append(current)
                        if len(matches) > 1 and any(s != matches[0] for s in matches[1:]):
                            raise ValueError(f"C2_A_AMBIGUOUS_LOCAL_IMPORT: distinct search roots: {origin}; import names={names!r}")
                        if level and not matches:
                            raise ValueError(f"C2_A_MISSING_RELATIVE_IMPORT: {origin}")
                        for matches_here in matches:
                            queue.extend(matches_here - found)
                record = probe(str(path.parent / "__init__.py"), f"package initializer for {path}", allow_missing=True)
                if record["identity"] is not None:
                    queue.append(record["canonical"])
            elif path.suffix == ".m":
                executable, _ = _matlab_lexical(text, str(path))
                if (re.search(r"\b(?:eval|feval|addpath)\s*\(", executable)
                        or re.search(r"(?:^|[;,\n])\s*(?:eval|feval|addpath)\b(?!\s*=)", executable)):
                    raise ValueError(f"C2_A_DYNAMIC_MATLAB_REVIEW_REQUIRED: {path}")
                before_names = sorted(p.name for p in path.parent.glob("*.m"))
                matlab_directories.append((path.parent, before_names))
                for name in before_names:
                    sibling = path.parent / name
                    if sibling != path and re.search(rf"\b{re.escape(sibling.stem)}\s*\(", executable):
                        record = probe(str(sibling), f"MATLAB same-directory call from {path}: {sibling.stem}")
                        queue.append(record["canonical"])
                if before_names != sorted(p.name for p in path.parent.glob("*.m")):
                    raise ValueError(f"C2_A_DEPENDENCY_DIRECTORY_CHANGED: {path.parent}")
        # Bounded checkpoint consistency only: no retries, lock or ABA claim.
        for value, origin, kind, allow_missing, before in probes:
            after = _path_record(ws, value, origin + " [closure recheck]", kind, allow_missing)
            if any(before[key] != after[key] for key in ("canonical", "identity", "fingerprint", "ancestors")):
                raise ValueError(f"C2_A_DEPENDENCY_PROBE_CHANGED: {origin}: {value!r}")
        for directory, names in matlab_directories:
            if names != sorted(p.name for p in directory.glob("*.m")):
                raise ValueError(f"C2_A_DEPENDENCY_DIRECTORY_CHANGED: {directory}")
        for path in found:
            _path_record(ws, str(path), "dependency closure final identity")
        return found


def detect_literal_data(ws, script, problems):
    with _path_scope():
        found = set()
        try:
            text = _read_source(ws, str(script), f"literal-data source {script}")
            if script.suffix == ".py":
                values = [(n.value, f"Python literal {script}:{n.lineno}") for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            else:
                _, literals = _matlab_lexical(text, str(script))
                values = [(value, f"MATLAB literal {script}:offset {start} line {text.count(chr(10), 0, start) + 1} source={text[start:end]!r}")
                          for value, start, end in literals]
            for raw, origin in values:
                if not re.search(r"(?:^|[/\\])data_(?:clean|raw)(?:[/\\]|$)", raw):
                    continue
                literal = raw.replace("\\", "/")
                if not DATA_LITERAL.fullmatch(literal) or any(p in {"", ".", ".."} for p in literal.split("/")):
                    raise ValueError(f"C2_A_INVALID_DATA_LITERAL: {origin}: {raw!r}")
                candidates = [literal] if literal.startswith("workspace/") else ["workspace/" + literal, literal]
                existing = []
                for candidate in candidates:
                    record = _path_record(ws, candidate, origin + f" raw={raw!r}", allow_missing=True)
                    if record["identity"] is not None:
                        existing.append(record["canonical"])
                if len(set(existing)) > 1:
                    raise ValueError(f"C2_A_AMBIGUOUS_DATA_LITERAL: {origin}: {raw!r}")
                if not existing:
                    raise ValueError(f"C2_A_MISSING_DATA_LITERAL: {origin}: {raw!r}")
                found.update(existing)
        except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
            problems.append(str(exc))
        return found


def listed_files(ws, value, problems, label):
    paths = set()
    for item in strings(value):
        path = source_path(ws, item, problems, label)
        if path:
            paths.add(path)
    return paths


def _strict_json(text):
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError(f"duplicate JSON key: {key}")
            obj[key] = value
        return obj
    def constant(value):
        raise ValueError(f"nonfinite JSON literal: {value}")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def _no_reparse(path):
    # Check lexical ancestors before resolve() can hide a link/junction.
    for node in [path] + list(path.parents):
        attrs = node.lstat().st_file_attributes
        if attrs & 0x400:
            raise ValueError(f"C2: reparse ancestor or file is unsupported: {node}")


def _declared_path(ws, value):
    if (not isinstance(value, str) or not value or "\\" in value
            or ":" in value or any(ord(c) < 32 for c in value)
            or Path(value).is_absolute() or any(p in {"", ".", ".."} for p in value.split("/"))):
        raise ValueError(f"invalid workspace-relative POSIX path: {value!r}")
    return _path_record(ws, value, "declared plan/evidence path")["canonical"]


def _evidence_file(ws, qx, value, dependencies):
    path = _declared_path(ws, value)
    rel = path.relative_to(ws).as_posix()
    roots = (f"code/{qx}/", f"code/matlab/{qx}/", f"methods/{qx}/",
             f"results/{qx}/", f"robustness/{qx}/", "workspace/data_clean/", "paper/")
    if not (rel.startswith(roots) or rel == "planning/framing_decisions.jsonl"):
        raise ValueError(f"outside this question's evidence read scope: {value}")
    dependencies.add(path)
    return path


def _plan_table(text, heading, headers):
    # Narrow visibility scan only: never parse examples inside fenced code.
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            lines.append(None)
        elif marker:
            if marker[1][0] == "`" and "`" in marker[2]:
                raise ValueError("ambiguous plan code fence; representation review required")
            fence = (marker[1][0], len(marker[1]))
            lines.append(None)
        else:
            lines.append(line)
    if fence is not None:
        raise ValueError("unclosed plan code fence; representation review required")
    if lines.count(heading) != 1:
        raise ValueError(f"missing/duplicate authoritative heading {heading}")
    if headers is None:
        return []  # The same visibility rules validate the unique plan title.
    start = lines.index(heading) + 1
    end = next((i for i in range(start, len(lines)) if lines[i] is not None
                and re.match(r" {0,3}#{1,6}(?:[ \t]+|$)", lines[i])), len(lines))
    section = lines[start:end]
    table = [line for line in section if line is not None and line.startswith("|")]
    if len(table) < 2 or table[0] != "| " + " | ".join(headers) + " |":
        raise ValueError(f"noncanonical headers at {heading}")
    if table[1] != "| " + " | ".join(["---"] * len(headers)) + " |":
        raise ValueError(f"noncanonical separator at {heading}")
    positions = [i for i, line in enumerate(section) if line is not None and line.startswith("|")]
    if positions != list(range(positions[0], positions[-1] + 1)):
        raise ValueError(f"multiple/ambiguous tables at {heading}")
    rows = []
    for line in table[2:]:
        if not line.endswith("|"):
            raise ValueError(f"unterminated physical table row at {heading}")
        cells = [c.strip(" ") for c in line[1:-1].split("|")]
        if len(cells) != len(headers):
            raise ValueError(f"wrong column count at {heading}")
        values = [_strict_json(c) for c in cells]
        if any(isinstance(v, dict) for v in values):
            raise ValueError("object-valued plan cells are unsupported")
        rows.append(dict(zip(headers, values)))
    return rows


def parse_confirmed_plan(text):
    categories = ["Required Main Model", "Required Baseline",
                  "Required Validation Experiments", "Non-required Exploratory Methods"]
    _plan_table(text, "# Code Plan Contents", None)
    metadata = _plan_table(text, "## Plan Identity", ["key", "value"])
    keys = {"question", "implementation_target", "round", "round_purpose", "plan_revision",
            "decision_id", "confirmation_status", "random_seed", "dependencies", "expected_runtime", "review_checks"}
    if any(not isinstance(r["key"], str) for r in metadata):
        raise ValueError("metadata key must be a string")
    if len(metadata) != len(keys) or {r["key"] for r in metadata} != keys:
        raise ValueError("missing/duplicate/unknown metadata key")
    meta = {r["key"]: r["value"] for r in metadata}
    def strings_array(value, nonempty=False):
        return (isinstance(value, list) and (bool(value) or not nonempty)
                and all(isinstance(x, str) and bool(x) for x in value)
                and len(set(value)) == len(value))
    for key, value in meta.items():
        valid = (type(value) is int if key == "random_seed" else
                 strings_array(value) if key in {"dependencies", "review_checks"} else
                 isinstance(value, str) and bool(value))
        if not valid:
            raise ValueError(f"invalid metadata type: {key}")
    cats = _plan_table(text, "## Four-Category Inventory and Acceptance", ["category", "applicability", "item_ids", "reason"])
    if [r["category"] for r in cats] != categories:
        raise ValueError("four ordered category declarations required")
    for index, row in enumerate(cats):
        if not strings_array(row["item_ids"]) or not isinstance(row["reason"], str) or not row["reason"]:
            raise ValueError("invalid category IDs/reason")
        mode = row["applicability"]
        if index < 2:
            valid = mode == "applicable" and bool(row["item_ids"])
        else:
            valid = ((mode == "applicable" and bool(row["item_ids"])) or
                     (mode == ("not_applicable" if index == 2 else "none_authorized") and row["item_ids"] == []))
        if not valid:
            raise ValueError("invalid applicability or empty required inventory")
    fields = "method_id validation_id role requiredness task_ids objective script input_files data_requirements output_files expected_outputs success_criteria execution_conditions failure_impact evidence_artifacts".split()
    rows = _plan_table(text, "### Work Items", fields)
    inventory = {}
    arrays = {"task_ids", "input_files", "data_requirements", "output_files", "expected_outputs", "execution_conditions", "evidence_artifacts"}
    role_map = dict(zip(categories, ["main", "usable_baseline", "validation", "exploratory"]))
    for row in rows:
        mid, vid = row["method_id"], row["validation_id"]
        if not ((isinstance(mid, str) and mid and vid is None) or (isinstance(vid, str) and vid and mid is None)):
            raise ValueError("exactly one method_id/validation_id required")
        item_id = mid if mid is not None else vid
        if item_id in inventory or any(ord(c) < 32 for c in item_id):
            raise ValueError(f"duplicate or illegal plan ID: {item_id}")
        if row["role"] not in categories or (vid is not None) != (row["role"] == categories[2]):
            raise ValueError(f"identity/category conflict: {item_id}")
        if row["requiredness"] != ("non-required" if row["role"] == categories[3] else "required"):
            raise ValueError(f"explicit requiredness conflict: {item_id}")
        for field in fields[4:]:
            value = row[field]
            valid = strings_array(value, field in {"task_ids", "evidence_artifacts"}) if field in arrays else isinstance(value, str) and bool(value)
            if not valid:
                raise ValueError(f"missing/invalid plan field {item_id}.{field}")
        if any(any(ord(c) < 32 for c in task) for task in row["task_ids"]):
            raise ValueError(f"control character in original-task identity: {item_id}")
        # Empty arrays are legal representations, not proof of applicability.
        if not row["input_files"] and (not row["data_requirements"] or not row["execution_conditions"]):
            raise ValueError(f"{item_id}: empty input_files lacks explicit data/generation conditions; manual applicability review required")
        if not row["output_files"] and (not row["expected_outputs"] or not row["execution_conditions"]):
            raise ValueError(f"{item_id}: empty output_files lacks a documented output design; manual applicability review required")
        inventory[item_id] = dict(row, run_role=role_map[row["role"]])
    for row in cats:
        if set(row["item_ids"]) != {k for k, r in inventory.items() if r["role"] == row["category"]}:
            raise ValueError(f"category/Work Items inventory mismatch: {row['category']}")
    vfields = "validation_id validation_target applicability applicability_reason design data_requirements metrics success_criteria execution_conditions failure_impact evidence_artifacts".split()
    validations = _plan_table(text, "## Required Validation Experiments", vfields)
    seen = set()
    for row in validations:
        item_id = row["validation_id"]
        if not isinstance(item_id, str) or item_id in seen or item_id not in inventory or inventory[item_id]["run_role"] != "validation":
            raise ValueError("missing/duplicate/unmatched validation row")
        seen.add(item_id)
        for field in vfields[1:]:
            value = row[field]
            is_array = field in {"design", "data_requirements", "metrics", "execution_conditions", "evidence_artifacts"}
            if not (strings_array(value, field in {"design", "metrics", "evidence_artifacts"}) if is_array else isinstance(value, str) and bool(value)):
                raise ValueError(f"invalid validation field {item_id}.{field}")
            if field in inventory[item_id] and inventory[item_id][field] != value:
                raise ValueError(f"cross-table conflict {item_id}.{field}")
        if row["applicability"] != "applicable":
            raise ValueError("included required validation is not applicable")
    if seen != {k for k, row in inventory.items() if row["run_role"] == "validation"}:
        raise ValueError("missing required validation design")
    return meta, inventory, validations


def run_summary_file_view(ws, summary, qx, problems):
    """File view only: no successful completeness or authorization verdict."""
    top_paths = {}
    for field in ("scripts", "inputs", "outputs"):
        if field in summary:
            top_paths[field] = set()
            for value in strings(summary[field]):
                try:
                    top_paths[field].add(_path_record(ws, value, f"{qx} top-level {field}: {value!r}")["canonical"])
                except (OSError, ValueError, RuntimeError) as exc:
                    problems.append(f"{qx}: top-level {field} source {value!r}: {exc}")
    if "methods" not in summary:
        if str(summary.get("status", "")).upper() not in GOOD or summary.get("failures") or summary.get("errors"):
            problems.append(f"{qx}: frozen round summary did not complete successfully")
        return summary
    if "schema_version" not in summary:
        problems.append(f"{qx}: COMPATIBILITY_GAP: unversioned methods summary lacks historical-contract evidence")
    elif type(summary["schema_version"]) is not int or summary["schema_version"] != 1:
        problems.append(f"{qx}: unsupported methods schema_version {summary['schema_version']!r}")
    methods = summary.get("methods")
    view = {"scripts": [], "inputs": [], "outputs": []}
    if not isinstance(methods, list) or not methods:
        problems.append(f"{qx}: methods must be a nonempty array")
        return view
    seen, failed = set(), False
    method_paths = {"scripts": set(), "inputs": set(), "outputs": set()}
    for i, row in enumerate(methods):
        label = f"{qx} methods[{i}]"
        if not isinstance(row, dict):
            problems.append(f"{label}: not an object")
            continue
        item_id = row.get("method_id")
        if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
            problems.append(f"{label}: missing/duplicate method_id {item_id!r}")
        else:
            seen.add(item_id)
        if row.get("role") not in ("main", "usable_baseline", "validation", "exploratory"):
            problems.append(f"{label}: unknown role {row.get('role')!r}")
        status = row.get("status")
        if status not in ("success", "failed"):
            problems.append(f"{label}: illegal/unknown method status {status!r}")
        failed = failed or status == "failed"
        errors = row.get("errors")
        if not isinstance(errors, list) or any(not isinstance(x, str) or not x for x in errors):
            problems.append(f"{label}: errors must be actual nonempty-string array entries")
        elif status == "failed" and not errors:
            problems.append(f"{label}: failed lacks formed genuine error record")
        elif status == "success" and errors:
            problems.append(f"{label}: success conflicts with errors")
        if row.get("failures"):
            problems.append(f"{label}: unresolved legacy failures")
        script = row.get("script")
        if not isinstance(script, str) or not script.strip():
            problems.append(f"{label}: missing/invalid script")
        else:
            view["scripts"].append(script)
            try:
                method_paths["scripts"].add(_declared_path(ws, script))
                _path_record(ws, script, f"{label}.script: {script!r}")
            except (OSError, ValueError, RuntimeError) as exc:
                problems.append(f"{label}.script source {script!r}: {exc}")
        for source, target in [("input_files", "inputs"), ("output_files", "outputs"), ("figure_files", "outputs")]:
            paths = row.get(source)
            if not isinstance(paths, list) or any(not isinstance(x, str) or not x for x in paths):
                problems.append(f"{label}: {source} must be an explicit path array")
            else:
                view[target].extend(paths)
                for value in paths:
                    try:
                        method_paths[target].add(_declared_path(ws, value))
                        _path_record(ws, value, f"{label}.{source}: {value!r}")
                    except (OSError, ValueError, RuntimeError) as exc:
                        problems.append(f"{label}.{source} source {value!r}: {exc}")
    if summary.get("errors") or summary.get("failures"):
        problems.append(f"{qx}: unresolved top-level errors/failures (not discarded)")
    if "status" in summary and (not isinstance(summary["status"], str) or summary["status"].upper() not in GOOD or failed):
        problems.append(f"{qx}: top-level failure, unknown status or method/top-level conflict")
    for field in ("scripts", "inputs", "outputs"):
        if field in summary:
            if not isinstance(summary[field], (str, list, dict)):
                problems.append(f"{qx}: unsupported top-level {field} type")
            declared = top_paths[field]
            derived = method_paths[field]
            if declared != derived:
                problems.append(f"{qx}: top-level {field} conflicts with methods paths")
    return view


def confirmed_plan_inventory(ws, qx, round_name, summary, problems, dependencies):
    """Bounded structural/evidence checks; does not certify human origin or math."""
    if summary.get("question") != qx or summary.get("round") != round_name:
        problems.append(f"{qx}: summary question/frozen-round identity conflict")
        return None
    language = summary.get("implementation_target")
    if language not in ("python", "matlab"):
        problems.append(f"{qx}: plan language/authority cannot be determined")
        return None
    rel = f"code/{qx}/{qx.lower()}_code_plan.md" if language == "python" else f"code/matlab/{qx}/{qx.lower()}_code_plan.md"
    try:
        plan = _evidence_file(ws, qx, rel, dependencies)
        current_bytes = plan.read_bytes()
        meta, inventory, validations = parse_confirmed_plan(current_bytes.decode("utf-8"))
        if (meta["question"], meta["implementation_target"], meta["round"]) != (qx, language, round_name):
            raise ValueError("current plan question/language/round mismatch")
        item_evidence = {}
        for item_id, row in inventory.items():
            item_evidence[item_id] = []
            for field in ("script", "input_files", "evidence_artifacts"):
                values = [row[field]] if field == "script" else row[field]
                for value in values:
                    try:
                        path = _evidence_file(ws, qx, value, dependencies)
                        if field == "evidence_artifacts":
                            item_evidence[item_id].append(value)
                            if not path.stat().st_size:
                                problems.append(f"{qx}: BLOCKING_ERROR ITEM_EVIDENCE_EMPTY: {item_id} {value}")
                    except (OSError, ValueError) as exc:
                        problems.append(f"{qx}: BLOCKING_ERROR ITEM_EVIDENCE_UNVERIFIABLE: {item_id}.{field}: {exc}")
            if not row["input_files"] or not row["output_files"]:
                # Existing prose/paths have no approved machine-readable semantic verdict.
                problems.append(f"{qx}: BLOCKING_ERROR EMPTY_FILE_APPLICABILITY_REVIEW_REQUIRED: {item_id} empty input/output is structurally representable, but its actual no-external-input/no-separate-output design, generation conditions and current human approval require attributable review; nonempty prose alone is not proof")
        ledger = _evidence_file(ws, qx, f"methods/{qx}/{qx.lower()}_decisions.jsonl", dependencies)
        records = [_strict_json(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
        if any(not isinstance(row, dict) for row in records):
            raise ValueError("Ledger line is not an object")
        ids = [r.get("decision_id") for r in records]
        if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
            raise ValueError("duplicate/invalid Ledger decision_id")
        for row in records:
            sup = row.get("supersedes")
            if sup is not None and (sup not in ids or sup == row["decision_id"]):
                raise ValueError("unverifiable supersession reference")
        for row in records:
            trail, current = set(), row
            while current.get("supersedes") is not None:
                if current["decision_id"] in trail:
                    raise ValueError("cyclic supersession")
                trail.add(current["decision_id"])
                current = records[ids.index(current["supersedes"])]
        removed = {r["supersedes"] for r in records if r.get("supersedes") is not None}
        choices = [r for r in records if r.get("decision_type") == "code_plan_confirmation" and r["decision_id"] not in removed]
        if not any(r.get("decision_type") == "method_choice" and r["decision_id"] == meta["decision_id"] and r["decision_id"] not in removed and r.get("status") == "DECIDED" and r.get("decided_by") == "human" for r in records):
            problems.append(f"{qx}: G2.5 method-choice evidence missing/unverifiable")
        if len(choices) != 1:
            raise ValueError("current full-plan confirmation missing or conflicting (fallback/method choice is not confirmation)")
        choice = choices[0]
        required = {"schema_version", "decision_id", "decision_type", "status", "decided_by", "captured_in_mode", "choice", "rationale", "evidence_refs", "decided_at", "supersedes"}
        if not required.issubset(choice) or type(choice["schema_version"]) is not int or choice["schema_version"] != 1:
            raise ValueError("incomplete confirmation structure")
        if choice["status"] != "DECIDED" or choice["decided_by"] != "human" or choice["captured_in_mode"] not in ("learning", "speed"):
            raise ValueError("confirmation is not a genuine supported human DECIDED record")
        if any(not isinstance(choice[k], str) or not choice[k].strip() for k in ["choice", "rationale", "decided_at"]):
            raise ValueError("missing actual confirmation wording/reason/time")
        dt.datetime.fromisoformat(choice["decided_at"].replace("Z", "+00:00"))
        refs = choice["evidence_refs"]
        if not isinstance(refs, list) or not refs or any(not isinstance(p, str) or not p for p in refs):
            raise ValueError("confirmation lacks real evidence references")
        material = [_evidence_file(ws, qx, p, dependencies) for p in refs]
        history = [p for p in material if p != plan and p.read_bytes() == current_bytes]
        # A preserved exact snapshot is one content representation, not the only
        # legal one. Digest wording may be in any existing permitted evidence.
        # Finding a matching token does NOT prove when it was recorded or by whom.
        binding_texts = [choice["choice"], choice["rationale"]]
        binding_texts.extend(p.read_text(encoding="utf-8", errors="replace") for p in material if p != plan)
        recorded_digest_candidate = any(re.search(r"(?<![0-9a-fA-F])" + digest(current_bytes) + r"(?![0-9a-fA-F])", value, re.I)
                                        for value in binding_texts)
        if not history:
            detail = ("a matching digest occurs in existing evidence but its contemporaneous full-content binding is unverified"
                      if recorded_digest_candidate else "immutable revision or other historical full-content evidence has no supported deterministic binding")
            problems.append(f"{qx}: BLOCKING_ERROR CONTENT_PROVENANCE_REVIEW_REQUIRED: {detail}; a current hash, mutable path or revision label cannot establish historical approval")
        if any(r.get("decision_type") == "decision_stale" for r in records):
            problems.append(f"{qx}: staleness relation needs scoped provenance review; not auto-reactivated")
        if any(r.get("decision_type") not in {"framing", "method_choice", "fallback_activation", "result_verdict", "stability_verdict", "assumption_necessity", "claim_scope", "package_signoff", "submission_authorization", "code_plan_confirmation", "decision_stale", "packaging_waiver"} for r in records):
            problems.append(f"{qx}: unknown decision/revocation effect requires authority review")
        # No new reply envelope, signature fields or mathematical-acceptance DSL is authorized.
        problems.append(f"{qx}: BLOCKING_ERROR AUTHENTICITY_REVIEW_REQUIRED: readable files/human flags/digest do not independently authenticate human origin or approval scope")
        actual = {r.get("method_id"): r for r in summary.get("methods", []) if isinstance(r, dict)}
        for item_id in inventory.keys() - actual.keys():
            problems.append(f"{qx}: missing planned run evidence for {item_id}; absent record does not prove non-execution")
        for item_id in actual.keys() - inventory.keys():
            problems.append(f"{qx}: run {item_id!r} lacks current-plan authorization (no fallback substitution)")
        for item_id in inventory.keys() & actual.keys():
            planned, ran = inventory[item_id], actual[item_id]
            if ran.get("role") != planned["run_role"] or ran.get("script") != planned["script"] or ran.get("input_files") != planned["input_files"]:
                problems.append(f"{qx}: STRUCTURE_CONFLICT: {item_id} plan/run identity, role, script or inputs conflict")
            outputs = ran.get("output_files")
            figures = ran.get("figure_files")
            valid_outputs = (isinstance(outputs, list) and isinstance(figures, list)
                             and all(isinstance(p, str) for p in outputs + figures))
            actual_outputs = set(outputs + figures) if valid_outputs else set()
            planned_outputs = set(planned["output_files"])
            if not valid_outputs or not actual_outputs.issubset(planned_outputs):
                problems.append(f"{qx}: {item_id} output scope is unverifiable")
            if planned["requiredness"] == "required":
                if ran.get("status") != "success":
                    problems.append(f"{qx}: EXECUTION_RECORD_UNSUCCESSFUL: required {item_id} did not execute successfully; the actual record is {ran.get('status')!r}, not an inferred NOT RUN or mathematical verdict")
                if not valid_outputs or planned_outputs != actual_outputs:
                    problems.append(f"{qx}: required {item_id} lacks expected real outputs")
                evidence = item_evidence[item_id]
                problems.append(f"{qx}: BLOCKING_ERROR EXECUTION_EVIDENCE_REVIEW_REQUIRED: {item_id} status={ran.get('status')!r}; readable planned evidence={evidence!r}; record/file presence alone does not verify actual execution, script/input lineage or evidence attribution")
                if planned["run_role"] == "validation":
                    problems.append(f"{qx}: BLOCKING_ERROR VALIDATION_ACCEPTANCE_REVIEW_REQUIRED: validation_id={item_id}; actual per-item metrics/outputs, confirmed criteria and attributable current review are required; an overall Reviewer PASS cannot certify this validation")
                problems.append(f"{qx}: BLOCKING_ERROR ACCEPTANCE_REVIEW_REQUIRED: {item_id} independent Reviewer/human assessment of current confirmed criteria and scope remains unresolved; no mathematical or scientific PASS inferred")
            elif ran.get("status") == "failed":
                problems.append(f"{qx}: optional failure {item_id} retained; failure provenance/material disclosure needs review, not automatic G6 failure")
        return dict(meta=meta, inventory=inventory, validations=validations, structural_confirmation_id=choice["decision_id"])
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as exc:
        problems.append(f"{qx}: BLOCKING_ERROR PLAN_OR_AUTHORITY_UNVERIFIABLE: {exc}")
        return None


class WindowsReadWindow:
    """Candidate primitive only, not yet a qualified packaging safety mechanism."""
    def __init__(self, ws, paths):
        self.ws, self.paths, self.handles, self.identities = ws, set(paths), [], {}

    def __enter__(self):
        import ctypes as ct
        from ctypes import wintypes as wt
        if sys.platform != "win32":
            raise ValueError("C2 unsupported platform; no ordinary-open fallback")
        self.ct, self.wt = ct, wt
        k = self.k = ct.WinDLL("kernel32", use_last_error=True)
        k.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, wt.LPVOID, wt.DWORD, wt.DWORD, wt.HANDLE]
        k.CreateFileW.restype = wt.HANDLE
        k.CloseHandle.argtypes = [wt.HANDLE]; k.CloseHandle.restype = wt.BOOL
        class Info(ct.Structure):
            _fields_ = [("attributes", wt.DWORD), ("created", wt.FILETIME), ("accessed", wt.FILETIME), ("written", wt.FILETIME), ("volume", wt.DWORD), ("size_hi", wt.DWORD), ("size_lo", wt.DWORD), ("links", wt.DWORD), ("index_hi", wt.DWORD), ("index_lo", wt.DWORD)]
        self.Info = Info
        k.GetFileInformationByHandle.argtypes = [wt.HANDLE, ct.POINTER(Info)]; k.GetFileInformationByHandle.restype = wt.BOOL
        k.GetVolumePathNameW.argtypes = [wt.LPCWSTR, wt.LPWSTR, wt.DWORD]; k.GetVolumePathNameW.restype = wt.BOOL
        k.GetVolumeInformationW.argtypes = [wt.LPCWSTR, wt.LPWSTR, wt.DWORD, ct.POINTER(wt.DWORD), ct.POINTER(wt.DWORD), ct.POINTER(wt.DWORD), wt.LPWSTR, wt.DWORD]; k.GetVolumeInformationW.restype = wt.BOOL
        k.GetDriveTypeW.argtypes = [wt.LPCWSTR]; k.GetDriveTypeW.restype = wt.UINT
        try:
            _no_reparse(self.ws)
            root, name, fs = ct.create_unicode_buffer(1024), ct.create_unicode_buffer(1024), ct.create_unicode_buffer(1024)
            serial, limit, flags = wt.DWORD(), wt.DWORD(), wt.DWORD()
            if not k.GetVolumePathNameW(str(self.ws), root, len(root)) or not k.GetVolumeInformationW(root.value, name, len(name), ct.byref(serial), ct.byref(limit), ct.byref(flags), fs, len(fs)):
                raise ct.WinError(ct.get_last_error())
            if fs.value != "NTFS" or k.GetDriveTypeW(root.value) != 3:
                raise ValueError("C2 requires verified local NTFS; no unsupported-filesystem fallback")
            self.volume = serial.value
            for path in sorted(self.paths):
                _no_reparse(path)
                if not path.is_relative_to(self.ws):
                    raise ValueError(f"C2 source escapes workspace: {path}")
                handle = k.CreateFileW(str(path), 0x80000000, 1, None, 3, 0x80, None)
                if handle == ct.c_void_p(-1).value:
                    raise ct.WinError(ct.get_last_error())
                self.handles.append(handle)
                info = self._info(handle)
                if info[0] != self.volume or info[2] != 1:
                    raise ValueError("C2 cross-volume or hardlink-alias identity unsupported")
                self.identities[path] = info
            return self
        except BaseException:
            self.close()
            raise

    def _info(self, handle):
        data = self.Info()
        if not self.k.GetFileInformationByHandle(handle, self.ct.byref(data)):
            raise self.ct.WinError(self.ct.get_last_error())
        return data.volume, (data.index_hi << 32) | data.index_lo, data.links

    def verify(self, snapshot):
        expected = {self.ws / row["source"] for row in snapshot["files"]}
        if expected != self.paths:
            raise ValueError("C2 dependency set changed after protection")
        for row in snapshot["files"]:
            path = self.ws / row["source"]
            _no_reparse(path)
            handle = self.k.CreateFileW(str(path), 0x80000000, 1, None, 3, 0x80, None)
            if handle == self.ct.c_void_p(-1).value:
                raise self.ct.WinError(self.ct.get_last_error())
            try:
                if self._info(handle) != self.identities[path]:
                    raise ValueError(f"C2 path/file identity changed: {path}")
            finally:
                self.k.CloseHandle(handle)
            if file_hash(path) != row["sha256"]:
                raise ValueError(f"C2 content changed: {path}")

    def close(self):
        failures = []
        for handle in reversed(self.handles):
            if not self.k.CloseHandle(handle):
                failures.append(self.ct.get_last_error())
        self.handles.clear()
        if failures:
            raise ValueError(f"C2 CloseHandle failed: {failures}")

    def __exit__(self, kind, value, trace):
        self.close()


@contextlib.contextmanager
def protected_package_plan(ws, paper, out, waiver):
    discovered = plan_package(ws, paper, out, waiver)
    summary_paths = [ws / row["source"] for row in discovered[0]["files"] if Path(row["source"]).name == "run_summary.json"]
    method_level = False
    for path in summary_paths:
        try:
            record = _strict_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # question_files already recorded the unreadable source.
        method_level = method_level or (isinstance(record, dict) and "methods" in record)
    if not method_level:
        # Legacy package selection, CLI and return behavior are preserved.
        yield (*discovered, None)
        return
    paths = {ws / row["source"] for row in discovered[0]["files"]}
    with WindowsReadWindow(ws, paths) as window:
        current = plan_package(ws, paper, out, waiver)
        if current[0] != discovered[0]:
            raise ValueError("C2 discovery changed before protected reread; stop and rediscover explicitly")
        window.verify(current[0])
        # Explicit deployment gate: real reparse fixtures, raw alias provenance and
        # the whole publish lifecycle have not been qualified. No bypass flag.
        current[3].append("BLOCKING_ERROR C2_UNQUALIFIED: candidate protected window is not certified for publication; no unsafe fallback")
        yield (*current, window)


def question_files(ws, qx, claims, problems, evidence_dependencies=None):
    with _path_scope():
        dependencies = evidence_dependencies if evidence_dependencies is not None else set()
        rounds = set()
        frozen_sources = set()
        for claim in claims:
            if not isinstance(claim, dict) or not claim.get("source_file"):
                continue
            src = source_path(ws, claim["source_file"], problems, f"{qx} frozen source")
            if src:
                frozen_sources.add(src)
                parts = src.relative_to(ws).parts
                if len(parts) >= 4 and parts[:3] == ("results", qx, "experiments"):
                    rounds.add(parts[3])
        if len(rounds) != 1:
            return set(), None, None
        round_name = next(iter(rounds))
        summary_path = ws / f"results/{qx}/experiments/{round_name}/run_summary.json"
        if not summary_path.is_file():
            problems.append(f"{qx}: {summary_path.relative_to(ws)} is missing")
            return set(), round_name, None
        try:
            summary = _strict_json(_read_source(ws, str(summary_path), f"{qx} frozen run-summary source"))
        except (OSError, ValueError):
            problems.append(f"{qx}: frozen round run_summary.json is unreadable")
            return frozen_sources, round_name, summary_path
        if not isinstance(summary, dict):
            problems.append(f"{qx}: frozen round run_summary.json must be an object")
            return frozen_sources, round_name, summary_path
        if "methods" in summary:
            dependencies.add(summary_path)
            file_view = run_summary_file_view(ws, summary, qx, problems)
            confirmed_plan_inventory(ws, qx, round_name, summary, problems, dependencies)
            for item in strings(file_view):
                try:
                    _declared_path(ws, item)
                except (OSError, ValueError) as exc:
                    problems.append(f"{qx}: method path: {exc}")
        else:
            file_view = summary
            if str(summary.get("status", "")).upper() not in GOOD or summary.get("failures") or summary.get("errors"):
                problems.append(f"{qx}: frozen round {round_name} did not complete successfully")
        scripts = listed_files(ws, file_view.get("scripts"), problems, f"{qx} scripts")
        if not scripts:
            problems.append(f"{qx}: final run_summary.json must list its scripts")
        allowed_code = {_path_record(ws, value, f"{qx} allowed code root", "dir", True)["canonical"]
                        for value in (f"code/{qx}", f"code/matlab/{qx}")}
        for script in scripts:
            if script.suffix not in {".py", ".m"} or not any(script.is_relative_to(root) for root in allowed_code):
                problems.append(f"{qx}: script must be Python/MATLAB under code/{qx}: {script.relative_to(ws)}")
        inputs = listed_files(ws, file_view.get("inputs"), problems, f"{qx} inputs")
        outputs = listed_files(ws, file_view.get("outputs"), problems, f"{qx} outputs")
        round_root = _path_record(ws, str(summary_path.parent), f"{qx} frozen round root", "dir")["canonical"]
        for output in outputs | frozen_sources:
            if not output.is_relative_to(round_root):
                problems.append(f"{qx}: output does not belong to frozen round: {output.relative_to(ws)}")
        closure = set()
        for script in scripts:
            if script.suffix in {".py", ".m"} and script.is_file():
                try:
                    closure.update(local_dependencies(script, ws))
                except ValueError as exc:
                    problems.append(str(exc))
        for script in closure:
            inputs.update(detect_literal_data(ws, script, problems))
        for path in inputs:
            if path.is_relative_to(round_root) or path in closure:
                problems.append(f"{qx}: input overlaps an output or script: {path.relative_to(ws)}")
        return closure | inputs | outputs | frozen_sources, round_name, summary_path


def paper_files(ws, paper, problems):
    with _path_scope():
        try:
            text = _read_source(ws, str(paper), "paper Markdown source")
        except (OSError, UnicodeError, ValueError):
            problems.append(f"paper Markdown cannot be read as UTF-8: {paper}")
            return "", set()
        if len(re.findall(r"!\[[^\]]*\]\(", text)) != len(list(IMAGE.finditer(text))):
            problems.append("paper contains image syntax that the packager cannot resolve")
        if re.search(r"<img\b", text, re.I):
            problems.append("paper contains HTML images; use Markdown image references before packaging")
        assets = set()

        def replace(match):
            original = match.group(2)
            value = unquote(original.strip("<>"))
            if value.startswith(("http://", "https://", "data:")):
                return match.group(0)
            src = source_path(ws, str(paper.parent / value), problems, f"paper image raw={original!r}")
            if not src:
                return match.group(0)
            assets.add(src)
            rel = src.relative_to(ws)
            target = Path("支撑材料") / rel
            return match.group(1) + target.as_posix() + match.group(3)

        text = IMAGE.sub(replace, text)
        text = TEX_IMAGE.sub(replace, text)
        return text, assets


def plan_package(ws, paper, out, waiver):
    with _path_scope():
        problems = []
        evidence_dependencies = set()
        _path_record(None, str(ws), "plan workspace root", "dir")
        _path_record(ws, "planning/manifests", "manifest discovery directory", "dir", True)
        manifests = sorted((ws / "planning/manifests").glob("Q*.json"))
        for manifest_path in manifests:
            _path_record(ws, str(manifest_path), "manifest discovery entry")
        questions = [path.stem for path in manifests]
        if not questions:
            problems.append("no planning/manifests/Q*.json found")
        # Path-only preflight: leave Gate and waiver decisions unchanged.
        preflight = ["planning/session_config.json", *AUDITS.values()]
        preflight += [f"results/{qx}/reports/frozen_numbers.json" for qx in questions]
        for value in preflight:
            _path_record(ws, value, "existing planning/audit/freeze source", allow_missing=True)
        gate = gate_evidence(ws, questions, waiver, paper, problems)
        if not paper.is_file() or not paper.is_relative_to(ws):
            problems.append("paper Markdown is missing or outside workspace")
            rendered, images = "", set()
        else:
            rendered, images = paper_files(ws, paper, problems)
        files = set(images)
        copied = set(images)
        evidence_paths = [ws / "planning/session_config.json"]
        evidence_paths += manifests
        evidence_paths += [ws / rel for rel in AUDITS.values()]
        if isinstance(gate.get("waiver"), dict) and gate["waiver"].get("ledger"):
            evidence_paths.append(ws / gate["waiver"]["ledger"])
        files.update(path for path in evidence_paths if path.is_file())
        rounds = {}
        frozen_paths = {}
        for qx in questions:
            claims, frozen = frozen_claims(ws, qx, problems)
            if frozen:
                frozen_paths[qx] = str(frozen.relative_to(ws))
                files.add(frozen)
            selected, round_name, summary = question_files(ws, qx, claims, problems, evidence_dependencies)
            files.update(selected)
            copied.update(selected)
            if summary:
                files.add(summary)
            rounds[qx] = round_name
        files.update(evidence_dependencies)
        for path in evidence_dependencies & copied:
            rel = path.relative_to(ws)
            if rel.parts[0] == "methods" or "logs" in rel.parts or path.name.endswith("_code_plan.md"):
                problems.append(f"evidence-only source conflicts with copy selection: {rel}")
        if evidence_dependencies:
            for path in files:
                if path.suffix == ".json":
                    try:
                        _strict_json(path.read_text(encoding="utf-8"))
                    except (ValueError, UnicodeError, OSError) as exc:
                        problems.append(f"method-level JSON evidence invalid: {path}: {exc}")
        if paper.is_file() and paper.is_relative_to(ws):
            files.add(paper)
        for path in files:
            _path_record(ws, str(path), "selected-source identity preflight")
        records = [{"source": str(path.relative_to(ws)), "sha256": file_hash(path), "copy": path in copied}
                   for path in sorted(files)]
        snapshot = {"paper": str(paper.relative_to(ws)) if paper.is_relative_to(ws) else str(paper),
                    "rendered_paper_sha256": digest(rendered.encode("utf-8")), "files": records,
                    "rounds": rounds, "frozen_paths": frozen_paths, "gate": gate,
                    "waiver": waiver, "output": str(out)}
        plan_hash = digest(json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode("utf-8"))
        return snapshot, plan_hash, rendered, problems


def json_locator(source, locator):
    if not isinstance(locator, str) or not locator.startswith("$.") or source.suffix.lower() != ".json":
        return None
    value = read_json(source)
    for token in re.findall(r"[^.\[\]]+|\[\d+\]", locator[2:]):
        value = value[int(token[1:-1])] if token.startswith("[") else value[token]
    return value


def verify_runtime(staging, commands, claims_by_question, atol, rtol):
    if not commands:
        return {"status": "UNVERIFIED", "reason": "no reproduction command supplied"}
    for claims in claims_by_question.values():
        for claim in claims:
            if isinstance(claim, dict) and claim.get("source_file"):
                source = staging / "支撑材料" / claim["source_file"]
                if source.is_file():
                    source.unlink()
    results = []
    for command in commands:
        parts = shlex.split(command)
        if not parts:
            return {"status": "FAIL", "reason": "empty reproduction command"}
        if parts[0] in {"python", "python3"}:
            parts[0] = sys.executable
        proc = subprocess.run(parts, cwd=staging / "支撑材料", text=True, capture_output=True, timeout=600)
        results.append({"command": command, "returncode": proc.returncode,
                        "stderr": proc.stderr[-2000:]})
        if proc.returncode:
            return {"status": "FAIL", "runs": results}
    checks = []
    for qx, claims in claims_by_question.items():
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            src = staging / "支撑材料" / claim["source_file"]
            if not src.is_file():
                checks.append({"claim": claim.get("claim_id"), "status": "FAIL",
                               "reason": "reproduction did not create the frozen source"})
                continue
            try:
                value = json_locator(src, claim.get("source_locator"))
            except (OSError, KeyError, IndexError, ValueError, TypeError):
                value = None
            expected = claim.get("value")
            if value is None or expected is None:
                checks.append({"claim": claim.get("claim_id"), "status": "UNVERIFIED"})
            elif isinstance(value, (int, float)) and isinstance(expected, (int, float)):
                ok = abs(value - expected) <= atol + rtol * abs(expected)
                checks.append({"claim": claim.get("claim_id"), "status": "PASS" if ok else "FAIL",
                               "actual": value, "expected": expected})
            else:
                checks.append({"claim": claim.get("claim_id"), "status": "PASS" if value == expected else "FAIL",
                               "actual": value, "expected": expected})
    status = "PASS" if checks and all(x["status"] == "PASS" for x in checks) else (
        "FAIL" if any(x["status"] == "FAIL" for x in checks) else "UNVERIFIED")
    return {"status": status, "runs": results, "claims": checks}


def safe_output(ws, out, snapshot, force, problems):
    if out == ws or ws.is_relative_to(out):
        problems.append("output cannot equal or contain the workspace")
    for protected in ("workspace/data_raw", "workspace/data_clean", "code", "results",
                      "paper", "planning", "methods", "robustness"):
        if out.is_relative_to(ws / protected):
            problems.append(f"output cannot be inside protected workspace directory: {protected}")
            break
    for row in snapshot["files"]:
        src = ws / row["source"]
        if src.is_relative_to(out):
            problems.append(f"output contains a selected source: {row['source']}")
            break
    if out.exists():
        manifest = ws / "planning/submission_packaging_manifest.json"
        if not force or not manifest.is_file():
            problems.append("output already exists; --force requires a prior package manifest")
        else:
            try:
                previous = read_json(manifest)
            except (OSError, ValueError):
                previous = {}
                problems.append("previous package manifest is unreadable")
            if not isinstance(previous, dict):
                previous = {}
                problems.append("previous package manifest must be an object")
            if previous.get("output") != str(out):
                problems.append("existing output is not the package recorded by the manifest")
            elif ({str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()}
                  != set(previous.get("package_files", {}))
                  or any(not (out / rel).is_file() or file_hash(out / rel) != sha
                         for rel, sha in previous.get("package_files", {}).items())):
                problems.append("existing package changed since its manifest; refusing replacement")
    if out.is_symlink():
        problems.append("output cannot be a symlink")


def assemble(ws, out, snapshot, rendered, commands, atol, rtol, _window=None):
    raise ValueError("C2_UNQUALIFIED: all assembly and publication are disabled in this restricted candidate")
    if _window is not None:
        _window.verify(snapshot)
        raise ValueError("C2_UNQUALIFIED: method-level publication is disabled in this candidate")
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".submission-stage-", dir=out.parent))
    backup = None
    try:
        support = staging / "支撑材料"
        support.mkdir()
        for row in snapshot["files"]:
            src = ws / row["source"]
            if file_hash(src) != row["sha256"]:
                raise ValueError(f"source changed after planning: {row['source']}")
            if not row["copy"]:
                continue
            dest = support / row["source"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        paper_name = Path(snapshot["paper"]).name
        (staging / paper_name).write_text(rendered, encoding="utf-8")
        for py in support.rglob("*.py"):
            compile(py.read_bytes(), str(py), "exec")
        claims_by_question = {}
        for qx, path in snapshot["frozen_paths"].items():
            data = read_json(ws / path)
            claims_by_question[qx] = data if isinstance(data, list) else data.get("claims", data.get("numbers", []))
        runtime = verify_runtime(staging, commands, claims_by_question, atol, rtol)
        if runtime["status"] == "FAIL":
            raise ValueError("packaged reproduction failed or disagreed with frozen claims")
        package_files = {str(p.relative_to(staging)): file_hash(p) for p in staging.rglob("*") if p.is_file()}
        if _window is not None:
            _window.verify(snapshot)
        if out.exists():
            backup = Path(tempfile.mkdtemp(prefix=".submission-backup-", dir=out.parent))
            backup.rmdir()
            out.rename(backup)
        try:
            staging.rename(out)
        except Exception:
            if backup:
                backup.rename(out)
            raise
        if backup:
            shutil.rmtree(backup)
        return package_files, runtime
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main():
    with _path_scope():
        ap = argparse.ArgumentParser(description=__doc__)
        ap.add_argument("--workspace", type=Path, default=Path("."))
        ap.add_argument("--paper", type=Path, default=Path("paper/main.md"))
        ap.add_argument("--out", type=Path)
        ap.add_argument("--confirm", help="SHA-256 plan digest from a reviewed dry run")
        ap.add_argument("--dry-run", action="store_true", help="print the plan without writing; also the default")
        ap.add_argument("--force", action="store_true")
        ap.add_argument("--allow-unaudited", metavar="DECISION_ID")
        ap.add_argument("--verify-command", action="append", default=[], help="reproduction command run from packaged support directory")
        ap.add_argument("--atol", type=float, default=0.0)
        ap.add_argument("--rtol", type=float, default=0.0)
        args = ap.parse_args()
        if args.dry_run and args.confirm:
            ap.error("--dry-run and --confirm cannot be used together")
        # Preserve exact CLI tokens as well as argparse's Path representation.
        raw_paths = {}
        tokens = sys.argv[1:]
        for index, token in enumerate(tokens):
            flag, equal, value = token.partition("=")
            matches = [key for key in ("--workspace", "--paper", "--out") if flag.startswith("--") and key.startswith(flag)]
            if len(matches) == 1:
                raw_paths[matches[0]] = value if equal else tokens[index + 1]
        try:
            ws = _path_record(None, raw_paths.get("--workspace", str(args.workspace)), "CLI --workspace", "dir")["canonical"]
            out = _path_record(None, raw_paths.get("--out", str(args.out or ws / "submission")), "CLI --out (provenance only; publication unqualified)", "any", True)["canonical"]
            paper = _path_record(ws, raw_paths.get("--paper", str(args.paper)), "CLI --paper")["canonical"]
        except (OSError, ValueError) as exc:
            print(f"BLOCKED: {exc}", file=sys.stderr)
            return 1
        if not ws.is_dir():
            ap.error(f"workspace not found: {ws}")
        if args.atol < 0 or args.rtol < 0:
            ap.error("tolerances must be nonnegative")
        try:
            with protected_package_plan(ws, paper, out, args.allow_unaudited) as (snapshot, plan_hash, rendered, problems, window):
                safe_output(ws, out, snapshot, args.force, problems)
                print(f"output: {out}\nplan: {plan_hash}")
                for row in snapshot["files"]:
                    if row["copy"]:
                        print(f"  {row['source']} -> 支撑材料/{row['source']}")
                    else:
                        print(f"  evidence only (not copied): {row['source']} sha256={row['sha256']}")
                print(f"  {snapshot['paper']} -> {Path(snapshot['paper']).name} (image links updated)")
                for issue in problems:
                    print(f"BLOCKED: {issue}")
                if problems:
                    return 1
                if not args.confirm:
                    print("dry run; review the list, then pass --confirm with the plan digest")
                    return 0
                if args.confirm != plan_hash:
                    print("BLOCKED: plan changed since confirmation", file=sys.stderr)
                    return 1
                try:
                    package_files, runtime = assemble(ws, out, snapshot, rendered, args.verify_command, args.atol, args.rtol, _window=window)
                except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                    print(f"BLOCKED: {exc}", file=sys.stderr)
                    return 1
                manifest = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "workspace": str(ws),
                            "output": str(out), "plan_digest": plan_hash, "plan": snapshot,
                            "package_files": package_files, "runtime": runtime}
                target = ws / "planning/submission_packaging_manifest.json"
                target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"package: {out}\nmanifest: {target}\nruntime: {runtime['status']}")
                return 0
        except (OSError, ValueError) as exc:
            print(f"BLOCKED: {exc}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
