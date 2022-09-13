# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install ndzip
#
# You can edit this file again by typing:
#
#     spack edit ndzip
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Ndzip(CMakePackage, CudaPackage):
    """A High-Throughput Parallel Lossless Compressor for Scientific Data"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/fknorr/ndzip"
    git = "https://github.com/robertu94/ndzip"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['robertu94']

    # FIXME: Add proper versions and checksums here.
    version('master', branch='master')

    variant('sycl', description="build with hipsycl support", default=False)
    variant('cuda', description="build with cuda support", default=False)
    variant('openmp', description="build with cuda support", default=False)


    depends_on('hipsycl@develop', when="+sycl")

    conflicts('%gcc', when="+sycl")

    def cmake_args(self):
        args = [
            self.define_from_variant("NDZIP_WITH_CUDA", "cuda"),
            self.define_from_variant("NDZIP_WITH_HIPSYCL", "sycl"),
            self.define_from_variant("NDZIP_WITH_MT", "openmp"),
            self.define("NDZIP_BUILD_BENCHMARK", False),
            self.define("NDZIP_BUILD_TEST", self.run_tests),
            self.define("NDZIP_USE_WERROR", False),
        ]
        if "+cuda" in self.spec and self.spec.variants['cuda_arch'].value != "none":
            arch_str = ";".join(self.spec.variants['cuda_arch'].value)
            args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))
        if "+sycl" in self.spec:
            if "+cuda" in self.spec['hipsycl']:
                args.append(self.define("HIPSYCL_PLATFORM", "cuda"))
            else:
                args.append(self.define("HIPSYCL_PLATFORM", "cpu"))
        return args
