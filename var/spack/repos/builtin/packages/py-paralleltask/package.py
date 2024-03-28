# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParalleltask(PythonPackage):
    """Paralleltask is a simple and lightweight parallel task engine. It can launch a given
    number of tasks from a batch of independent tasks, and keep this number of running tasks
    until all tasks are completed."""

    homepage = "https://github.com/moold/ParallelTask"
    pypi = "Paralleltask/Paralleltask-0.2.2.tar.gz"

    license("GPL-3.0-only")

    version(
        "0.2.2",
        sha256="2a067f7a696883d77e8eee6f4a19499f11856147476f823fd83512e134723fe5",
        url="https://pypi.org/packages/52/76/e2e56a4b0785063baf06852459c4f63e38e9831cbe4bf696865123aa03de/Paralleltask-0.2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-psutil")
