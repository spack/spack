# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleResumableMedia(PythonPackage):
    """Utilities for Google Media Downloads and Resumable Uploads."""

    homepage = "https://github.com/GoogleCloudPlatform/google-resumable-media-python"
    pypi = "google-resumable-media/google-resumable-media-0.3.2.tar.gz"

    version('1.2.0', sha256='ee98b1921e5bda94867a08c864e55b4763d63887664f49ee1c231988f56b9d43')
    version('1.1.0', sha256='dcdab13e95bc534d268f87d5293e482cce5bc86dfce6ca0f2e2e89cbb73ef38c')
    version('1.0.0', sha256='173acc6bade1480a529fa29c6c2717543ae2dc09d42e9461fdb86f39502efcf2')
    version('0.7.1', sha256='57841f5e65fb285c01071f439724745b2549a72eb75e5fd979198eb518608ed0')
    version('0.7.0', sha256='85848d9353770e88562e7d61dae4d3b83999de5a19ba6f466da8eb4b7b18772c')
    version('0.6.0', sha256='2e311edf3d2112d66d634e84e6904dfb432f6de1ae5fd45d36e0876810807e8c')
    version('0.5.1', sha256='97155236971970382b738921f978a6f86a7b5a0b0311703d991e065d3cb55773')
    version('0.5.0', sha256='2a8fd188afe1cbfd5998bf20602f76b0336aa892de88fe842a806b9a3ed78d2a')
    version('0.4.1', sha256='cdeb8fbb3551a665db921023603af2f0d6ac59ad8b48259cb510b8799505775f')
    version('0.4.0', sha256='46ee131e55d16e350cf9dc7de6fc0653b55314e8645e2deb0633394adcd7e9c0')
    version('0.3.3', sha256='49493999cf046b5a02f648e201f0c2fc718c5969c53326b4d2c0693b01bdc8bb')
    version('0.3.2', sha256='3e38923493ca0d7de0ad91c31acfefc393c78586db89364e91cb4f11990e51ba')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
