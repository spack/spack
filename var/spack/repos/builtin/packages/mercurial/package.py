# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

from spack.package import *


class Mercurial(PythonPackage):
    """Mercurial is a free, distributed source control management tool."""

    homepage = "https://www.mercurial-scm.org"
    url = "https://www.mercurial-scm.org/release/mercurial-5.3.tar.gz"

    version("5.8", sha256="fc5d6a8f6478d88ef83cdd0ab6d86ad68ee722bbdf4964e6a0b47c3c6ba5309f")
    version("5.7.1", sha256="cb5139144ccb2ef648f36963c8606d47dea1cb0e22aa2c055d6f860ce3fde7b0")
    version("5.7", sha256="609c3e7c9276dd75b03b713eccc10f5e0553001f35ae21600bcea1509699c601")
    version("5.6.1", sha256="e55c254f4904c45226a106780e57f4279aee03368f6ff6a981d5d2a38243ffad")
    version("5.3", sha256="e57ff61d6b67695149dd451922b40aa455ab02e01711806a131a1e95c544f9b9")
    version("5.1.2", sha256="15af0b090b23649e0e53621a88dde97b55a734d7cb08b77d3df284db70d44e2e")
    version("5.1.1", sha256="35fc8ba5e0379c1b3affa2757e83fb0509e8ac314cbd9f1fd133cf265d16e49f")
    version("4.9.1", sha256="1bdd21bb87d1e05fb5cd395d488d0e0cc2f2f90ce0fd248e31a03595da5ccb47")
    version("4.4.1", sha256="8f2a5512d6cc2ffb08988aef639330a2f0378e4ac3ee0e1fbbdb64d9fff56246")

    depends_on("python+bz2+ssl+zlib@2.7:2.8,3.5.3:3.5,3.6.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-docutils", type="build")
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))

    def setup_build_environment(self, env):
        # Python 3 support is still experimental, explicitly allow
        env.set("HGALLOWPYTHON3", True)
        env.set("HGPYTHON3", True)
        # Setuptools is still opt-in, explicitly enable
        env.set("FORCE_SETUPTOOLS", True)

    @run_after("install")
    def post_install(self):
        prefix = self.prefix

        # Install man pages
        mkdirp(prefix.man.man1)
        mkdirp(prefix.man.man5)
        mkdirp(prefix.man.man8)
        with working_dir("doc"):
            install("hg.1", prefix.man.man1)
            install("hgignore.5", prefix.man.man5)
            install("hgrc.5", prefix.man.man5)
            install("hg-ssh.8", prefix.man.man8)

        # Install completion scripts
        contrib = prefix.contrib
        mkdir(contrib)
        with working_dir("contrib"):
            install("bash_completion", contrib.bash_completion)
            install("zsh_completion", contrib.zsh_completion)

    @run_after("install")
    def configure_certificates(self):
        """Configuration of HTTPS certificate authorities
        https://www.mercurial-scm.org/wiki/CACertificates"""

        etc_dir = self.prefix.etc.mercurial
        mkdirp(etc_dir)

        hgrc_filename = etc_dir.hgrc

        # Use certifi to find the location of the CA certificate
        certificate = python("-c", "import certifi; print(certifi.where())", output=str)

        if not certificate:
            tty.warn(
                "CA certificate not found. You may not be able to "
                "connect to an HTTPS server. If your CA certificate "
                "is in a non-standard location, you should add it to "
                "{0}.".format(hgrc_filename)
            )
        else:
            # Write the global mercurial configuration file
            with open(hgrc_filename, "w") as hgrc:
                hgrc.write("[web]\ncacerts = {0}".format(certificate))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Sanity-check setup."""

        hg = Executable(self.prefix.bin.hg)

        hg("debuginstall")
        hg("version")
