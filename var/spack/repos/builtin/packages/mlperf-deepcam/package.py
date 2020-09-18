# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MlperfDeepcam(Package):
    """PyTorch implementation for the climate segmentation benchmark,
       based on the Exascale Deep Learning for Climate Analytics"""

    homepage = "https://github.com/azrael417/mlperf-deepcam"
    url      = "https://github.com/azrael417/mlperf-deepcam.git"

    version('417', sha256='a2ebf7233001cd92a244c295a53da503ed24ad81af1d244403cfa944a91dbae6')

    tags = ['proxy-app']

    depends_on('python@3:', type=('build', 'run'))

    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-pycuda', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('py-torch+cuda', when='+cuda', type=('build', 'run'))
    depends_on('py-torch~cuda~cudnn~nccl', when='~cuda', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-basemap', type=('build', 'run'))
    depends_on('py-pillow', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pillow', type=('build', 'run'))
    depends_on('py-argparse', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-apex', type=('build', 'run'))

    def install(self, spec, prefix):
        # Mostly  about providing an environment so just copy everything
        install_tree('.', prefix)
