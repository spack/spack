# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack.package import *

try:
    from spack.build_systems.perl import PerlBuilder as builder
except ImportError:
    from spack.build_systems.perl import PerlPackage as builder


class PerlIoSocketSsl(PerlPackage):
    """SSL sockets with IO::Socket interface"""

    homepage = "https://metacpan.org/dist/IO-Socket-SSL/view/lib/IO/Socket/SSL.pod"
    url = "https://cpan.metacpan.org/authors/id/S/SU/SULLR/IO-Socket-SSL-2.052.tar.gz"

    version("2.074", sha256="36486b6be49da4d029819cf7069a7b41ed48af0c87e23be0f8e6aba23d08a832")
    version("2.073", sha256="b2c0b34df97cb1aa816221cee2454a1efd89b86ccbda810389a30e0d08cf57c8")
    version("2.072", sha256="b5bee81db3905a9069340a450a48e1e1b32dec4ede0064f5703bafb9a707b89d")
    version("2.071", sha256="40da40948ecc9c787ed39c95715872679eebfd54243721174993a2003e32ab0a")
    version("2.070", sha256="876fe09763e7a474519431aff248cb1f1abaf070d6bdc791f60bf9abe781cd3b")
    version("2.069", sha256="d83c2cae5e8a22ab49c9f2d964726625e9efe56490d756a48a7b149a3d6e278d")
    version("2.068", sha256="4420fc0056f1827b4dd1245eacca0da56e2182b4ef6fc078f107dc43c3fb8ff9")
    version("2.067", sha256="ef8842806d047cf56e2af64add4ed30b24547bcbb50e8df33cee0c54609af1c1")
    version("2.066", sha256="0d47064781a545304d5dcea5dfcee3acc2e95a32e1b4884d80505cde8ee6ebcd")
    version("2.065", sha256="b5977c62709db19a26a336debd887aa131d39cd48a8d1495ef640457cea83dab")
    version("2.064", sha256="5827c6459ed2dce1da0ba6f442d198fa2c81554e045930e32b92c6d39e3ac3f5")
    version("2.063", sha256="5fc33c573dbd8383018e49fbc3d6f933c2ae0597e272f2225d5b7ce08f8b2327")
    version("2.062", sha256="1a62202b9357e1550230ce07bbad7e5f22ec815979a88f56bd7177790f9881ba")
    version("2.061", sha256="7b7dddc6c2653f567092f5a179504a6b299adfac8625c6f6839622a8b45200e5")
    version("2.060", sha256="fb5b2877ac5b686a5d7b8dd71cf5464ffe75d10c32047b5570674870e46b1b8c")
    version("2.059", sha256="217debbe0a79f0b7c5669978b4d733271998df4497f4718f78456e5f54d64849")
    version("2.058", sha256="746cd17c292cfc206b394497a060b0582d0b06a1040e6bb27e6530d56786e40b")
    version("2.057", sha256="635f33405ab8db1af7c523d97dd2a699ae23355a2d8fbd2d47fa6aaea98e1572")
    version("2.056", sha256="91451ecc28b243a78b438f0a42db24c4b60a86f088879b38e40bdbd697818259")
    version("2.055", sha256="32278dfc5e7ef8e9231654e5540a9f0cc67e0f4b4c31a06399b6053c49eb23f9")
    version("2.054", sha256="02ea04e9a336a7d3ca9aa604c0c5b5aaf3efa513cefecfc73cc79ceeb5131e4b")
    version("2.053", sha256="c51eaf315cddd2d0d6f870bce9d3fe58872a02148017ac10f25d2e6b25c15bbb")
    version("2.052", sha256="e4897a9b17cb18a3c44aa683980d52cef534cdfcb8063d6877c879bfa2f26673")

    provides("perl-io-socket-ssl-intercept@2.056")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-ocsp-cache")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-ocsp-resolver")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-publicsuffix")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-ssl-context")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-ssl-handle")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-session-cache")  # AUTO-CPAN2Spack
    provides("perl-io-socket-ssl-utils@2.015")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-mozilla-ca", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-net-ssleay@1.46:", type="run")  # AUTO-CPAN2Spack

    def configure(self, spec, prefix):
        builder.build_method = "Makefile.PL"
        builder.build_executable = inspect.getmodule(self).make
        # Should I do external tests?
        config_answers = ["n\n"]
        config_answers_filename = "spack-config.in"

        with open(config_answers_filename, "w") as f:
            f.writelines(config_answers)

        with open(config_answers_filename, "r") as f:
            inspect.getmodule(self).perl("Makefile.PL", "INSTALL_BASE={0}".format(prefix), input=f)
