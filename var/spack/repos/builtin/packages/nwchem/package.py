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
import sys
import os


class Nwchem(Package):
    """High-performance computational chemistry software"""

    homepage = "http://www.nwchem-sw.org"
    url      = "http://www.nwchem-sw.org/images/Nwchem-6.6.revision27746-src.2015-10-20.tar.gz"

    tags = ['ecp', 'ecp-apps']

    version('6.8', '50b18116319f4c15d1cb7eaa1b433006',
            url='https://github.com/nwchemgit/nwchem/archive/v6.8-release.tar.gz')
    version('6.6', 'c581001c004ea5e5dfacb783385825e3',
            url='http://www.nwchem-sw.org/images/Nwchem-6.6.revision27746-src.2015-10-20.tar.gz')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('scalapack')

    depends_on('python@2.7:2.8', type=('build', 'link', 'run'))

    # first hash is sha256 of the patch (required for URL patches),
    # second is sha256 for the archive.
    # patches for 6.6-27746:
    urls_for_patches = {
        '@6.6': [
            ('http://www.nwchem-sw.org/images/Tddft_mxvec20.patch.gz',    'ae04d4754c25fc324329dab085d4cc64148c94118ee702a7e14fce6152b4a0c5', 'cdfa8a5ae7d6ee09999407573b171beb91e37e1558a3bfb2d651982a85f0bc8f'),
            ('http://www.nwchem-sw.org/images/Tools_lib64.patch.gz',      'ef2eadef89c055c4651ea807079577bd90e1bc99ef6c89f112f1f0e7560ec9b4', '76b8d3e1b77829b683234c8307fde55bc9249b87410914b605a76586c8f32dae'),
            ('http://www.nwchem-sw.org/images/Config_libs66.patch.gz',    '56f9c4bab362d82fb30d97564469e77819985a38e15ccaf04f647402c1ee248e', 'aa17f03cbb22ad7d883e799e0fddad1b5957f5f30b09f14a1a2caeeb9663cc07'),
            ('http://www.nwchem-sw.org/images/Cosmo_meminit.patch.gz',    'f05f09ca235ad222fe47d880bfd05a1b88d0148b990ca8c7437fa231924be04b', '569c5ee528f3922ee60ca831eb20ec6591633a36f80efa76cbbe41cabeb9b624'),
            ('http://www.nwchem-sw.org/images/Sym_abelian.patch.gz',      'e3470fb5786ab30bf2eda3bb4acc1e4c48fb5e640a09554abecf7d22b315c8fd', 'aa693e645a98dbafbb990e26145d65b100d6075254933f36326cf00bac3c29e0'),
            ('http://www.nwchem-sw.org/images/Xccvs98.patch.gz',          '75540e0436c12e193ed0b644cff41f5036d78c101f14141846083f03ad157afa', '1c0b0f1293e3b9b05e9e51e7d5b99977ccf1edb4b072872c8316452f6cea6f13'),
            ('http://www.nwchem-sw.org/images/Dplot_tolrho.patch.gz',     '8c30f92730d15f923ec8a623e3b311291eb2ba8b9d5a9884716db69a18d14f24', '2ebb1a5575c44eef4139da91f0e1e60057b2eccdba7f57a8fb577e840c326cbb'),
            ('http://www.nwchem-sw.org/images/Driver_smalleig.patch.gz',  'a040df6f1d807402ce552ba6d35c9610d5efea7a9d6342bbfbf03c8d380a4058', 'dd65bfbae6b472b94c8ee81d74f6c3ece37c8fc8766ff7a3551d8005d44815b8'),
            ('http://www.nwchem-sw.org/images/Ga_argv.patch.gz',          '6fcd3920978ab95083483d5ed538cd9a6f2a80c2cafa0c5c7450fa5621f0a314', '8a78cb2af14314b92be9d241b801e9b9fed5527b9cb47a083134c7becdfa7cf1'),
            ('http://www.nwchem-sw.org/images/Raman_displ.patch.gz',      'ca4312cd3ed1ceacdc3a7d258bb05b7824c393bf44f44c28a789ebeb29a8dba4', '6a16f0f589a5cbb8d316f68bd2e6a0d46cd47f1c699a4b256a3973130061f6c3'),
            ('http://www.nwchem-sw.org/images/Ga_defs.patch.gz',          'f8ac827fbc11f7d2a9d8ec840c6f79d4759ef782bd4d291f2e88ec81b1b230aa', 'c6f1a48338d196e1db22bcfc6087e2b2e6eea50a34d3a2b2d3e90cccf43742a9'),
            ('http://www.nwchem-sw.org/images/Zgesvd.patch.gz',           'c333a94ceb2c35a490f24b007485ac6e334e153b03cfc1d093b6037221a03517', '4af592c047dc3e0bc4962376ae2c6ca868eb7a0b40a347ed9b88e887016ad9ed'),
            ('http://www.nwchem-sw.org/images/Cosmo_dftprint.patch.gz',   '449d59983dc68c23b34e6581370b2fb3d5ea425b05c3182f0973e5b0e1a62651', 'd3b73431a68d6733eb7b669d471e18a83e03fa8e40c48e536fe8edecd99250ff'),
            ('http://www.nwchem-sw.org/images/Txs_gcc6.patch.gz',         '1dab87f23b210e941c765f7dd7cc2bed06d292a2621419dede73f10ba1ca1bcd', '139692215718cd7414896470c0cc8b7817a73ece1e4ca93bf752cf1081a195af'),
            ('http://www.nwchem-sw.org/images/Gcc6_optfix.patch.gz',      '8f8a5f8246bc1e42ef0137049acab4448a2e560339f44308703589adf753c148', '15cff43ab0509e0b0e83c49890032a848d6b7116bd6c8e5678e6c933f2d051ab'),
            ('http://www.nwchem-sw.org/images/Util_gnumakefile.patch.gz', '173e17206a9099c3512b87e3f42441f5b089db82be1d2b306fe2a0070e5c8fad', '5dd82b9bd55583152295c999a0e4d72dd9d5c6ab7aa91117c2aae57a95a14ba1'),
            ('http://www.nwchem-sw.org/images/Util_getppn.patch.gz',      'c4a23592fdcfb1fb6b65bc6c1906ac36f9966eec4899c4329bc8ce12015d2495', '8be418e1f8750778a31056f1fdf2a693fa4a12ea86a531f1ddf6f3620421027e'),
            ('http://www.nwchem-sw.org/images/Gcc6_macs_optfix.patch.gz', 'ff33d5f1ccd33385ffbe6ce7a18ec1506d55652be6e7434dc8065af64c879aaa', 'fade16098a1f54983040cdeb807e4e310425d7f66358807554e08392685a7164'),
            ('http://www.nwchem-sw.org/images/Notdir_fc.patch.gz',        '54c722fa807671d6bf1a056586f0923593319d09c654338e7dd461dcd29ff118', 'a6a233951eb254d8aff5b243ca648def21fa491807a66c442f59c437f040ee69')
        ]
    }
    # Iterate over patches
    for __condition, __urls in urls_for_patches.items():
        for __url, __sha256, __archive_sha256 in __urls:
            patch(__url, when=__condition, level=0, sha256=__sha256, archive_sha256=__archive_sha256)

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
            'PYTHONHOME=%s' % spec['python'].home,
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
        use_32_bit_lin_alg = True

        if use_32_bit_lin_alg:
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
            if use_32_bit_lin_alg:
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
