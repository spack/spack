# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdfview(Package):
    """HDFView is a visual tool written in Java for browsing
    and editing HDF (HDF5 and HDF4) files."""

    homepage = "https://www.hdfgroup.org/downloads/hdfview/"
    url      = "https://s3.amazonaws.com/hdf-wordpress-1/wp-content/uploads/manual/HDFView/hdfview-3.0.tar.gz"

    version('3.0', sha256='e2a16d3842d8947f3d4f154ee9f48a106c7f445914a9e626a53976d678a0e934')

    depends_on('ant', type='build')
    depends_on('hdf5 +java')
    depends_on('hdf +java -external-xdr +shared')

    def install(self, spec, prefix):
        env['HDF5LIBS'] = spec['hdf5'].prefix
        env['HDFLIBS'] = spec['hdf'].prefix

        ant = which('ant')
        ant('deploy')
        mkdirp(prefix.bin)
        filter_file(
            r'\$dir',
            prefix,
            'build/HDF_Group/HDFView/3.0.0/hdfview.sh'
        )
        install('build/HDF_Group/HDFView/3.0.0/hdfview.sh',
                join_path(prefix.bin, 'hdfview'))
        chmod = which('chmod')
        chmod('+x', join_path(self.prefix.bin, 'hdfview'))
        install_tree('build/HDF_Group/HDFView/3.0.0', prefix)
