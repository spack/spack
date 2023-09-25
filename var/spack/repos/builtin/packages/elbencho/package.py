# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
#     spack install elbencho
#
# You can edit this file again by typing:
#
#     spack edit elbencho
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import os

class Elbencho(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/breuner/elbencho"
    url = "https://github.com/breuner/elbencho/archive/refs/tags/v3.0-1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("ethanjjjjjjj")

    version("3.0-1", sha256="19dad85e1fc74419dcdf740f11a47d3f6d566770a06e40976755a3404566c11d")
    version("2.2-5", sha256="4b598639452665a8b79c4c9d8a22ae63fb9b04057635a45e686aa3939ee255b4")
    version("2.2-3", sha256="0ae2d495d2863b84f21f55b7c526674fab1be723d0697087017946647f79d0e6")
    version("2.1-5", sha256="5d2293dcdb766e9194bed964486a10b4c8c308cc1ba8c0044c6e5a2aadd4f199")
    version("2.1-3", sha256="9d08aa0e83753666cb16a78320dfa5710350879f9f4f1e281dacd69f53249d01")
    version("2.1-1", sha256="18be49f521df2fab4f16a1a9f00dd6104a25e5ea335ce8801bf07268ed9271a9")
    version("2.0-9", sha256="fe0f67fbb7dd7c743f8b3e0a92358f7393f2950da456474d4adb38690fab1878")
    version("2.0-7", sha256="a2e49cb2cf1ae99e46e9fa95b42ece250cb58fbadb4c393f9776b40204e8b2c0")
    # FIXME: Add dependencies if required.
    # depends_on("foo")
   # depends_on("")
    
    variant(

    "s3", default=False, description="Enable support for s3 api"
    
)
    variant("cuda", default=True, description="Enable CUDA support", when="+cufile")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("cufile", default=False,description="GDS GPU Direct Storage support")
    depends_on("cuda",when="+cuda")
    conflicts("+cufile", when="~cuda")
    def edit(self, spec, prefix):
        config={}
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        os.mkdir(prefix.bin)
        os.environ['INST_PATH'] = prefix.bin
        if "+s3" in spec:
          os.environ['S3_SUPPORT'] = "1"
        if "+cuda" in spec:
          os.environ['CUDA_SUPPORT'] = "1"
        if "+cufile" in spec:
          os.environ['CUDA_SUPPORT'] = "1"
        makefile = FileFilter("Makefile")
        makefile.filter('\s+/etc/bash_completion.d/', f' {prefix}/etc/bash_completion.d/')
        pass
