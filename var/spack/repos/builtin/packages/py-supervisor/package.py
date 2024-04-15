# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySupervisor(PythonPackage):
    """A system for controlling process state under UNIX"""

    homepage = "http://supervisord.org"
    pypi = "supervisor/supervisor-4.2.4.tar.gz"

    version(
        "4.2.4",
        sha256="bbae57abf74e078fe0ecc9f30068b6da41b840546e233ef1e659a12e4c875af6",
        url="https://pypi.org/packages/3d/47/b4030b2b01f6c559bd528974cee72bee7fe75594b31cc3e064678a454548/supervisor-4.2.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-setuptools", when="@4.2.3:")
