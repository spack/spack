# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMmtfPython(PythonPackage):
    """The macromolecular transmission format (MMTF) is a binary encoding of
    biological structures."""

    homepage = "https://github.com/rcsb/mmtf-python"
    pypi = "mmtf-python/mmtf-python-1.1.2.tar.gz"

    license("Apache-2.0")

    version(
        "1.1.2",
        sha256="a00136e9798e84f58f509a8bc341834e497169c1079bd757c12bc1a4ce736b57",
        url="https://pypi.org/packages/af/d2/aabefd607ff89e35704574205b382a351f531885cc98bfd91baaf192a9fe/mmtf_python-1.1.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-msgpack@0.5.6:", when="@1.1.2")
