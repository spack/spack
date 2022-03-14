# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class ManyVirtualConsumer(Package):
    """PAckage that depends on many virtual packages"""
    url = "http://www.example.com/"
    url = "http://www.example.com/2.0.tar.gz"

    version('1.0', 'abcdef1234567890abcdef1234567890')

    depends_on('mpi')
    depends_on('lapack')

    # This directive is an example of imposing a constraint on a
    # dependency is that dependency is in the DAG. This pattern
    # is mainly used with virtual providers.
    depends_on('low-priority-provider@1.0', when='^low-priority-provider')
