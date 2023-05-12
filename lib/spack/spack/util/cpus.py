# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import multiprocessing
import os

import spack.config


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
    parallel=False, command_line=None, config_default=None, max_cpus=None
):
    """
    Packages that require sequential builds need 1 job. Otherwise we use the
    number of jobs set on the command line. If not set, then we use the config
    defaults (which is usually set through the builtin config scope), but we
    cap to the number of CPUs available to avoid oversubscription.

    Parameters:
        parallel (bool or None): true when package supports parallel builds
        command_line (int or None): command line override
        config_default (int or None): config default number of jobs
        max_cpus (int or None): maximum number of CPUs available. When None, this
            value is automatically determined.
    """
    if not parallel:
        return 1

    if command_line is not None:
        return command_line
    elif "command_line" in spack.config.scopes():
        command_line = spack.config.get("config:build_jobs", scope="command_line")

    max_cpus = max_cpus or cpus_available()

    # in some rare cases _builtin config may not be set, so default to max 16
    config_default = config_default or spack.config.get("config:build_jobs", 16)

    return min(max_cpus, config_default)
