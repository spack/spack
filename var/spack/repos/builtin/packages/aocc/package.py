# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

from spack.package import *


class Aocc(Package):
    """
    The AOCC compiler system is a high performance, production quality code
    generation tool.  The AOCC environment provides various options to developers
    when building and optimizing C, C++, and Fortran applications targeting 32-bit
    and 64-bit Linux platforms.  The AOCC compiler system offers a high level of
    advanced optimizations, multi-threading and processor support that includes
    global optimization, vectorization, inter-procedural analyses, loop
    transformations, and code generation.  AMD also provides highly optimized
    libraries, which extract the optimal performance from each x86 processor core
    when utilized.  The AOCC Compiler Suite simplifies and accelerates development
    and tuning for x86 applications.

    Installation requires acceptance of the EULA by setting the +license-agreed variant.
    https://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf

    Example for installation: \'spack install aocc +license-agreed\'
    """

    _name = "aocc"
    family = "compiler"
    homepage = "https://developer.amd.com/amd-aocc/"

    maintainers("amd-toolchain-support")

    version(
        ver="4.0.0",
        sha256="2729ec524cbc927618e479994330eeb72df5947e90cfcc49434009eee29bf7d4",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-4.0.0.tar",
    )
    version(
        ver="3.2.0",
        sha256="8493525b3df77f48ee16f3395a68ad4c42e18233a44b4d9282b25dbb95b113ec",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-3.2.0.tar",
    )
    version(
        ver="3.1.0",
        sha256="1948104a430506fe5e445c0c796d6956109e7cc9fc0a1e32c9f1285cfd566d0c",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-3.1.0.tar",
    )
    version(
        ver="3.0.0",
        sha256="4ff269b1693856b9920f57e3c85ce488c8b81123ddc88682a3ff283979362227",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-3.0.0.tar",
    )
    version(
        ver="2.3.0",
        sha256="9f8a1544a5268a7fb8cd21ac4bdb3f8d1571949d1de5ca48e2d3309928fc3d15",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-2.3.0.tar",
    )
    version(
        ver="2.2.0",
        sha256="500940ce36c19297dfba3aa56dcef33b6145867a1f34890945172ac2be83b286",
        url="https://developer.amd.com/wordpress/media/files/aocc-compiler-2.2.0.tar",
    )

    # Licensing
    license_url = "https://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf"

    depends_on("libxml2")
    depends_on("zlib")
    depends_on("ncurses")
    depends_on("libtool")
    depends_on("texinfo")

    variant(
        "license-agreed",
        default=False,
        sticky=True,
        description="Confirm acceptance of the EULA ({0})".format(license_url),
    )

    conflicts(
        "~license-agreed",
        msg=(
            "Installation of {0} requires acceptance of the EULA (found at {1}). Set the "
            "+license-agreed variant to confirm acceptance of the EULA"
        ).format(_name, license_url),
    )

    @run_before("install")
    def license_reminder(self):
        if "+license-agreed" in self.spec:
            tty.msg(
                "Reminder: by setting +license-agreed you are confirming you agree to the terms "
                "of the {0} EULA (found at {1})".format(self.spec.name, self.license_url)
            )
        else:
            # Conflict means we should never get here...
            msg = (
                "Installation of {0} requires acceptance of the EULA (found at {1}). Set the "
                "+license-agreed variant to confirm acceptance of the EULA"
            ).format(self.spec.name, self.license_url)
            raise InstallError(msg)

    def install(self, spec, prefix):
        print("Installing AOCC Compiler ... ")
        install_tree(".", prefix)
