# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlBioBigfile(PerlPackage):
    """Bio::DB::BigFile -- Low-level interface to BigWig & BigBed files for perl"""

    homepage = "https://metacpan.org/pod/Bio::DB::BigFile"
    url = "https://cpan.metacpan.org/authors/id/L/LD/LDS/Bio-BigFile-1.07.tar.gz"

    maintainers("teaguesterling")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later", checked_by="teaguesterling")

    version("1.07", sha256="277b66ce8acbdd52399e2c5a0cf4e3bd5c74c12b94877cd383d0c4c97740d16d")
    version("1.06", sha256="15f1ece2563096a301cff533a9ac91b8fc31af7643b4c4d7fd5d4fa75d4cb5ef")
    version("1.05", sha256="1675662cfeff05a4e7289132481fd6cf8a15578bef0552b614047a03048fd057")
    version("1.04", sha256="aef1db4cc4f4fb5b4d629719e16b50ec8d0b471d90e894060a88bd379647c4fa")
    version("1.03", sha256="cb4c61c4d880661580f1964280a3731e31c952a3f7e973e7096b2377a6c62d29")
    version("1.02", sha256="baab5010d2b1121c9f84fb1a8c873ced6e24882ef9bece1c3a2b455ed90925fd")
    version("1.01", sha256="662310df5cad45f916c341e6b9a888323bd7b2d6a96957fdf8b0be73de7c3877")
    version("1.00", sha256="925c9b94d5ea10db59911556fe87d4566e12032d13c70c574e74dc009cf73b91")

    depends_on("perl-module-build", type="build")
    depends_on("gmake", type="build")

    with default_args(type=("build", "link", "run")):
        depends_on("perl-bioperl")
        depends_on("perl-io-string")
        depends_on("kentutils")
        depends_on("openssl")

    def setup_build_environment(self, env):
        kent_src = self.spec["kentutils"]
        env.set("KENT_SRC", kent_src.prefix)
        env.set("MACHTYPE", kent_src.package.machtype)

