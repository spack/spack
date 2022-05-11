# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RoctracerDevApi(Package):
    """ROC-tracer API. Installs the API header files of the roctracer-dev
       package, mainly to avoid circular dependencies in the ROCm ecosystem.
       For the ROC-tracer library, please check out roctracer-dev."""

    homepage = "https://github.com/ROCm-Developer-Tools/roctracer"
    git      = "https://github.com/ROCm-Developer-Tools/roctracer.git"
    url      = "https://github.com/ROCm-Developer-Tools/roctracer/archive/refs/tags/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.0.2', sha256='5ee46f079e57dfe491678ffa4cdaf5f3b3d179cb3137948e4bcafca99ded47cc')
    version('5.0.0', sha256='a21f4fb093cee4a806d53cbc0645d615d89db12fbde305e9eceee7e4150acdf2')
    version('4.5.2', sha256='7012d18b79736dbe119161aab86f4976b78553ce0b2f4753a9386752d75d5074')
    version('4.5.0', sha256='83dcd8987e129b14da0fe74e24ce8d027333f8fedc9247a402d3683765983296')
    version('4.3.1', sha256='88ada5f256a570792d1326a305663e94cf2c3b0cbd99f7e745326923882dafd2')
    version('4.3.0', sha256='c3d9f408df8d4dc0e9c0026217b8c684f68e775da80b215fecb3cd24419ee6d3')
    version('4.2.0', sha256='62a9c0cb1ba50b1c39a0636c886ac86e75a1a71cbf5fec05801517ceb0e67a37')
    version('4.1.0', sha256='5d93de4e92895b6eb5f9d098f5dbd182d33923bd9b2ab69cf5a1abbf91d70695', deprecated=True)
    version('4.0.0', sha256='f47859a46173228b597c463eda850b870e810534af5efd5f2a746067ef04edee', deprecated=True)
    version('3.10.0', sha256='ac4a1d059fc34377e906071fd0e56f5434a7e0e4ded9db8faf9217a115239dec', deprecated=True)
    version('3.9.0', sha256='0678f9faf45058b16923948c66d77ba2c072283c975d167899caef969169b292', deprecated=True)
    version('3.8.0', sha256='5154a84ce7568cd5dba756e9508c34ae9fc62f4b0b5731f93c2ad68b21537ed1', deprecated=True)
    version('3.7.0', sha256='6fa5b771e990f09c242237ab334b9f01039ec7d54ccde993e719c5d6577d1518', deprecated=True)
    version('3.5.0', sha256='7af5326c9ca695642b4265232ec12864a61fd6b6056aa7c4ecd9e19c817f209e', deprecated=True)

    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        include = join_path(source_directory, 'inc')

        def only_headers(p):
            return (p.endswith('CMakeLists.txt') or
                    p.endswith('RPM') or
                    p.endswith('DEBIAN'))

        mkdirp(prefix.roctracer.inc)
        install_tree(include, prefix.roctracer.inc, ignore=only_headers)
