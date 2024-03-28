# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyJobMetrics(PythonPackage):
    """The Galaxy job metrics framework and default plugins."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-job-metrics/galaxy-job-metrics-22.1.1.tar.gz"

    license("CC-BY-3.0")

    version(
        "22.1.1",
        sha256="ab37fbfd3b792c5751f984565fe52026eaa8425046df16fc879b6c6860a9ab03",
        url="https://pypi.org/packages/29/cf/ee35c158179eab845b16903b26cdfc874440d106d64f567f704153f188b2/galaxy_job_metrics-22.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-galaxy-util")
