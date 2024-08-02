# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install msr-safe
#
# You can edit this file again by typing:
#
#     spack edit msr-safe
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class MsrSafe(MakefilePackage):
    """msr_safe provides controlled userspace access to model-specific registers (MSRs). 
    It allows system administrators to give register-level read access and bit-level write 
    access to trusted users in production environments. This access is useful where kernel 
    drivers have not caught up with new processor features, or performance constraints 
    requires batch access across dozens or hundreds of registers."""

    homepage = "https://github.com/LLNL/msr-safe"
    url = "https://github.com/LLNL/msr-safe/archive/refs/tags/v1.7.0.tar.gz"

    maintainers("fleshling", "rountree", "rountree-alt")

    license("GPL-2.0-only", checked_by="fleshling")

    version("diapason", md5="61184ea72d900474772ee3239c3118ea",
        url="https://github.com/rountree/msr-safe/archive/refs/heads/diapason.zip")

    version("1.7.0", sha256="bdf4f96bde92a23dc3a98716611ebbe7d302005305adf6a368cb25da9c8a609a")
    version("1.6.0", sha256="defe9d12e2cdbcb1a9aa29bb09376d4156c3dbbeb7afc33315ca4b0b6859f5bb")
    version("1.5.0", sha256="e91bac281339bcb0d119a74d68a73eafb5944fd933a893e0e3209576b4c6f233")
    version("1.4.0", sha256="3e5a913e73978c9ce15ec5d2bf1a4583e9e5c30e4e75da0f76d9a7a6153398c0")
    version("1.3.0", sha256="718dcc78272b45ffddf520078e7e54b0b6ce272f1ef0376de009a133149982a0")
    version("1.2.0", sha256="d3c2e5280f94d65866f82a36fea50562dc3eaccbcaa81438562caaf35989d8e8")
    version("1.1.0", sha256="5b723e9d360e15f3ed854a84de7430b2b77be1eb1515db03c66456db43684a83")
    version("1.0.2", sha256="9511d021ab6510195e8cc3b0353a0ac414ab6965a188f47fbb8581f9156a970e")

    depends_on("linux")

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter("Makefile")
        # makefile.filter("CC = .*", "CC = cc")
        pass

    # Should be "make -C /full/path/to/depends/on/package/source M=/full/path/to/package/source modules"
    @property
    def build_targets(self):
        return [
            f"-C",
            f"{self.spec['linux'].prefix}",
            f"M={self.build_directory}",
            "modules"
        ]
