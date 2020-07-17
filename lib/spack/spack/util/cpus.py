# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import multiprocessing


def cpus_available():
    if platform.system() == 'Linux':
        try:
            return len(os.sched_getaffinity(0))  # novermin
        except Exception:
            pass

    return multiprocessing.cpu_count()
