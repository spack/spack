# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UfswmPyenv(BundlePackage):
    """
    Python development environment for the UFS weather model.
    """

    homepage = "https://github.com/NOAA-EMC/GSI"
    git = "https://github.com/NOAA-EMC/global-workflow.git"
    # There is no URL since there is no code to download.

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA']

    version('1.0.0')

    depends_on('py-cython')
    depends_on('py-cftime')
    depends_on('py-h5py')
    depends_on('py-numpy')
    depends_on('py-pandas')
    depends_on('py-python-dateutil')
    depends_on('py-netcdf4')
