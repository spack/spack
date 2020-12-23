# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

def setup_libtirpc_build_environment(spec, env):
    """The `libtirpc` package places its headers differently than some of its consumers expect.

    The `libtirpc` package provides the virtual dependency `rpc`.
    """
    if 'libtirpc' in spec:
        libtirpc = spec['libtirpc']
        env.prepend_path('CPATH', libtirpc.prefix.include.tirpc)
        env.append_flags('LDFLAGS', '-ltirpc')
