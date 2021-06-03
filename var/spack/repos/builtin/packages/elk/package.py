# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install elk
#
# You can edit this file again by typing:
#
#     spack edit elk
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Elk(MakefilePackage):
    """Elk code is a plane wave dft code aimed at material discovery"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://elk.sourceforge.io/"
    url      = "https://sourceforge.net/projects/elk/files/elk-7.1.14.tgz/download"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('7.1.14', sha256='7c2ff30f4b1d72d5dc116de9d70761f2c206700c69d85dd82a17a5a6374453d2')

    #mpi support is optional, it is possible to use openmp parallelist only
    variant('mpi', default='False')
    depends_on('mpi', when='+mpi')

    #Elk comes with internal blas and lapack. Only supported external 
    #implementations are openblas and mkl, plus unknown type use of BLIS
    # All requires changes in make.inc Add MKL and BLIS support if possible. 
    variant('linal', default='internal'
            , description='linear algebra libraries to use'
            , values=('internal', 'openblas')
            , multi=False
            )
    depends_on('openblas', when='linal=openblas')
    
    #Add MKL FFTW support if possible
    variant('fft', default='fftw'
            , description='fft library to use;'
            , values=('internal','fftw')
            , multi=False
            )
    depends_on('fftw@3:', when='fft=fftw')

    variant('wannier90', default=False
            , description="support for wannier code. requires wannier library"
            )
    depends_on('wannier90', when="+wannier90")
    
    variant('libxc', default=False
            , description="libxc DFT functional library support"
            )
    #Note! libxc changed API around v5, 
    #Linking with older version might not work
    depends_on('libxc@5:', when='+libxc')

#   def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')
