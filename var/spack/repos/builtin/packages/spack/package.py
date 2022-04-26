# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spack(Package):
    """
    Spack is a multi-platform package manager that builds and installs multiple
    versions and configurations of software. It works on Linux, macOS, and many
    supercomputers. Spack is non-destructive: installing a new version of a
    package does not break existing installations, so many configurations of
    the same package can coexist.
    """

    homepage = "https://spack.io/"
    git      = "https://github.com/spack/spack.git"
    url      = "https://github.com/spack/spack/releases/download/v0.16.2/spack-0.16.2.tar.gz"
    maintainers = ['haampie']

    version('develop', branch='develop')
    version('0.17.0', sha256='93df99256a892ceefb153d48e2080c01d18e58e27773da2c2a469063d67cb582')
    version('0.16.3', sha256='26636a2e2cc066184f12651ac6949f978fc041990dba73934960a4c9c1ea383d')
    version('0.16.2', sha256='ed3e5d479732b0ba82489435b4e0f9088571604e789f7ab9bc5ce89030793350')
    version('0.16.1', sha256='8d893036b24d9ee0feee41ac33dd66e4fc68d392918f346f8a7a36a69c567567')
    version('0.16.0', sha256='064b2532c70916c7684d4c7c973416ac32dd2ea15f5c392654c75258bfc8c6c2')

    variant('development_tools', default=True, description='Build development dependencies')

    # Python (with spack python -i ipython support)
    depends_on('python@2.6.0:2.7,3.5:', type='run')
    depends_on('python@2.7.0:2.7,3.5:', type='run', when='@0.18.0:')
    depends_on('py-ipython', type='run')

    # Concretizer
    depends_on('clingo-bootstrap@spack', type='run')

    # Archives
    depends_on('bzip2', type='run')
    depends_on('gzip', type='run')
    depends_on('tar', type='run')
    depends_on('unzip', type='run')
    depends_on('xz', type='run')
    depends_on('zstd +programs', type='run')

    # Build tools
    depends_on('bash', type='run')
    depends_on('file', type='run')
    depends_on('gmake', type='run')
    depends_on('patch', type='run')
    depends_on('ccache', type='run')

    # Fetchers
    depends_on('curl', type='run')
    depends_on('git', type='run')
    depends_on('mercurial', type='run')
    depends_on('subversion', type='run')

    # Modules
    depends_on('tcl', type='run')
    depends_on('lmod', type='run')
    # Spack 0.18 uses lmod's depends_on function, which was introduced in v7.5.12
    depends_on('lmod@7.5.12:', type='run', when='@0.18:')

    # Buildcache
    # We just need the 'strings' executable, we don't want to install
    # binutil's linkers.
    depends_on('binutils~plugins~gold~libiberty~nls~headers~lto~ld~gas~interwork', type='run')
    depends_on('gnupg', type='run')
    depends_on('patchelf', type='run', when='platform=linux')
    depends_on('patchelf', type='run', when='platform=cray')
    depends_on('py-boto3', type='run')

    # See https://github.com/spack/spack/pull/24686
    # and #25595, #25726, #25853, #25923, #25924 upstream in python/cpython
    with when('@:0.16.2'):
        conflicts('^python@3.10:')
        conflicts('^python@3.9.6:3.9')
        conflicts('^python@3.8.11:3.8')
        conflicts('^python@3.7.11:3.7')
        conflicts('^python@3.6.14:3.6')

    # https://bugs.python.org/issue45235#msg406121
    # To be fixed in 3.9.9, no other releases are affected
    conflicts('^python@3.9.8', when='@:0.17.0')

    # Development tools
    with when('+development_tools'):
        depends_on('py-isort@4.3.5:', type='run')
        depends_on('py-mypy@0.900:', type='run')
        depends_on('py-black', type='run')
        depends_on('py-flake8', type='run')
        depends_on('py-sphinx@3.4:4.1.1,4.1.3:', type='run')
        depends_on('py-sphinxcontrib-programoutput', type='run')
        depends_on('py-sphinx-rtd-theme', type='run')
        depends_on('graphviz', type='run')

    def setup_run_environment(self, env):
        env.set('SPACK_PYTHON', self.spec['python'].command.path)

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, self.prefix)
