# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RInsight(RPackage):
    """Easy Access to Model Information for Various Model Objects.

    A tool to provide an easy, intuitive and consistent access to information
    contained in various R models, like model formulas, model terms,
    information about random effects, data that was used to fit the model or
    data from response variables. 'insight' mainly revolves around two types of
    functions: Functions that find (the names of) information, starting with
    'find_', and functions that get the underlying data, starting with 'get_'.
    The package has a consistent syntax and works with many different model
    objects, where otherwise functions to access these information are
    missing."""

    cran = "insight"

    version('0.16.0', sha256='7944d7a386c99ea06d9d9e2b5f4aeb98fded7ec90b1cb908d03e278480be9e3d')
    version('0.15.0', sha256='d6a148c3e1cfcb3829e2f8950bcbf98f500ee88bebd7e2482f9b085542e93fee')
    version('0.14.1', sha256='0e7761997a46ee33039cdeff1779dbc210de3644e4444c6e893e4ef2f12cc129')

    depends_on('r@3.4:', type=('build', 'run'))
