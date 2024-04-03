# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIrpf90(PythonPackage):
    """IRPF90 is a Fortran90 preprocessor written in Python for programming
    using the Implicit Reference to Parameters (IRP) method. It simplifies the
    development of large fortran codes in the field of scientific high
    performance computing."""

    homepage = "http://irpf90.ups-tlse.fr"
    pypi = "irpf90/irpf90-2.0.5.tar.gz"

    maintainers("scemama")

    version(
        "2.0.5",
        sha256="886fa2dd852d1040185f061f8ab05b3aafcf1dbc16cfff0e439fd6dcb63f1bc3",
        url="https://pypi.org/packages/a4/03/a4ce3cb0d2c934888276875ed22f73166ad4651f8f960ee5de7f4c6f22a3/irpf90-2.0.5-py3-none-any.whl",
    )
