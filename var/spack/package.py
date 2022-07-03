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
#     spack install py-phylophlan
#
# You can edit this file again by typing:
#
#     spack edit py-phylophlan
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPhylophlan(PythonPackage):
    """PhyloPhlAn 3.0 is an integrated pipeline for large-scale phylogenetic profiling of genomes and metagenomes."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/biobakery/phylophlan"
    url      = "https://github.com/biobakery/phylophlan/archive/refs/tags/3.0.2.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('3.0.2', sha256='c342116662bbfbb49f0665291fc7c0be5a0d04a02a7be2da81de0322eb2256b4')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))
    depends_on('python@3:')
    depends_on('py-numpy@1.12.1:')
    depends_on('py-biopython@1.70:')
    depends_on('py-dendropy@4.2.0:')
    depends_on('muscle')
    depends_on('blast-plus')
    depends_on('diamond')


    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
