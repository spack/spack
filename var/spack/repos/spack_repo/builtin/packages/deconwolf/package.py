# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Deconwolf(CMakePackage):
    """deconwolf is a software for 3-D deconvolution of fluorescent wide-field images."""

    homepage = "https://deconwolf.fht.org/"
    url = "https://github.com/elgw/deconwolf/archive/refs/tags/v0.4.5.tar.gz"
    git = "https://github.com/elgw/deconwolf.git"

    maintainers("dacolombo")

    license("GPL-3.0-only")

    version("0.4.5", tag="v0.4.5", commit="ca062c49eedd6bf60fcd9804df467e64cfc3c113")

    patch(
        "https://github.com/elgw/deconwolf/commit/c5f28dd3d6ef532b6963127e551da1d7b4f33f83.patch?full_index=1",
        sha256="d67096f7d2c7ddc764884e3cb09b0a6bbbca7eca5253512e73bc8d7eff89a1fc",
        when="@0.4.5",
    )

    depends_on("cmake@3.22:")
    depends_on("fftw@3")
    depends_on("libtiff")
    depends_on("gsl")
    depends_on("libpng@1.6:")
    depends_on("opencl")
