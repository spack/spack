# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShadow3(PythonPackage):
    """SHADOW is an open source ray tracing code for modeling optical systems.
    Targeted to synchrotron radiation beamlines, it has unique features for
    designing X-ray optical systems.
    """

    homepage = "https://github.com/oasys-kit/shadow3"
    url = "https://files.pythonhosted.org/packages/11/29/c330f8ed5fa1d77927105bb6884a928d74ac9ec89e03181f3084a6cdb361/shadow3-23.9.19-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    maintainers("luccabavia")

    version("23.9.19", sha256=("d06920433552526398fd1373df03264a65dcdf020c0a67e196ac6f78f8673867"))

    depends_on("py-setuptools", type="build")
