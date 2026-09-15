# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Coverage in multiprocessing children, enabled only for tests marked ``child_coverage``."""

import contextlib
import multiprocessing.process
import os
from multiprocessing import spawn
from typing import Any, Dict, Iterator

_bootstrap = getattr(multiprocessing.process.BaseProcess, "_bootstrap")
_get_preparation_data = spawn.get_preparation_data


class ChildCoverage:
    """Starts coverage in children; pickled into spawn and forkserver children to do the same."""

    def __init__(self, root: str, config_file: str) -> None:
        self.root = root
        self.config_file = config_file

    def __getstate__(self) -> Dict[str, str]:
        return {"root": self.root, "config_file": self.config_file}

    def __setstate__(self, state: Dict[str, str]) -> None:
        self.__dict__.update(state)
        self.enable()

    def enable(self) -> None:
        settings = self

        def bootstrap(process, *args, **kwargs):
            import coverage  # type: ignore

            # relative source and data paths are resolved at start
            cwd = os.getcwd()
            os.chdir(settings.root)
            try:
                cov = coverage.Coverage(config_file=settings.config_file, data_suffix=True)
                cov._warn_no_data = False
                cov._warn_unimported_source = False
                cov._warn_preimported_source = False
                cov.start()
            finally:
                os.chdir(cwd)
            try:
                return _bootstrap(process, *args, **kwargs)
            finally:
                cov.stop()
                cov.save()

        def get_preparation_data(name: str) -> Dict[str, Any]:
            data = _get_preparation_data(name)
            data["spack_child_coverage"] = settings
            return data

        setattr(multiprocessing.process.BaseProcess, "_bootstrap", bootstrap)
        setattr(spawn, "get_preparation_data", get_preparation_data)


def disable() -> None:
    setattr(multiprocessing.process.BaseProcess, "_bootstrap", _bootstrap)
    setattr(spawn, "get_preparation_data", _get_preparation_data)


@contextlib.contextmanager
def enabled(root: str) -> Iterator[None]:
    """Measure coverage in children started in this context, if coverage is running."""
    try:
        import coverage
    except ImportError:
        cov = None
    else:
        cov = coverage.Coverage.current()
    if cov is None or not cov.config.config_file:
        yield
        return
    ChildCoverage(root, os.path.join(root, cov.config.config_file)).enable()
    try:
        yield
    finally:
        disable()
