# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KimApiV2(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
       reliable, reproducible, and portable. Computer implementations of
       inter-atomic models are archived in OpenKIM, verified for coding
       integrity, and tested by computing their predictions for a variety
       of material properties.  Models conforming to the KIM application
       programming interface (API) work seamlessly with major simulation
       codes that have adopted the KIM API standard.

       This package provides the kim-api-v2 library and supporting
       utilities.  It also provides a small set of example models.

       To obtain all models archived at https://openkim.org that are
       compatible with the kim-api-v2 package, install and activate the
       openkim-models-v2 pacakge too.
    """
    extendable = True
    homepage = "https://openkim.org/"
    url      = "https://s3.openkim.org/kim-api/kim-api-v2-2.0.1.txz"
    git      = "https://github.com/openkim/kim-api.git"

    version('develop', branch='devel')
    version('2.0.1', sha256="6b54a9c4bc34c669b8ef00b9be4bbdce6fca2bb813dc1fe7697d618f267860d0", extension='txz', url='https://s3.openkim.org/kim-api/kim-api-v2-2.0.1.txz')
