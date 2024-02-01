# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neko(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Neko: A modern, portable, and scalable framework
    for high-fidelity computational fluid dynamics
    """

    homepage = "https://github.com/ExtremeFLOW/neko"
    git = "https://github.com/ExtremeFLOW/neko.git"
    url = "https://github.com/ExtremeFLOW/neko/releases/download/v0.3.2/neko-0.3.2.tar.gz"
    maintainers("njansson")

    version("0.6.1", sha256="6282baaf9c8a201669e274cba23c37922f7ad701ba20ef086442e48f00dabf29")
    version("0.6.0", sha256="ce37c7cea1a7bf1bf554c5717aa7fed35bbd079ff68c2fc9d3529facc717e31a")
    version("0.5.2", sha256="8873f5ada106f92f21c9bb13ea8164550bccde9301589b9e7f1c1a82a2efe2b8")
    version("0.5.1", sha256="8b176bcc9f2d4a6804b68dd93a2f5e02e2dfa986d5c88063bbc72d39e9659cc4")
    version("0.5.0", sha256="01a745f2e19dd278330889a0dd6c5ab8af49da99c888d95c10adb5accc1cbfc4")
    version("0.4.3", sha256="ba8fde09cbc052bb4791a03f69c880705615b572982cd3177ee31e4e14931da2")
    version("0.4.2", sha256="927f926bdbf027c30e8e383e1790e84b60f5a9ed61e48a413092aac2ab24abcc")
    version("0.3.2", sha256="0628910aa9838a414f2f27d09ea9474d1b3d7dcb5a7715556049a2fdf81a71ae")
    version("0.3.0", sha256="e46bef72f694e59945514ab8b1ad7d74f87ec9dca2ba2b230e2148662baefdc8")
    version("develop", branch="develop")
    variant("parmetis", default=False, description="Build with support for parmetis")
    variant("xsmm", default=False, description="Build with support for libxsmm")
    variant("gslib", default=False, when="@develop", description="Build with support for gslib")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("parmetis", when="+parmetis")
    depends_on("libxsmm", when="+xsmm")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("json-fortran", when="@develop")
    depends_on("gslib", when="+gslib")

    def configure_args(self):
        args = []
        args.append("--with-blas={0}".format(self.spec["blas"].libs.joined(";")))
        args.append("--with-lapack={0}".format(self.spec["lapack"].libs.joined(";")))
        args += self.with_or_without("parmetis", variant="parmetis", activation_value="prefix")
        args += self.with_or_without("metis", variant="parmetis", activation_value="prefix")
        args += self.with_or_without("libxsmm", variant="xsmm")
        args += self.with_or_without("gslib", variant="gslib", activation_value="prefix")
        args += self.with_or_without("cuda", activation_value="prefix")
        rocm_fn = lambda x: self.spec["hip"].prefix
        args += self.with_or_without("hip", variant="rocm", activation_value=rocm_fn)

        return args
