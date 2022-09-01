# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimePiece(PerlPackage):
    """Object Oriented time objects"""

    homepage = "https://metacpan.org/pod/Time::Piece"
    url = "https://cpan.metacpan.org/authors/id/E/ES/ESAYM/Time-Piece-1.3203.tar.gz"

    version("1.34.01", sha256="4b55b7bb0eab45cf239a54dfead277dfa06121a43e63b3fce0853aecfdb04c27",
            url="https://cpan.metacpan.org/authors/id/E/ES/ESAYM/Time-Piece-1.3401.tar.gz")
    version("1.34", sha256="98e6c95b4d536f23a1884073cc49d8af7720be6b2f1717208e0f5b8f632cb973")
    version("1.33", sha256="c7e128bcee285b1e666ea9824c0491e219d482242897e386ca18de268bbee930")
    version("1.32.04", sha256="d7485ea520f913c932032a37ea1d4611ac34bbfbef10a00d392748f744adeabd",
            url="https://cpan.metacpan.org/authors/id/E/ES/ESAYM/Time-Piece-1.3204.tar.gz")
    version("1.32.03", sha256="6971faf6476e4f715a5b5336f0a97317f36e7880fcca6c4db7c3e38e764a6f41",
            url="https://cpan.metacpan.org/authors/id/E/ES/ESAYM/Time-Piece-1.3203.tar.gz")

    provides("perl-time-seconds")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
