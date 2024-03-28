# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHeapdict(PythonPackage):
    """A heap with decrease-key and increase-key operations"""

    homepage = "http://stutzbachenterprises.com/"
    pypi = "HeapDict/HeapDict-1.0.1.tar.gz"

    version(
        "1.0.1",
        sha256="6065f90933ab1bb7e50db403b90cab653c853690c5992e69294c2de2b253fc92",
        url="https://pypi.org/packages/b6/9d/cd4777dbcf3bef9d9627e0fe4bc43d2e294b1baeb01d0422399d5e9de319/HeapDict-1.0.1-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="f7e4858afe3465d4693280c5ebd542d4e105eca98210d68ea8594fd501e81807",
        url="https://pypi.org/packages/ac/aa/867f3493599247eebb239588b030d7928fe6474d4454c45770aa78951164/HeapDict-1.0.0-py3-none-any.whl",
    )
