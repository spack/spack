# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsPyenv(BundlePackage):
    """
    Python development environment for UFS models.
    """

    homepage = ""
    # There is no URL since there is no code to download.

    maintainers = ["AlexanderRichert-NOAA", "Hang-Lei-NOAA"]

    version("1.0.0")

    depends_on("py-cython")
    depends_on("py-cftime")
    depends_on("py-h5py")
    depends_on("py-numpy")
    depends_on("py-pandas")
    depends_on("py-python-dateutil")
    depends_on("py-netcdf4")
    depends_on("py-jinja2")
    depends_on("py-pyyaml")
    depends_on("py-f90nml")

    # There is no need for install() since there is no code.
