# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openrasmol(MakefilePackage):
    """RasMol is a molecular graphics program intended for the
       visualisation of proteins, nucleic acids and small molecules."""

    homepage = "http://www.openrasmol.org/"
    url      = "https://sourceforge.net/projects/openrasmol/files/RasMol/RasMol_2.7.5/RasMol-2.7.5.2.tar.gz"

    version('2.7.5.2', sha256='b975e6e69d5c6b161a81f04840945d2f220ac626245c61bcc6c56181b73a5718')

    depends_on('imake', type='build')
    depends_on('libxext')
    depends_on('libxi')

    depends_on('cbflib')
    depends_on('cqrlib')
    depends_on('cvector')
    depends_on('neartree')
    depends_on('xforms@1.0.91')

    patch('rasmol_noqa.patch')
    patch('rasmol_imake.patch')
    patch('rasmol_imakec.patch')
    patch('rasmol_help.patch')

    def edit(self, spec, prefix):
        mf = FileFilter(join_path('src', 'Imakefile'))
        mf.filter('SPACK_XFORMS', spec['xforms'].prefix)
        mf.filter('SPACK_CBF', spec['cbflib'].prefix)
        mf.filter('SPACK_CQR', spec['cqrlib'].prefix)
        mf.filter('SPACK_CVECTOR', spec['cvector'].prefix)
        mf.filter('SPACK_NEARTREE', spec['neartree'].prefix)
        df = FileFilter(join_path('src', 'host.def'))
        df.filter('SPACK_CC', spack_cc)

    def build(self, spec, prefix):
        with working_dir('src'):
            bash = which('bash')
            bash('./build_all.sh')

    def install(self, spec, prefix):
        install_tree('./data', prefix.sample)
        install_tree('./doc', prefix.doc)
        with working_dir('src'):
            bash = which('bash')
            bash('./rasmol_install.sh', '--prefix={0}'.format(prefix))
