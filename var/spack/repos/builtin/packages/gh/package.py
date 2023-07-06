# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gh(Package):
    """GitHub's official command line tool."""

    homepage = "https://github.com/cli/cli"
    url = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"

    maintainers("lcnzg")

    version("2.28.0", sha256="cf3c0fb7f601d717d8b5177707a197c49fd426f5dc3c9aa52a932e96ba7166af")
    version("2.25.1", sha256="d3b28da03f49600697d2e80c2393425bd382e340040c34641bf3569593c7fbe8")
    version("2.25.0", sha256="b445dbb863643d30cc7991b134c694ea14492e7fac363a9e2648f245f67184f7")
    version("2.24.3", sha256="f5c8a273d3adabee9d4a07d38e738df589f1e9dcdae03f9c7b8e3d8aa4b58cf4")
    version("2.23.0", sha256="1e9f92a47caa92efedc06b22cfe9c951c5163c4a9bc60a45d477fd5d9b592e54")
    version("2.5.1", sha256="89aac9c35ad875f1b17144bf9fcbfa7231554d4abce187d9277fcc83da846e4a")
    version("2.5.0", sha256="4e9d1cbcdd2346cab5b7fc176cd57c07ed3628a0241fad8a48fe4df6a354b120")
    version("2.4.0", sha256="3c87db4d9825a342fc55bd7f27461099dd46291aea4a4a29bb95d3c896403f94")
    version("2.3.0", sha256="56bcf353adc17c386377ffcdfc980cbaff36123a1c1132ba09c3c51a7d1c9b82")
    version("2.2.0", sha256="597c6c1cde4484164e9320af0481e33cfad2330a02315b4c841bdc5b7543caec")
    version("2.1.0", sha256="4b353b121a0f3ddf5046f0a1ae719a0539e0cddef27cc78a1b33ad7d1d22c007")
    version("2.0.0", sha256="5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426")
    version("1.14.0", sha256="1a99050644b4821477aabc7642bbcae8a19b3191e9227cd8078016d78cdd83ac")
    version("1.13.1", sha256="1a19ab2bfdf265b5e2dcba53c3bd0b5a88f36eff4864dcc38865e33388b600c5")

    conflicts("platform=darwin", when="@2.28.0")

    depends_on("go@1.16:", type="build")

    phases = ["build", "install"]

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install", "prefix=" + prefix)
