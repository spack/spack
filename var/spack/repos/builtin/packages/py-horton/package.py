# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class PyHorton(PythonPackage):
    """HORTON: Helpful Open-source Research TOol for N-fermion systems. Copyright (C) 2011-2016 The HORTON Development Team
       For more information, visit HORTON's website: http://theochem.github.com/horton/latest
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://theochem.github.io/horton"
    url      = "https://github.com/theochem/horton/releases/download/2.1.1/horton-2.1.1.tar.gz"

    maintainers = ['frobnitzem']

    version('2.1.1', sha256='4b3f87920d881030ba80f097326a744de2cfee5316aa4499cc9a6501f64b5060')

    depends_on('python@2.7:2.99', type=('build', 'run'))
    # note: The py-setuptools dep should be type='build', but build_systems/python.py
    # adds "args += ['--single-version-externally-managed', '--root=/']"
    # This conflicts with the present setuptools version (required by python2).
    # So, it's hacked to run-dep here.
    depends_on('py-setuptools@:44.1.0',   type='run')
    depends_on('py-nose@1.1.2:',        type=('build'))
    depends_on('py-numpy@1.9.1:1.16', type=('build', 'run'))
    depends_on('py-scipy@0.11.0:1.2.3', type=('build', 'run'))
    depends_on('py-cython@0.24.1:', type=('build', 'run'))
    depends_on('py-h5py@2.2.1:2.10.0', type=('build', 'run'))
    depends_on('py-matplotlib@1.0:2.2.5', type=('build', 'run'))
    depends_on('libxc@2.2.2:',  type=('build', 'run'))
    depends_on('libint@2.0.3: tune=cp2k-lmax-7', type=('build', 'run'))
    depends_on('curl@7.0:',     type=('build', 'run'))

    patch("cext.patch")

    @run_before('build')
    def gen_setup_cfg(self):
        spec = self.spec
        numpy = self.spec['py-numpy']
        print("TODO: use numpy to create initial setup.cfg")
        # print(dir(numpy.package))

        self.set_blas_lapack(numpy.package)

        def write_library_dirs(f, dirs):
            f.write('library_dirs = {0}\n'.format(dirs))
            if not ((platform.system() == 'Darwin') and
                    (Version(platform.mac_ver()[0]).up_to(2) == Version(
                        '10.12'))):
                # f.write('rpath = {0}\n'.format(dirs))
                f.write('extra_link_args = -Wl,-rpath={0}\n'.format(dirs))

        deps = {'libxc':  {'name': 'libxc', 'libraries': 'xc'},
                'libint': {'name': 'libint2', 'libraries': 'int2'}}
        for key, val in deps.items():
            # val['libraries'] = ','.join(spec[key].libs.names)
            val['library_dirs'] = spec[key].prefix + '/lib'
            val['include_dirs'] = spec[key].prefix + '/include'

        # Tell numpy where to find BLAS/LAPACK libraries
        with open('setup.cfg', 'w') as f:
            with open('site.cfg') as site:
                for line in site:
                    s = line.strip()
                    if s[0] == '[' and s[-1] == ']':
                        f.write('[blas]\n')
                    else:
                        f.write(line)
            for key, val in deps.items():
                f.write('[{0}]\n'.format(val['name']))
                f.write('libraries = {0}\n'.format(val['libraries']))
                write_library_dirs(f, val['library_dirs'])
                f.write('include_dirs = {0}\n'.format(val['include_dirs']))
                if key == 'libint':
                    f.write('extra_compile_args = -DLIBINT2_MAX_AM_ERI=7')

    # copied from py-numpy
    def set_blas_lapack(other, self):
        # https://numpy.org/devdocs/user/building.html
        # https://github.com/numpy/numpy/blob/master/site.cfg.example

        # Skip if no BLAS/LAPACK requested
        spec = self.spec
        if '+blas' not in spec and '+lapack' not in spec:
            return

        def write_library_dirs(f, dirs):
            f.write('library_dirs = {0}\n'.format(dirs))
            if not ((platform.system() == 'Darwin') and
                    (Version(platform.mac_ver()[0]).up_to(2) == Version(
                        '10.12'))):
                f.write('rpath = {0}\n'.format(dirs))

        blas_libs = LibraryList([])
        blas_headers = HeaderList([])
        if '+blas' in spec:
            blas_libs = spec['blas'].libs
            blas_headers = spec['blas'].headers

        lapack_libs = LibraryList([])
        lapack_headers = HeaderList([])
        if '+lapack' in spec:
            lapack_libs = spec['lapack'].libs
            lapack_headers = spec['lapack'].headers

        lapackblas_libs = lapack_libs + blas_libs
        lapackblas_headers = lapack_headers + blas_headers

        blas_lib_names   = ','.join(blas_libs.names)
        blas_lib_dirs    = ':'.join(blas_libs.directories)
        blas_header_dirs = ':'.join(blas_headers.directories)

        lapack_lib_names   = ','.join(lapack_libs.names)
        lapack_lib_dirs    = ':'.join(lapack_libs.directories)
        lapack_header_dirs = ':'.join(lapack_headers.directories)

        lapackblas_lib_names   = ','.join(lapackblas_libs.names)
        lapackblas_lib_dirs    = ':'.join(lapackblas_libs.directories)
        lapackblas_header_dirs = ':'.join(lapackblas_headers.directories)

        # Tell numpy where to find BLAS/LAPACK libraries
        with open('site.cfg', 'w') as f:
            if '^intel-mkl' in spec or '^intel-parallel-studio+mkl' in spec:
                f.write('[mkl]\n')
                # FIXME: as of @1.11.2, numpy does not work with separately
                # specified threading and interface layers. A workaround is a
                # terribly bad idea to use mkl_rt. In this case Spack will no
                # longer be able to guarantee that one and the same variant of
                # Blas/Lapack (32/64bit, threaded/serial) is used within the
                # DAG. This may lead to a lot of hard-to-debug segmentation
                # faults on user's side. Users may also break working
                # installation by (unconsciously) setting environment variable
                # to switch between different interface and threading layers
                # dynamically. From this perspective it is no different from
                # throwing away RPATH's and using LD_LIBRARY_PATH throughout
                # Spack.
                f.write('libraries = {0}\n'.format('mkl_rt'))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^blis' in spec:
                f.write('[blis]\n')
                f.write('libraries = {0}\n'.format(blas_lib_names))
                write_library_dirs(f, blas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(blas_header_dirs))

            if '^openblas' in spec:
                f.write('[openblas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^libflame' in spec:
                f.write('[flame]\n')
                f.write('libraries = {0}\n'.format(lapack_lib_names))
                write_library_dirs(f, lapack_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapack_header_dirs))

            if '^atlas' in spec:
                f.write('[atlas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^veclibfort' in spec:
                f.write('[accelerate]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)

            if '^netlib-lapack' in spec:
                # netlib requires blas and lapack listed
                # separately so that scipy can find them
                if spec.satisfies('+blas'):
                    f.write('[blas]\n')
                    f.write('libraries = {0}\n'.format(blas_lib_names))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write('include_dirs = {0}\n'.format(blas_header_dirs))
