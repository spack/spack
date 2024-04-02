# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDcm2bids(PythonPackage):
    """Reorganising NIfTI files from dcm2niix into the Brain Imaging Data
    Structure."""

    homepage = "https://github.com/unfmontreal/Dcm2Bids"
    pypi = "dcm2bids/dcm2bids-2.1.9.tar.gz"

    license("GPL-3.0-only")

    version(
        "3.1.0",
        sha256="4262d9739ec567fb167fa8995a9a0423783bcedb2ce436ed234f332d7f44bb57",
        url="https://pypi.org/packages/24/00/e8ca836232e25254af2810e091d4dc806f8d37b966b9846f00d026a3faae/dcm2bids-3.1.0-py3-none-any.whl",
    )
    version(
        "2.1.9",
        sha256="45346f76d659b92c1fd19d2b511b86870a5907b5012c22a777273f16f35a7b94",
        url="https://pypi.org/packages/21/62/11f5f6ef133ac2da911755513a0a82374e8819feb33992bb1cc8db34587d/dcm2bids-2.1.9-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.1.7:")
        depends_on("py-future@0.17.1:", when="@2.1.5:2")
        depends_on("py-packaging@23.1:", when="@3:")

    # Historical dependencies
