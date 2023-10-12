# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import multiprocessing
import os
from typing import Optional


def cpus_available():
    """
    Returns the number of CPUs available for the current process, or the number
    of phyiscal CPUs when that information cannot be retrieved. The number
    of available CPUs might differ from the number of physical CPUs when
    using spack through Slurm or container runtimes.
    """
    try:
        return len(os.sched_getaffinity(0))  # novermin
    except Exception:
        return multiprocessing.cpu_count()


def determine_number_of_jobs(
    *,
    parallel: bool = False,
    max_cpus: int = cpus_available(),
    config: Optional["spack.config.Configuration"] = None,
    config_path: str = 'config:build_jobs',
) -> int:
    """
    Packages that require sequential builds need 1 job. Otherwise we use the
    number of jobs set on the command line. If not set, then we use the config
    defaults (which is usually set through the builtin config scope), but we
    cap to the number of CPUs available to avoid oversubscription.

    Parameters:
        parallel: true when package supports parallel builds
        max_cpus: maximum number of CPUs to use (defaults to cpus_available())
        config: configuration object (defaults to global config)
        config_path: configuration path to read number of jobs from
    """
    if not parallel:
        return 1

    # Command line overrides all
    config_jobs = 16
    try:
        command_line = None
        if config is not None:
            command_line = config.get(config_path, default=None, scope="command_line")

        if command_line is not None:
            return command_line
    except ValueError:
        pass

    if config is not None:
        config_jobs = config.get(config_path, 16)

    return min(max_cpus, config_jobs)
