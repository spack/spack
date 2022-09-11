# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyValideer(PythonPackage):
    """Lightweight data validation and adaptation library for Python."""

    homepage = "https://github.com/podio/valideer"
    pypi = "valideer/valideer-0.4.2.tar.gz"

    version("0.4.2", sha256="4b997751d514e9c8990321bf46c09b3b15c398472dae3ef993e2e0f72fe82596")

    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
