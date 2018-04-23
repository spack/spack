##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os
import llnl.util.tty as tty
import shutil


# http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
def xcopytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class Galahad(Package):
    """Optimization Library"""

    homepage = "http://www.galahad.rl.ac.uk/"

    # Galahad has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('2.60003', '2a0b77eacb55987118d2217a318f8541')
    url = 'http://none/galahad-2.60003.tar.gz'

    mainatiners = ['citibeth']

    # GALAHAD uses its own internal BLAS/LAPACK,
    # I don't know how to turn it off for now
    # depends_on('blas')
    # depends_on('lapack')
    depends_on('gsl')

    depends_on('archdefs-src')
    depends_on('cutest-src')
    depends_on('sifdecode-src')

    def install(self, spec, prefix):
        stage = self.stage
        os.chdir(stage.source_path)

        shutil.rmtree('cutest', ignore_errors=True)
        shutil.rmtree('sifdecode', ignore_errors=True)
        shutil.copytree(spec['cutest-src'].prefix, 'cutest')
        shutil.copytree(spec['sifdecode-src'].prefix, 'sifdecode')

        # os.environ['BLAS'] = spec['blas'].prefix
        # os.environ['LAPACK'] = spec['lapack'].prefix
        os.environ['C_INCLUDE_PATH'] = os.path.join(
            spec['gsl'].prefix, 'include')
        os.environ['GALAHAD'] = spec.prefix
        os.environ['ARCHDEFS'] = spec['archdefs-src'].prefix
        os.environ['CUTEST'] = os.path.join(stage.source_path, 'cutest')
        os.environ['SIFDECODE'] = os.path.join(stage.source_path, 'sifdecode')

        with open('build_input.txt', 'w') as fout:
            fout.write('y3\nc\n6\n2\nn2\nn3\nnyydydy')
            fout.write('\n')

        install_optsuite = Executable(os.path.join(
            spec['archdefs-src'].prefix, 'install_optsuite'))

        with open('build_input.txt', 'r') as fin:
            try:
                install_optsuite(input=fin)
            except Exception as e:
                tty.warn('Ignoring error while building' +
                         ' (this is normal): %s' % str(e))

        version = 'pc64.lnx.gfo'
        shutil.copytree(
            os.path.join(stage.source_path, 'modules', version, 'double'),
            os.path.join(spec.prefix, 'include'))

        prefix_include = os.path.join(spec.prefix, 'include')
        prefix_lib = os.path.join(spec.prefix, 'lib')

        path = os.path.join(
            stage.source_path, 'cutest', 'modules', version, 'double')
        xcopytree(path, prefix_include)

        path = os.path.join(
            stage.source_path,
            'sifdecode', 'objects', version, 'double')
        xcopytree(path, prefix_include)

        shutil.copytree(
            os.path.join(stage.source_path, 'objects', version, 'double'),
            prefix_lib)

        path = os.path.join(
            stage.source_path,
            'cutest', 'objects', version, 'double')
        xcopytree(path, prefix_lib)

        path = os.path.join(
            stage.source_path,
            'sifdecode', 'objects', version, 'double'),
        xcopytree(path, prefix_lib)
