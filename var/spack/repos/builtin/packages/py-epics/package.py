# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEpics(PythonPackage):
    """EPICS channel access for python. A thin layer of abstraction
    for libca with some tools built above it.

    You can learn more about EPICS here: https://epics-controls.org/resources-and-support/documents/getting-started/
    """

    homepage = "http://pyepics.github.io/pyepics/"
    url = "https://files.pythonhosted.org/packages/6c/cd/f97b676b6903e6f88bfced3817964559c20a1e3c6cd5244fa188f76fff75/pyepics-3.5.1.tar.gz"

    maintainers("MarcoMontevechiFilho1")

    version("3.5.1", sha256="a4d0f2d0d163aa34a53f560519f5664a42ba96aeb19bbf92e46228f22fa87ff6")

    depends_on("py-setuptools", type="build")
