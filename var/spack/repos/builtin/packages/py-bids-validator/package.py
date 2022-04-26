# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBidsValidator(PythonPackage):
    """Validator for the Brain Imaging Data Structure"""

    homepage = "https://github.com/bids-standard/bids-validator"
    pypi     = "bids-validator/bids-validator-1.7.2.tar.gz"

    version('1.8.9', sha256='01fcb5a8fe6de1280cdfd5b37715103ffa0bafb3c739ca7f5ffc41e46549612e')
    version('1.8.4', sha256='63e7a02c9ddb5505a345e178f4e436b82c35ec0a177d7047b67ea10ea3029a68')
    version('1.7.2', sha256='12398831a3a3a2ed7c67e693cf596610c23dd23e0889bfeae0830bbd1d41e5b9')

    depends_on('py-setuptools', type='build')
