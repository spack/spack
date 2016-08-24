##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Pocl(Package):
    """Portable Computing Language (pocl) is an open source implementation
    of the OpenCL standard which can be easily adapted for new targets
    and devices, both for homogeneous CPU and heterogeneous
    GPUs/accelerators."""

    homepage = "http://portablecl.org"
    url = "http://portablecl.org/downloads/pocl-0.13.tar.gz"

    version("0.13", "344480864d4269f2f63f1509395898bd")
    version("0.12", "e197ba3aa01a35f40581c48e053330dd")
    version("0.11", "9be0640cde2983062c47393d9e8e8fe7")
    version("0.10", "0096be4f595c7b5cbfa42430c8b3af6a")
    version("0.9", "f95f4a9e7870854c60be2d2269c3ebec")

    # This is Github's pocl/pocl#373
    patch("uint.patch")
    patch("vecmathlib.patch")

    depends_on("hwloc")
    depends_on("libtool", type="build")
    # We don't request LLVM's shared libraries because these fail to
    # build for us (Ubuntu 14.04)
    depends_on("llvm +clang")
    depends_on("pkg-config", type="build")

    def install(self, spec, prefix):
        with working_dir("spack-build", create=True):
            # Could switch to cmake build
            configure = Executable(join_path(self.stage.source_path,
                                             "configure"))
            configure("--prefix=%s" % prefix,
                      "--disable-icd", "--enable-direct-linkage",
                      # We use static linking againste the LLVM
                      # libraries because we didn't request LLVM's
                      # shared libraries
                      "--enable-static-llvm",
                      "--enable-static",
                      "--disable-shared",
                      "CFLAGS=-std=gnu99",
                      "HWLOC_CFLAGS=-I%s" % spec["hwloc"].prefix.include,
                      "HWLOC_LIBS=-L%s -lhwloc" % spec["hwloc"].prefix.lib,
                      "LLVM_CONFIG=%s" % join_path(spec["llvm"].prefix.bin,
                                                   "llvm-config"),
                      "CLANGXX_FLAGS=-std=gnu++11")
            make()
            make("install")
        self.check_install(spec)

    def check_install(self, spec):
        "Build and run a small program to test the installed package"
        print "Checking pocl installation..."
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            # Import source files from package
            for src in ["scalarwave.c", "scalarwave.cl"]:
                shutil.copyfile(join_path(self.package_dir(), src), src)
            # Build driver
            cc = which("cc")
            cc("-c",
               "-I%s" % join_path(spec.prefix, "include"),
               "-I%s" % join_path(spec.prefix, "share", "pocl", "include"),
               "scalarwave.c")
            cc("-o", "scalarwave",
               "scalarwave.o",
               "-L%s" % join_path(spec.prefix, "lib"),
               "-lpocl")
            # Read expected output
            with open(join_path(self.package_dir(),
                                "expected-output.txt"), "r") as f:
                expected = f.read()
            # Run driver, building and running the OpenCL code
            try:
                scalarwave = Executable("./scalarwave")
                output = check(return_output=True)
            except:
                output = ""
            # Check output
            success = output == expected
            if not success:
                print "Produced output does not match expected output."
                print "Produced output:"
                print "-" * 80
                print output
                print "-" * 80
                print "Expected output:"
                print "-" * 80
                print expected
                print "-" * 80
                raise InstallError("pocl install check failed")
        # Clean up
        shutil.rmtree(checkdir)
