# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenkimModelsV2(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
       reliable, reproducible, and portable. Computer implementations of
       inter-atomic models are archived in OpenKIM, verified for coding
       integrity, and tested by computing their predictions for a variety
       of material properties.  Models conforming to the KIM application
       programming interface (API) work seamlessly with major simulation
       codes that have adopted the KIM API standard.

       This package provides all models archived at openkim.org that are
       compatible with the kim-api-v2 package.
    """
    homepage = "https://openkim.org/"
    url      = "https://s3.openkim.org/archives/collection/OpenKIM-Models-v2-2019-02-21.txz"

    extends('kim-api-v2')

    version('2019-02-21', sha256='3bd30b0cf2bab314755a66eed621a77c72d3f990818d08366874149be39f208e', extension='txz', url='https://s3.openkim.org/archives/collection/OpenKIM-Models-v2-2019-02-21.txz')

    def cmake_args(self):
        args = []
        args.append('-DKIM_API_MODEL_INSTALL_PREFIX={0}/lib/kim-api-v2/models'
                    .format(prefix))
        args.append(('-DKIM_API_MODEL_DRIVER_INSTALL_PREFIX={0}'
                     + '/lib/kim-api-v2/model-drivers').format(prefix))
        return args
