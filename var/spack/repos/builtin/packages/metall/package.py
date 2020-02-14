# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('develop', branch='develop')

    # Install only header files (no binary files)
    depends_on('boost@1.64: atomic=False chrono=False clanglibcpp=False context=False coroutine=False date_time=False debug=False exception=False fiber=False filesystem=False graph=False icu=False iostreams=False locale=False log=False math=False mpi=False multithreaded=False numpy=False pic=False program_options=False python=False random=False regex=False serialization=False shared=False signals=False singlethreaded=False system=False taggedlayout=False test=False thread=False timer=False versionedlayout=False wave=False', type=('build', 'link'))

    def cmake_args(self):
        args = []
        args.append('-DINSTALL_HEADER_ONLY=ON')
        return args
