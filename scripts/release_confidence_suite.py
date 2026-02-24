#!/usr/bin/env python3
"""Tiny release confidence suite for Rijwal IDE/server APIs.
Fails with non-zero exit code if any required check fails.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ide_server


def check(name: str, fn: Callable[[], None]) -> Tuple[str, bool, str]:
    try:
        fn()
        return (name, True, "ok")
    except Exception as exc:  # noqa: BLE001
        return (name, False, str(exc))


def main() -> int:
    client = ide_server.app.test_client()
    results: List[Tuple[str, bool, str]] = []

    def assert_true(cond: bool, msg: str) -> None:
        if not cond:
            raise AssertionError(msg)

    def t_health() -> None:
        r = client.get('/api/health')
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, 'health success=false')
        assert_true(bool(j.get('mission')), 'mission missing in health')

    def t_docs() -> None:
        r = client.get('/api/docs')
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(bool(j.get('mission')), 'mission missing in docs')
        assert_true(isinstance(j.get('builtin_functions'), list), 'builtin_functions missing')

    def t_execute() -> None:
        r = client.post('/api/execute', json={'code': 'When Program Starts:\n    Print "suite"'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"execute failed: {j}")
        assert_true('suite' in (j.get('output') or []), f"unexpected output: {j.get('output')}")


    def t_cloud_execute() -> None:
        r = client.post('/api/cloud/execute', json={'code': 'When Program Starts:\n    Print "cloud"', 'filename': 'job.rjwl'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"cloud execute failed: {j}")
        assert_true('cloud' in (j.get('output') or []), f"unexpected cloud output: {j.get('output')}")

    def t_compile() -> None:
        r = client.post('/api/compile', json={'code': 'When Program Starts:\n    Let x = 2\n    Print x'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"compile failed: {j}")
        assert_true('python_code' in j and 'def main' in j['python_code'], 'python_code missing')
        assert_true(isinstance(j.get('ir'), list), 'ir missing')

    def t_export() -> None:
        r = client.post('/api/export/executable', json={'name': 'suite_export', 'code': 'When Program Starts:\n    Print "export"'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"export failed: {j}")
        assert_true(bool(j.get('path')), 'export path missing')

    def t_terminal() -> None:
        help_r = client.post('/api/terminal', json={'command': 'help', 'code': ''})
        help_j = help_r.get_json() or {}
        assert_true(help_r.status_code == 200, f"status={help_r.status_code}")
        assert_true(help_j.get('success') is True, f"terminal help failed: {help_j}")

        run_r = client.post('/api/terminal', json={'command': 'run', 'code': 'When Program Starts:\n    Print "term"'})
        run_j = run_r.get_json() or {}
        assert_true(run_r.status_code == 200, f"status={run_r.status_code}")
        assert_true(run_j.get('success') is True, f"terminal run failed: {run_j}")
        assert_true('term' in (run_j.get('output') or []), f"terminal output bad: {run_j.get('output')}")

    def t_ai_assist() -> None:
        r = client.post('/api/ai-assist', json={'prompt': 'help me', 'code': 'Print "x"'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"ai assist failed: {j}")
        assert_true(bool(j.get('response')), 'ai response empty')

    def t_evolve() -> None:
        r = client.post('/api/evolve', json={'goals': 'next generation roadmap', 'code': 'Print "x"'})
        j = r.get_json() or {}
        assert_true(r.status_code == 200, f"status={r.status_code}")
        assert_true(j.get('success') is True, f"evolve failed: {j}")
        assert_true(bool(j.get('plan')), 'plan empty')
        assert_true(bool(j.get('mission')), 'mission missing in evolve')

    for name, fn in [
        ('health', t_health),
        ('docs', t_docs),
        ('execute', t_execute),
        ('cloud_execute', t_cloud_execute),
        ('compile', t_compile),
        ('export', t_export),
        ('terminal', t_terminal),
        ('ai_assist', t_ai_assist),
        ('evolve', t_evolve),
    ]:
        results.append(check(name, fn))

    has_fail = False
    for name, ok, detail in results:
        prefix = 'PASS' if ok else 'FAIL'
        print(f"[{prefix}] {name}: {detail}")
        has_fail = has_fail or (not ok)

    if has_fail:
        print('\nRelease confidence suite FAILED. Refuse release.')
        return 1

    print('\nRelease confidence suite PASSED. Safe to release.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
