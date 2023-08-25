# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetcdf4(PythonPackage):
    """Python interface to the netCDF Library."""

    homepage = "https://github.com/Unidata/netcdf4-python"
    pypi = "netCDF4/netCDF4-1.2.7.tar.gz"

    maintainers("skosukhin")

    version("1.6.2", sha256="0382b02ff6a288419f6ffec85dec40f451f41b8755547154c575ddd9f0f4ae53")
    version("1.5.8", sha256="ca3d468f4812c0999df86e3f428851fb0c17ac34ce0827115c246b0b690e4e84")
    version("1.5.3", sha256="2a3ca855848f4bbf07fac366da77a681fcead18c0a8813d91d46302f562dc3be")
    version("1.4.2", sha256="b934af350459cf9041bcdf5472e2aa56ed7321c018d918e9f325ec9a1f9d1a30")

    variant("mpi", default=True, description="Parallel IO support")

    depends_on("python@2.6:2.7,3.3:", when="@1.2.8:1.5.1", type=("build", "link", "run"))
    depends_on("python@2.7,3.5:", when="@1.5.2:1.5.3", type=("build", "link", "run"))
    depends_on("python@3.6:", when="@1.5.4:", type=("build", "link", "run"))

    depends_on("py-setuptools@18:", when="@1.4.2:1.5.8", type="build")
    depends_on("py-setuptools@41.2:", when="@1.6.2:", type="build")
    depends_on("py-cython@0.19:", type="build")

    depends_on("py-numpy@1.7:", type=("build", "link", "run"))
    depends_on("py-numpy@1.9:", when="@1.5.4:", type=("build", "link", "run"))
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-mpi4py", when="+mpi", type=("build", "run"))

    depends_on("netcdf-c", when="-mpi")
    depends_on("netcdf-c+mpi", when="+mpi")

    depends_on("hdf5@1.8.0:+hl", when="-mpi")
    depends_on("hdf5@1.8.0:+hl+mpi", when="+mpi")

    # The installation script tries to find hdf5 using pkg-config. However, the
    # version of hdf5 installed with Spack does not have pkg-config files.
    # Therefore, if pkg-config finds hdf5.pc at all (e.g. provided by
    # Ubuntu/Debian package manager), it is definitely not what we need. The
    # following patch disables the usage of pkg-config at all.
    patch("disable_pkgconf.patch")

    def setup_build_environment(self, env):
        """Ensure installed netcdf and hdf5 libraries are used"""
        # Explicitly set these variables so setup.py won't erroneously pick up
        # system versions
        # See: http://unidata.github.io/netcdf4-python
        env.set("USE_SETUPCFG", "0")
        env.set("USE_NCCONFIG", "1")
        env.set("HDF5_DIR", self.spec["hdf5"].prefix)
        env.set("HDF5_INCDIR", self.spec["hdf5"].prefix.include)
        env.set("HDF5_LIBDIR", self.spec["hdf5"].prefix.lib)
        env.set("NETCDF4_DIR", self.spec["netcdf-c"].prefix)
        env.set("NETCDF4_INCDIR", self.spec["netcdf-c"].prefix.include)
        env.set("NETCDF4_LIBDIR", self.spec["netcdf-c"].prefix.lib)
