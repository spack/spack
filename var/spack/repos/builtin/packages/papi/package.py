##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import glob
import os
import sys
from llnl.util.filesystem import fix_darwin_install_name


class Papi(Package):
    """PAPI provides the tool designer and application engineer with a
       consistent interface and methodology for use of the performance
       counter hardware found in most major microprocessors. PAPI
       enables software engineers to see, in near real time, the
       relation between software performance and processor events.  In
       addition Component PAPI provides access to a collection of
       components that expose performance measurement opportunites
       across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"

    url      = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    version('5.5.1', '86a8a6f3d0f34cd83251da3514aae15d')
    version('5.5.0', '5e1244a04ca031d4cc29b46ce3dd05b5')
    version('5.4.3', '3211b5a5bb389fe692370f5cf4cc2412')
    version('5.4.1', '9134a99219c79767a11463a76b0b01a2')
    version('5.3.0', '367961dd0ab426e5ae367c2713924ffb')

    variant('components',
            default='',
            values=('', 'example', 'cuda', 'nvml','infiniband', 
		'infiniband_umad', 'powercap', 'rapl', 'lmsensors'),
            multi=True,
            description='Include optional components')
    depends_on('cuda', when='components=cuda')
    depends_on('cuda', when='components=nvml')
    depends_on('lm-sensors', when='components=lmsensors')

    def install(self, spec, prefix):
        with working_dir("src/components/cuda"):
            if 'components=cuda' in spec:
                configure_args = [
                    "--with-cuda-dir=%s" % spec['cuda'].prefix,
                    "--with-cupti-dir=%s/extras/CUPTI" % spec['cuda'].prefix]
                configure(*configure_args)
        with working_dir("src/components/nvml"):
            if 'components=nvml' in spec:
                configure_args = [
                    "--with-nvml-incdir=%s/include" % spec['cuda'].prefix,
                    "--with-nvml-libdir=%s/lib64/stubs" % spec['cuda'].prefix,
                    "--with-cuda-dir=%s" % spec['cuda'].prefix]
                configure(*configure_args)
        with working_dir("src/components/infiniband_umad"):
            if 'components=infiniband_umad' in spec:
                configure()
        with working_dir("src/components/lmsensors"):
            if 'components=lmsensors' in spec:
                configure_args = [
                    "--with-sensors_incdir=%s/include/sensors" % spec['lm-sensors'].prefix,
                    "--with-sensors_libdir=%s/lib64" % spec['lm-sensors'].prefix]
                configure(*configure_args)
        with working_dir("src"):

            configure_args = ["--prefix=%s" % prefix]

            # PAPI uses MPI if MPI is present; since we don't require
            # an MPI package, we ensure that all attempts to use MPI
            # fail, so that PAPI does not get confused
            configure_args.append('MPICC=:')

            configure_args.append('--with-components={0}'.format(
                ' '.join(spec.variants['components'].value))
            )

            configure(*configure_args)

            # Don't use <malloc.h>
            for level in [".", "*", "*/*"]:
                files = glob.iglob(join_path(level, "*.[ch]"))
                filter_file(r"\<malloc\.h\>", "<stdlib.h>", *files)

            make()
            make("install")

            # The shared library is not installed correctly on Darwin
            if sys.platform == 'darwin':
                os.rename(join_path(prefix.lib, 'libpapi.so'),
                          join_path(prefix.lib, 'libpapi.dylib'))
                fix_darwin_install_name(prefix.lib)
