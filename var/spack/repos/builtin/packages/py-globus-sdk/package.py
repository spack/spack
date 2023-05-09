# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlobusSdk(PythonPackage):
    """
    Globus SDK for Python
    """

    homepage = "https://github.com/globus/globus-sdk-python"
    pypi = "globus-sdk/globus-sdk-3.0.2.tar.gz"

    maintainers("hategan")

    version("3.10.1", sha256="c20fec55fc7e099f4d0c8224a36e194604577539445c5985cb465b23779baee8")
    version("3.10.0", sha256="7a7e7cd5cfbc40c6dc75bdb92b050c4191f992b5f7081cd08895bf119fd97bbf")
    version("3.9.0", sha256="456f707b25a8c502607134f1d699b5970ef1aa9d17877474db73fc6d87c711e9")
    version("3.8.0", sha256="492611636c190806409198cdadc9960227fa712281dce95ef3ec0d7e8f9823a9")
    version("3.7.0", sha256="81dbcb7bb7072bf9a5f730becc65e4a0f15f0fa0e2022faf2d943a99b5ce1fb5")
    version("3.0.2", sha256="765b577b37edac70c513179607f1c09de7b287baa855165c9dd68de076d67f16")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.19.1:2", type=("build", "run"))
    depends_on("py-pyjwt@2.0.0:2+crypto", type=("build", "run"))
    depends_on("py-cryptography@3.3.1:3.3,3.4.1:", when="@3.7:", type=("build", "run"))
    depends_on("py-cryptography@2:3.3,3.4.1:3.6", when="@:3.0", type=("build", "run"))
