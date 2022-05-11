# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RGenomeinfodbdata(RPackage):
    """for mapping between NCBI taxonomy ID and species. Used by functions
       in the GenomeInfoDb package."""

    bioc = "GenomeInfoDbData"
    url = "https://bioconductor.org/packages/release/data/annotation/src/contrib/GenomeInfoDbData_0.99.0.tar.gz"

    version('1.2.7',
            url='https://bioconductor.org/packages/3.14/data/annotation/src/contrib/GenomeInfoDbData_1.2.7.tar.gz',
            sha256='217cbad0dd3ed8f0da6b21c7d35df5737bcbd21e317ca71d2fb6ec4c316b1987')
    version('1.2.1',
            url='https://bioconductor.org/packages/3.9/data/annotation/src/contrib/GenomeInfoDbData_1.2.1.tar.gz',
            sha256='75e6d683a29b8baeec66ba5194aa59a6aa69b04fae5a9c718a105c155fb41711')
    version('1.1.0',
            url='https://bioconductor.org/packages/3.7/data/annotation/src/contrib/GenomeInfoDbData_1.1.0.tar.gz',
            sha256='6efdca22839c90d455843bdab7c0ecb5d48e3b6c2f7b4882d3210a6bbad4304c')
    version('0.99.0', sha256='457049804bbd70f218c1c84067a23e83bdecb7304a3e4d8b697fee0b16dc1888')

    depends_on('r@3.5:', type=('build', 'run'), when='@1.2.1:')
    depends_on('r@3.3:', type=('build', 'run'), when='@0.99.0:1.1.0')
