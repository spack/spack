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
        for lang in ('c', 'f'):
            filename = 'mpi_hello.' + lang
            filepath = os.path.join(self.test_dir, 'data', 'mpi')

            compiler_var = 'MPI%sC' % lang.upper()
            compiler = os.environ[compiler_var]

            exe_name = 'mpi_hello_%s' % lang
            mpirun = os.path.join(self.prefix.bin, 'mpirun')

            compiled = self.run_test(compiler, options=['-o', exe_name])
            if compiled:
                self.run_test(mpirun,
                              options=['-np', '1', exe_name],
                              expected=['Hello world! From rank 1 of 1'])
