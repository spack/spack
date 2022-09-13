# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install r-libpressio
#
# You can edit this file again by typing:
#
#     spack edit r-libpressio
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class RLibpressio(RPackage):
    """R package for libpressio"""

    homepage = "https://github.com/robertu94/libpressio-r"
    url      = "https://github.com/robertu94/libpressio-r/archive/0.0.1.tar.gz"

    # notify when the package is updated.
    maintainers = ['robertu94']

    version("1.5.0", sha256="6b0e095610f190aad5dded0dbc6c0783893d4d5e773afc80328fc8c5befeff58")
    version('1.4.1', sha256='fa9d47c84ddeb4edd9c5250067a87cc1bb549b9b1dd71e2501dd39ee4e171c27')
    version('1.3.2', sha256='6afc907aa3663fbb9bfc7c92ca57e15d05ecbec59f94badec24e8da99ac1422f')
    version('1.3', sha256='6ade53d30446de85d2bf6aff0f0a756887f970634b97456aec8b2920a96c0726')
    version('1.2', sha256='e5889abf6aabd14b25b5c11e8ecc42cfe56681b1e4f7ade9c9fc28de213981b4')
    version('1.1', sha256='b86a541e095b6e41b3548f6cd734c1ff50c70edda2806ed66b5205880fbfbb96')
    version('0.0.1', sha256='a508cf3ec1b06c417e0de0e1e4180f3175ead2e4ec23b374425fcf2abfaa1b88')

    variant('third_party', description="include support for 3rd party compressor modules", default=True)

    depends_on('r@3.3.0:', type=('build','run'))
    depends_on('r-rcpp', type=('build', 'link', 'run'))
    depends_on('libpressio+json', type=('build', 'link', 'run'))
    depends_on('libpressio@0.65.0:+json', type=('build', 'link', 'run'), when="@1.2:")
    depends_on('pkgconfig', type=('build'))
    depends_on('libpressio-tools@0.1.4:', type=('build','link', 'run'), when="+third_party")


