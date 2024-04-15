# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThewalrus(PythonPackage):
    """A library for the calculation of hafnians, Hermite polynomials and
    Gaussian boson sampling.
    """

    homepage = "https://github.com/XanaduAI/thewalrus"
    pypi = "thewalrus/thewalrus-0.19.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.19.0",
        sha256="07b6e2969bf5405a2df736c442b1500857438bbd2afc2053b8b600b8b0c67f97",
        url="https://pypi.org/packages/92/ec/aec87db2151afd4527b119f524203f8631d3c2457a127c8d1ed4ce9f59a9/thewalrus-0.19.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-dask+delayed", when="@:0.13.0-rc1,0.18:0.19,0.21:")
        depends_on("py-numba@0.49.1:", when="@0.19,0.21:")
        depends_on("py-numpy@1.19.2:", when="@0.18:0.19,0.21:")
        depends_on("py-scipy@1.2.1:", when="@:0.13.0-rc1,0.18:0.19,0.21:")
        depends_on("py-sympy@1.5.1:", when="@:0.13.0-rc1,0.18:0.19,0.21:")
