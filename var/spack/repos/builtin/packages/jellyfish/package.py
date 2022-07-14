# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jellyfish(AutotoolsPackage):
    """JELLYFISH is a tool for fast, memory-efficient counting of k-mers in
       DNA."""

    homepage = "https://www.cbcb.umd.edu/software/jellyfish/"
    url      = "https://github.com/gmarcais/Jellyfish/releases/download/v2.2.7/jellyfish-2.2.7.tar.gz"
    list_url = "https://www.cbcb.umd.edu/software/jellyfish/"

    version('2.2.7', sha256='d80420b4924aa0119353a5b704f923863abc802e94efeb531593147c13e631a8')
    version('1.1.11', sha256='496645d96b08ba35db1f856d857a159798c73cbc1eccb852ef1b253d1678c8e2',
            url='https://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz')

    variant('pybind', default=False, description='Enable python binding')
    variant('rubybind', default=False, description='Enable ruby binding')
    variant('perlbind', default=False, description='Enable perl binding')

    extends('perl', when='+perlbind')
    extends('python@:2.7.18', when='+pybind')
    extends('ruby', when='+rubybind')

    patch('dna_codes.patch', when='@1.1.11')

    conflicts('+pybind', when='@1.1.11')
    conflicts('+rubybind', when='@1.1.11')
    conflicts('+perlbind', when='@1.1.11')

    def configure_args(self):
        spec = self.spec

        # Can only specify one binding to build with using extends()
        # see https://github.com/spack/spack/issues/987

        if '+pybind' in spec:
            args = [
                '--enable-python-binding',
            ]
        elif '+rubybind' in spec:
            args = [
                '--enable-ruby-binding',
            ]
        elif '+perlbind' in spec:
            args = [
                '--enable-perl-binding'
            ]

        return args
