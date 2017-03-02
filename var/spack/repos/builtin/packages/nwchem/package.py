##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import sys
import os


class Nwchem(Package):
    """High-performance computational chemistry software"""

    homepage = "http://www.nwchem-sw.org"
    url      = "http://www.nwchem-sw.org/images/Nwchem-6.6.revision27746-src.2015-10-20.tar.gz"

    version('6.6', 'c581001c004ea5e5dfacb783385825e3',
            url='http://www.nwchem-sw.org/images/Nwchem-6.6.revision27746-src.2015-10-20.tar.gz')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('scalapack')

    depends_on('python@2.7:2.8', type=('build', 'run'))

    # patches for 6.6-27746:
    urls_for_patches = {
        '@6.6': [
            ('http://www.nwchem-sw.org/images/Tddft_mxvec20.patch.gz', 'f91c6a04df56e228fe946291d2f38c9a'),
            ('http://www.nwchem-sw.org/images/Tools_lib64.patch.gz', 'b71e8dbad27f1c97b60a53ec34d3f6e0'),
            ('http://www.nwchem-sw.org/images/Config_libs66.patch.gz', 'cc4be792e7b5128c3f9b7b1167ade2cf'),
            ('http://www.nwchem-sw.org/images/Cosmo_meminit.patch.gz', '1d94685bf3b72d8ecd40c46334348ca7'),
            ('http://www.nwchem-sw.org/images/Sym_abelian.patch.gz', 'b19cade61c787916a73a4aaf6e2445d6'),
            ('http://www.nwchem-sw.org/images/Xccvs98.patch.gz', 'b9aecc516a3551dcf871cb2f066598cb'),
            ('http://www.nwchem-sw.org/images/Dplot_tolrho.patch.gz', '0a5bdad63d2d0ffe46b28db7ad6d9cec'),
            ('http://www.nwchem-sw.org/images/Driver_smalleig.patch.gz', 'c3f609947220c0adb524b02c316b5564'),
            ('http://www.nwchem-sw.org/images/Ga_argv.patch.gz', '7a665c981cfc17187455e1826f095f6f'),
            ('http://www.nwchem-sw.org/images/Raman_displ.patch.gz', 'ed334ca0b2fe81ce103ef8cada990c4c'),
            ('http://www.nwchem-sw.org/images/Ga_defs.patch.gz', '0c3cab4d5cbef5acac16ffc5e6f869ef'),
            ('http://www.nwchem-sw.org/images/Zgesvd.patch.gz', '8fd5a11622968ef4351bd3d5cddce8f2'),
            ('http://www.nwchem-sw.org/images/Cosmo_dftprint.patch.gz', '64dcf27f3c6ced2cadfb504fa66e9d08'),
            ('http://www.nwchem-sw.org/images/Txs_gcc6.patch.gz', '56595a7252da051da13f94edc54fe059'),
            ('http://www.nwchem-sw.org/images/Gcc6_optfix.patch.gz', 'c6642c21363c09223784b47b8636047d'),
            ('http://www.nwchem-sw.org/images/Util_gnumakefile.patch.gz', 'af74ea2e32088030137001ce5cb047c5'),
            ('http://www.nwchem-sw.org/images/Util_getppn.patch.gz', '8dec8ee198bf5ec4c3a22a6dbf31683c'),
            ('http://www.nwchem-sw.org/images/Gcc6_macs_optfix.patch.gz', 'a891a2713aac8b0423c8096461c243eb'),
            ('http://www.nwchem-sw.org/images/Notdir_fc.patch.gz', '2dc997d4ab3719ac7964201adbc6fd79')
        ]
    }
    # Iterate over patches
    for condition, urls in urls_for_patches.iteritems():
        for url, md5 in urls:
            patch(url, when=condition, level=0, md5=md5)

    def install(self, spec, prefix):
        scalapack = spec['scalapack'].libs
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs
        # see http://www.nwchem-sw.org/index.php/Compiling_NWChem
        args = []
        args.extend([
            'NWCHEM_TOP=%s' % self.stage.source_path,
            # NWCHEM is picky about FC and CC. They should NOT be full path.
            # see http://www.nwchem-sw.org/index.php/Special:AWCforum/sp/id7524
            'CC=%s' % os.path.basename(spack_cc),
            'FC=%s' % os.path.basename(spack_fc),
            'USE_MPI=y',
            'MPI_LOC=%s' % spec['mpi'].prefix,
            'USE_PYTHONCONFIG=y',
            'PYTHONVERSION=%s' % spec['python'].version.up_to(2),
            'PYTHONHOME=%s' % spec['python'].prefix,
            'BLASOPT=%s' % ((lapack + blas).ld_flags),
            'BLAS_LIB=%s' % blas.ld_flags,
            'LAPACK_LIB=%s' % lapack.ld_flags,
            'USE_SCALAPACK=y',
            'SCALAPACK=%s' % scalapack.ld_flags,
            'NWCHEM_MODULES=all python',
            'NWCHEM_LONG_PATHS=Y'  # by default NWCHEM_TOP is 64 char max
        ])

        # TODO: query if blas/lapack/scalapack uses 64bit Ints
        # A flag to distinguish between 32bit and 64bit integers in linear
        # algebra (Blas, Lapack, Scalapack)
        use32bitLinAlg = True

        if use32bitLinAlg:
            args.extend([
                'USE_64TO32=y',
                'BLAS_SIZE=4',
                'LAPACK_SIZE=4',
                'SCALAPACK_SIZE=4'
            ])
        else:
            args.extend([
                'BLAS_SIZE=8',
                'LAPACK_SIZE=8'
                'SCALAPACK_SIZE=8'
            ])

        if sys.platform == 'darwin':
            target = 'MACX64'
            args.extend([
                'CFLAGS_FORGA=-DMPICH_NO_ATTR_TYPE_TAGS'
            ])
        else:
            target = 'LINUX64'

        args.extend(['NWCHEM_TARGET=%s' % target])

        with working_dir('src'):
            make('nwchem_config', *args)
            if use32bitLinAlg:
                make('64_to_32', *args)
            make(*args)

            #  need to install by hand. Follow Ubuntu:
            #  http://packages.ubuntu.com/trusty/all/nwchem-data/filelist
            #  http://packages.ubuntu.com/trusty/amd64/nwchem/filelist
            share_path = join_path(prefix, 'share', 'nwchem')
            mkdirp(prefix.bin)

            install_tree('data', share_path)
            install_tree(join_path('basis', 'libraries'),
                         join_path(share_path, 'libraries'))
            install_tree(join_path('nwpw', 'libraryps'),
                         join_path(share_path, 'libraryps'))

            b_path = join_path(self.stage.source_path, 'bin',
                               target, 'nwchem')
            chmod = which('chmod')
            chmod('+x', b_path)
            install(b_path, prefix.bin)

            # Finally, make user's life easier by creating a .nwchemrc file
            # to point to the required data files.
            nwchemrc = """\
   nwchem_basis_library {data}/libraries/
   nwchem_nwpw_library {data}/libraryps/
   ffield amber
   amber_1 {data}/amber_s/
   amber_2 {data}/amber_q/
   amber_3 {data}/amber_x/
   amber_4 {data}/amber_u/
   spce    {data}/solvents/spce.rst
   charmm_s {data}/charmm_s/
   charmm_x {data}/charmm_x/
""".format(data=share_path)
            with open(".nwchemrc", 'w') as f:
                f.write(nwchemrc)
            install(".nwchemrc", share_path)
