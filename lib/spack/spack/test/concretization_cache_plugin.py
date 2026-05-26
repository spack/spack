# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Opt-in pytest plugin that gives the test suite a persistent concretization cache.

Enable with ``--spack-concretization-cache=DIR`` or by setting the
``SPACK_TEST_CONCRETIZATION_CACHE`` environment variable. The mock configuration most
tests run under then enables Spack's concretization cache in DIR, so any ASP problem
that was already solved -- earlier in the run, by another xdist worker, or in a previous
pytest invocation -- skips clingo entirely. The solver dominates test suite CPU time and
roughly half of its problems are repeats, so a warm cache cuts wall time substantially.

Entries are keyed by the entire solver input (the ASP problem plus the .lp control
files), so changes to packages, configuration, or the concretizer miss the cache instead
of returning stale results: one directory can safely be shared across branches,
worktrees, and CI runs. Hit/miss statistics are printed at the end of the run. Works
serially and under pytest-xdist.
"""

import functools
import os
from typing import Optional, Tuple

import spack.solver.asp

_stats = {"hits": 0, "misses": 0}

#: Absolute path of the cache directory, or None when the plugin is disabled
_cache_dir: Optional[str] = None

#: Number of cache entries on disk when the session started
_initial_entries = 0


def cache_dir(config) -> Optional[str]:
    """Absolute path of the persistent concretization cache, or None when disabled.

    ``~`` and environment variables are expanded, so DIR can be given as e.g.
    ``${RUNNER_TEMP}/cache`` and stay correct on Windows, where the temporary directory
    lives on a different drive."""
    path = config.getoption("--spack-concretization-cache")
    if not path:
        return None
    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))


def pytest_addoption(parser):
    group = parser.getgroup("Spack specific command line options")
    group.addoption(
        "--spack-concretization-cache",
        action="store",
        default=os.environ.get("SPACK_TEST_CONCRETIZATION_CACHE"),
        metavar="DIR",
        help="enable a persistent concretization cache in DIR: tests whose concretization "
        "problem was already solved by an earlier test or pytest invocation skip the solver "
        "entirely. Entries are keyed by the full solver input, so DIR can be shared across "
        "branches and CI runs. ~ and environment variables in DIR are expanded "
        "(default: $SPACK_TEST_CONCRETIZATION_CACHE)",
    )


def pytest_configure(config):
    global _cache_dir, _initial_entries
    _cache_dir = cache_dir(config)
    if _cache_dir is None:
        return
    os.makedirs(_cache_dir, exist_ok=True)
    _initial_entries, _ = _scan(_cache_dir)
    _count_lookups(spack.solver.asp.ConcretizationCache)


def _count_lookups(cache_cls):
    """Wrap ConcretizationCache.fetch to count cache hits and misses."""
    original = cache_cls.fetch
    if getattr(original, "_spack_cache_counted", False):
        return

    @functools.wraps(original)
    def fetch(self, *args, **kwargs):
        result, statistics = original(self, *args, **kwargs)
        _stats["hits" if result is not None else "misses"] += 1
        return result, statistics

    fetch._spack_cache_counted = True  # ty: ignore[unresolved-attribute]
    cache_cls.fetch = fetch


def _scan(root: str) -> Tuple[int, int]:
    """Return the entry count and total size in bytes of the cache directory."""
    entries, size = 0, 0
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            # dotfiles are in-flight temporary files, not entries
            if name.startswith("."):
                continue
            try:
                size += os.stat(os.path.join(dirpath, name)).st_size
            except OSError:
                continue
            entries += 1
    return entries, size


def pytest_sessionfinish(session):
    # xdist worker: ship this process's counters to the controller
    workeroutput = getattr(session.config, "workeroutput", None)
    if workeroutput is not None and _cache_dir is not None:
        workeroutput["spack_concretization_cache_stats"] = _stats


def pytest_testnodedown(node, error):
    # xdist controller: add the counters of a finished worker
    stats = getattr(node, "workeroutput", {}).get("spack_concretization_cache_stats")
    if stats is not None:
        _stats["hits"] += stats["hits"]
        _stats["misses"] += stats["misses"]


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if _cache_dir is None:
        return
    lookups = _stats["hits"] + _stats["misses"]
    hit_rate = 100.0 * _stats["hits"] / lookups if lookups else 0.0
    entries, size = _scan(_cache_dir)
    tr = terminalreporter
    tr.write_sep("=", "spack concretization cache")
    tr.write_line(f"directory: {_cache_dir} ({entries} entries, {size / 1e6:.1f} MB)")
    tr.write_line(
        f"this run: {_stats['hits']} hits / {lookups} lookups ({hit_rate:.0f}%), "
        f"{entries - _initial_entries} entries added"
    )
