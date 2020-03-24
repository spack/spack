# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.io/packages/source/s/scikit-learn/scikit-learn-0.22.tar.gz"
    git      = "https://github.com/scikit-learn/scikit-learn.git"

    maintainers = ['adamjstewart']
    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'sklearn', 'sklearn.tree', 'sklearn.metrics', 'sklearn.ensemble',
        'sklearn.experimental', 'sklearn.cluster',
        'sklearn.feature_extraction', 'sklearn.__check_build',
        'sklearn.semi_supervised', 'sklearn.gaussian_process',
        'sklearn.compose', 'sklearn.datasets', 'sklearn.externals',
        'sklearn.linear_model', 'sklearn.impute', 'sklearn.utils',
        'sklearn.covariance', 'sklearn.neural_network',
        'sklearn.feature_selection', 'sklearn.inspection', 'sklearn.svm',
        'sklearn.manifold', 'sklearn.mixture', 'sklearn.preprocessing',
        'sklearn.model_selection', 'sklearn._build_utils',
        'sklearn.decomposition', 'sklearn.cross_decomposition',
        'sklearn.neighbors', 'sklearn.metrics.cluster',
        'sklearn.ensemble._hist_gradient_boosting'
    ]

    version('master', branch='master')
    version('0.22.1', sha256='51ee25330fc244107588545c70e2f3570cfc4017cff09eed69d6e1d82a212b7d')
    version('0.22',   sha256='314abf60c073c48a1e95feaae9f3ca47a2139bd77cebb5b877c23a45c9e03012')
    version('0.21.3', sha256='eb9b8ebf59eddd8b96366428238ab27d05a19e89c5516ce294abc35cea75d003')
    version('0.21.2', sha256='0aafc312a55ebf58073151b9308761a5fcfa45b7f7730cea4b1f066f824c72db')
    version('0.21.1', sha256='228d0611e69e5250946f8cd7bbefec75347950f0ca426d0c518db8f06583f660')
    version('0.20.3', sha256='c503802a81de18b8b4d40d069f5e363795ee44b1605f38bc104160ca3bfe2c41')
    version('0.20.2', sha256='bc5bc7c7ee2572a1edcb51698a6caf11fae554194aaab9a38105d9ec419f29e6')
    version('0.20.0', sha256='97d1d971f8ec257011e64b7d655df68081dd3097322690afa1a71a1d755f8c18')
    version('0.19.1', sha256='5ca0ad32ee04abe0d4ba02c8d89d501b4e5e0304bdf4d45c2e9875a735b323a0')
    version('0.18.1', sha256='1eddfc27bb37597a5d514de1299981758e660e0af56981c0bfdf462c9568a60c')
    version('0.15.2', sha256='1a8a881f6f13edc0ac58931ce21f899eb7920af50aa08802413d1239e2aa5fa6')
    version('0.16.1', sha256='c0721e295056c95c7002e05726f2bd271a7923e88bdeab34a2b60aac2b0ee6e4')
    version('0.17.1', sha256='9f4cf58e57d81783289fc503caaed1f210bab49b7a6f680bf3c04b1e0a96e5f0')
    version('0.13.1', sha256='a6e4759a779ba792435d096c882a0d66ee29d369755c09209f1a4e50877bdc94')

    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('python@2.6:2.8,3.3:', when='@:0.19', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.20.0:0.20.999', type=('build', 'run'))
    depends_on('python@3.5:', when='@0.21:', type=('build', 'run'))
    depends_on('py-numpy@1.6.1:', when='@:0.19', type=('build', 'run'))
    depends_on('py-numpy@1.8.2:', when='@0.20.0:0.20.999', type=('build', 'run'))
    depends_on('py-numpy@1.11.0:', when='@0.21:', type=('build', 'run'))
    depends_on('py-scipy@0.9:', when='@:0.19', type=('build', 'run'))
    depends_on('py-scipy@0.13.3:', when='@0.20.0:0.20.999', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', when='@0.21:', type=('build', 'run'))
    depends_on('py-joblib@0.11:', type=('build', 'run'))
    depends_on('py-cython@0.23:', type='build')
    depends_on('py-cython@0.28.5:', when='@0.21:', type='build')
    depends_on('py-pytest@3.3.0:', type='test')
    depends_on('py-pandas', type='test')
    depends_on('py-setuptools', type='build')
    # Technically not correct, but currently no way to check if we
    # are using Apple Clang or not.
    depends_on('llvm-openmp', when='@0.21: %clang platform=darwin +openmp')

    # Release tarballs are already cythonized. If you wanted to build a release
    # version without OpenMP support, you would need to delete all .c files
    # that include omp.h, as well as PKG-INFO.
    # See https://github.com/scikit-learn/scikit-learn/issues/14332
    conflicts('~openmp', when='@:999', msg='Only master supports ~openmp')

    def setup_build_environment(self, env):
        # https://scikit-learn.org/stable/developers/advanced_installation.html#building-from-source
        if self.spec.satisfies('~openmp'):
            env.set('SKLEARN_NO_OPENMP', 'True')
        # https://scikit-learn.org/stable/developers/advanced_installation.html#mac-osx
        elif self.spec.satisfies('@0.21: %clang platform=darwin +openmp'):
            env.append_flags(
                'CPPFLAGS', self.compiler.openmp_flag)
            env.append_flags(
                'CFLAGS', self.spec['llvm-openmp'].headers.include_flags)
            env.append_flags(
                'CXXFLAGS', self.spec['llvm-openmp'].headers.include_flags)
            env.append_flags(
                'LDFLAGS', self.spec['llvm-openmp'].libs.ld_flags)

    def install_test(self):
        # https://scikit-learn.org/stable/developers/advanced_installation.html#testing
        with working_dir('spack-test', create=True):
            pytest = which('pytest')
            pytest(join_path(self.prefix, site_packages_dir, 'sklearn'))
