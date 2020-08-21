# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class Mpi(Package):
    """Virtual package for the Message Passing Interface."""
    homepage = 'https://www.mpi-forum.org/'
    virtual = True

    def test(self):
        mpi_test_data_dir = self.test_dir.data.join('mpi')

        for lang in ('c', 'f'):
            filename = 'mpi_hello.' + lang
            filepath = join_path(mpi_test_data_dir, filename)

            compiler_var = 'MPI%sC' % lang.upper()
            compiler = os.environ[compiler_var]

            exe_name = 'mpi_hello_%s' % lang
            mpirun = join_path(self.prefix.bin, 'mpirun')

            compiled = self.run_test(compiler,
                                     options=['-o', exe_name, filepath])
            if compiled:
                self.run_test(mpirun,
                              options=['-np', '1', exe_name],
                              expected=['Hello world! From rank 1 of 1'])
