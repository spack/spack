# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIsaRwval(PythonPackage):
    """Metadata tracking tools help to manage an increasingly diverse set
    of life science, environmental and biomedical experiments
    """

    homepage = "https://github.com/ISA-tools/isa-rwval"
    pypi = "isa-rwval/isa-rwval-0.10.10.tar.gz"

    version(
        "0.10.10",
        sha256="772b336ff24f501483a09bc8158571ef61fdb1122a7e911c524455f7030dde47",
        url="https://pypi.org/packages/7c/8a/8393799b83529a7d791e2bc909f5081883c3431bce18c84feee771fa3f4b/isa_rwval-0.10.10-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-networkx@2.5:2.5.0", when="@0.10.10:")
