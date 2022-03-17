# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class QtDeclarative(CMakePackage):
    """Qt Declarative (Quick 2)."""

    url      = "https://github.com/qt/qtdeclarative/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtdeclarative/tags"

    maintainers = ['wdconinc', 'sethrj']

    version('6.2.3', sha256='eda82abfe685a6ab5664e4268954622ccd05cc9ec8fb16eaa453c54900591baf')

    generator = 'Ninja'

    # Changing default to Release for typical use in HPC contexts
    variant('build_type',
            default='Release',
            values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
            description='CMake build type')

    depends_on('cmake@3.16:', type='build')
    depends_on('ninja', type='build')
    depends_on("pkgconfig", type='build')
    depends_on("python", when='@5.7.0:', type='build')

    versions = ['6.2.3']
    for v in versions:
        depends_on('qt-base@' + v, when='@' + v)
        depends_on('qt-shadertools@' + v, when='@' + v)

    def patch(self):
        import os
        import shutil
        vendor_dir = join_path(self.stage.source_path, 'src/3rdparty')
        vendor_deps_to_keep = ['masm']
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)

    def cmake_args(self):
        args = []
        return args
