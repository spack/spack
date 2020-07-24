# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Whizard(AutotoolsPackage):
    """WHIZARD is a program system designed for the efficient calculation
      of multi-particle scattering cross sections
      and simulated event samples."""

    homepage = "whizard.hepforge.org"
    url      = "https://whizard.hepforge.org/downloads/?f=whizard-2.8.2.tar.gz"
    git      = "https://gitlab.tp.nt.uni-siegen.de/whizard/public.git"

    maintainers = ['vvolkl']

    version('master', branch="master")
    version('3.0.0_alpha', sha256='4636e5a10350bb67ccc98cd105bc891ea04f3393c2420f81be3d21240be20009')
    version('2.8.2', sha256='32c9be342d01b3fc6f947fddce74bf2d81ece37fb39bca1f37778fb0c07e2568', prefered=True)
    version('2.8.1', sha256='0c759ce0598e25f38e04659f745c5963d238c4b5c12209f16449b6c0bc6dc64e')
    version('2.8.0', sha256='3b5175eafa879d1baca20237d18fb2b18bee89631e73ada499de9c082d009696')

    variant('hepmc', default=True,
            description="builds with hepmc")

    variant('pythia8', default=True,
            description="builds with pythia8")

    variant('fastjet', default=False,
            description="builds with fastjet")

    variant('lcio', default=False,
            description="builds with lcio")

    variant('lhapdf', default=False,
            description="builds with fastjet")

    variant('openmp', default=False,
            description="builds with openmp")

    variant('latex', default=False,
            description="data visualization with latex")

    depends_on('ocaml', type='build', when="@3:")
    depends_on('ocaml@:4.8.2', type='build', when="@:2.99.99")
    depends_on('hepmc', when="+hepmc")
    depends_on('pythia8', when="+pythia8")
    depends_on('lhapdf', when="+lhapdf")
    depends_on('fastjet', when="+fastjet")
    depends_on('texlive', when="+latex")
    depends_on('zlib')

    def setup_build_environment(self, env):
        # whizard uses the compiler during runtime,
        # and seems incompatible with
        # filter_compiler_wrappers, thus the
        # actual compilers need to be used to build
        env.set('CC', self.compiler.cc)
        env.set('CXX', self.compiler.cxx)
        env.set('FC', self.compiler.fc)
        env.set('F77', self.compiler.fc)

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-hepmc=%s' % ("yes" if "+hepmc" in spec else "no"),
            '--enable-fastjet=%s' % ("yes" if "+fastjet" in spec else "no"),
            '--enable-pythia8=%s' % ("yes" if "+pythia8" in spec else "no"),
            '--enable-lcio=%s' % ("yes" if "+lcio" in spec else "no"),
            '--enable-lhapdf=%s' % ("yes" if "+lhapdf" in spec else "no"),
            # todo: openloops
            # todo: hoppet
            # todo: recola
            # todo: looptools
            # todo: gosam
            # todo: pythia6
        ]
        if "+openmp" not in spec:
            args.append('--disable-openmp')

        return args

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        patch = str(version[2])
        if len(version) == 4:
            url = "https://whizard.hepforge.org/downloads/?f=whizard-%s.%s.%s_%s.tar.gz" % (major, minor, patch, version[3])
        else:
            url = "https://whizard.hepforge.org/downloads/?f=whizard-%s.%s.%s.tar.gz" % (major, minor, patch)
        return url
