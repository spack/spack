# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install tfel
#
# You can edit this file again by typing:
#
#     spack edit tfel
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Tfel(CMakePackage):
    """
    `TFEL` is a collaborative development of CEA and EDF.

    `MFront` is a code generator which translates a set of closely related
    domain specific languages into plain C++ on top of the `TFEL`
    library. Those languages covers three kind of material knowledge:

    - material properties (for instance the
      Young modulus, the thermal conductivity, etc.)
    - mechanical behaviours. Numerical performances of generated
      mechanical behaviours was given a particular attention. MFront
      offers a variety of interfaces to finite element solvers `Cast3M`,
      `Code-Aster`, `EUROPLEXUS`, `Abaqus-Standard`, `Abaqus-Explicit`,
      `Zebulon`, etc.. or various FFT solvers such as
      `AMITEX_FFTP`. Various benchmarks shows that `MFront`
      implementations are competitive with native implementations
      available in the `Cast3M`, `Code-Aster` and `Cyrano3` solvers.
    - simple point-wise models, such as material swelling
      used in fuel performance codes.

    `MFront` comes with an handy easy-to-use tool called `MTest` that can
    test the local behaviour of a material, by imposing independent
    constraints on each component of the strain or the stress. This tool
    has been much faster (from ten to several hundred times depending on
    the test case) than using a full-fledged finite element solver.
    """

    homepage = "http://tfel.sourceforge.net"
    url      = "https://github.com/thelfer/tfel/archive/TFEL-3.2.0.tar.gz"
    git      = "https://github.com/thelfer/tfel.git"

    # development branches
    version("master", branch="master")
    version("rliv-3.2", branch="rliv-3.2")
    version("rliv-3.1", branch="rliv-3.1")
    version("rliv-3.0", branch="rliv-3.0")
    version("rliv-2.0", branch="rliv-2.0")
    version("rliv-1.2", branch="rliv-1.2")

    # released version
    version('3.2.0', sha256='089d79745e9f267a2bd03dcd8841d484e668bd27f5cc2ff7453634cb39016848')
    version('3.1.3', sha256='2022fa183d2c2902ada982ec6550ebe15befafcb748fd988fc9accdde7976a42')
    version('3.1.2', sha256='2eaa191f0699031786d8845ac769320a42c7e035991d82b3738289886006bfba')
    version('3.1.1', sha256='a4c0c21c6c22752cc90c82295a6bafe637b3395736c66fcdfcfe4aeccb5be7af')
    version('3.1.0', sha256='dd67b400b5f157aef503aa3615b9bf6b52333876a29e75966f94ee3f79ab37ad')
    version('3.0.3', sha256='3ff1c14bcc27e9b615aab5748eaf3afac349050b27b55a2b57648aba28b801ac')
    version('3.0.2', sha256='edd54ac652e99621410137ea2f7f90f133067615a17840440690365e2c3906f5')
    version('3.0.1', sha256='fa239ddd353431954f2ab7443cf85d86c862433e72f7685c1b933ae12dbde435')
    version('3.0.0', sha256='b2cfaa3d7900b4f32f327565448bf9cb8e4242763f651bff8f231f378a278f9e')
    version('2.0.4', sha256='cac078435aad73d9a795516f161b320d204d2099d6a286e786359f484355a43a')

    variant('python',
            default=True, description='Enables python interface')
    variant('python_bindings',
            default=True, description='Enables python bindings')

    depends_on('boost', when='+python_bindings')

    def cmake_args(self):

        args = ["-Denable-fortran=ON",
                "-Denable-castem=ON",
                "-Denable-aster=ON",
                "-Denable-abaqus=ON",
                "-Denable-calculix=ON",
                "-Denable-ansys=ON",
                "-Denable-europlexus=ON",
                "-Denable-cyrano=ON",
                "-Denable-lsdyna=ON"]

        if '+python_bindings' in self.spec:
            args.append("-Denable-python=ON")

        if '+python_bindings' in self.spec:
            args.append("-Denable-python-bindings=ON")

        return args
