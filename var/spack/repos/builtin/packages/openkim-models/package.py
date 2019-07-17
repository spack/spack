# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenkimModels(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
       reliable, reproducible, and portable. Computer implementations of
       inter-atomic models are archived in OpenKIM, verified for coding
       integrity, and tested by computing their predictions for a variety
       of material properties.  Models conforming to the KIM application
       programming interface (API) work seamlessly with major simulation
       codes that have adopted the KIM API standard.

       This package provides all models archived at openkim.org that are
       compatible with the kim-api package.
    """
    homepage = "https://openkim.org/"
    url      = "https://s3.openkim.org/archives/collection/openkim-models-2019-03-29.txz"

    extends('kim-api')

    version('2019-03-29', sha256='053dda2023fe4bb6d7c1d66530c758c4e633bbf1f1be17b6b075b276fe8874f6')

    def cmake_args(self):
        args = []
        args.append(('-DKIM_API_MODEL_DRIVER_INSTALL_PREFIX={0}'
                     + '/lib/kim-api/model-drivers').format(prefix))
        args.append('-DKIM_API_MODEL_INSTALL_PREFIX={0}/lib/kim-api/models'
                    .format(prefix))
        args.append('-DKIM_API_SIMULATOR_MODEL_INSTALL_PREFIX={0}/lib/'
                    'kim-api/simulator-models'
                    .format(prefix))
        return args
