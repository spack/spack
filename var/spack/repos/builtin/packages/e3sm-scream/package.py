# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E3smScream(Package, CudaPackage):
    """Builds dependencies for E3SM SCREAM"""

    homepage = "https://e3sm.org/"
    url = "https://github.com/E3SM-Project/scream"
    git = "https://github.com/E3SM-Project/scream.git"

    # maintainers = ["Jessicat-H", "mtaylo12"]

    version("master", branch="master", submodules=True)

    depends_on("cmake@3.18.0:")
    depends_on("cuda", when="+cuda")
    
    # netcdf-c@4.4.5:4.7.0 incompatible with netcdf-fortran@4.5: (https://www.unidata.ucar.edu/support/help/MailArchives/netcdf/msg14846.html) 
    depends_on("netcdf-c@4.7.1:")
    depends_on("netcdf-fortran@4.4.5:")
    depends_on("parallel-netcdf@1.10:")
    
    depends_on("py-poetry", type=("build", "link", "run"))
    depends_on("py-pip", type=("build", "link", "run"))
    depends_on("py-pyyaml", type=("build", "link", "run"))
    depends_on("py-pylint", type=("build", "link", "run"))
    depends_on("py-psutil", type=("build", "link", "run"))
    depends_on("perl-xml-libxml", type=("build", "link", "run"))

    #depends_on("util-linux-uuid", when="%intel")
    #depends_on("intel-mkl@2020.0.166", when="%intel", type=("build", "link", "run"))
    #depends_on("intel-mkl", when="%intel", type=("build", "link", "run"))
    
    #conflicts("diffutils@3.8:", when="%intel")

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
