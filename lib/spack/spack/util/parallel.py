# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import concurrent.futures
import sys
from typing import Optional

from spack.util.cpus import cpus_available

#: Used in tests to disable parallelism, as tests themselves are parallelized
ENABLE_PARALLELISM = sys.platform != "win32"


class SequentialExecutor(concurrent.futures.Executor):
    """Executor that runs tasks sequentially in the current thread."""

    def submit(self, fn, *args, **kwargs):
        """Submit a function to be executed."""
        future = concurrent.futures.Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as e:
            future.set_exception(e)
        return future


def make_concurrent_executor(
    jobs: Optional[int] = None, *, serialize_env: bool = False
) -> concurrent.futures.Executor:
    """Create a concurrent executor.

    If serialize_env is False (default), the active Spack environment is not transmitted to the
    worker processes, which avoids the cost of pickling potentially large environment state."""

    if not ENABLE_PARALLELISM or sys.version_info[:2] == (3, 6):
        return SequentialExecutor()

    from spack.subprocess_context import GlobalStateMarshaler

    jobs = jobs or min(cpus_available(), 16)
    marshaler = GlobalStateMarshaler(serialize_env=serialize_env)
    return concurrent.futures.ProcessPoolExecutor(jobs, initializer=marshaler.restore)  # novermin
