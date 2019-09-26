# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.io/packages/source/s/scikit-learn/scikit-learn-0.21.2.tar.gz"
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
    version('0.21.2', sha256='0aafc312a55ebf58073151b9308761a5fcfa45b7f7730cea4b1f066f824c72db')
    version('0.21.1', sha256='228d0611e69e5250946f8cd7bbefec75347950f0ca426d0c518db8f06583f660')
    version('0.20.2', sha256='bc5bc7c7ee2572a1edcb51698a6caf11fae554194aaab9a38105d9ec419f29e6')
    version('0.20.0', sha256='97d1d971f8ec257011e64b7d655df68081dd3097322690afa1a71a1d755f8c18')
    version('0.19.1', 'b67143988c108862735a96cf2b1e827a')
    version('0.18.1', '6b0ff1eaa5010043895dd63d1e3c60c9')
    version('0.15.2', 'd9822ad0238e17b382a3c756ea94fe0d')
    version('0.16.1', '363ddda501e3b6b61726aa40b8dbdb7e')
    version('0.17.1', 'a2f8b877e6d99b1ed737144f5a478dfc')
    version('0.13.1', 'acba398e1d46274b8470f40d0926e6a4')

    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('python@2.6:2.8,3.3:', when='@:0.19')
    depends_on('python@2.7:2.8,3.4:', when='@0.20.0:0.20.999')
    depends_on('python@3.5:', when='@0.21:')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'), when='@:0.19')
    depends_on('py-numpy@1.8.2:', type=('build', 'run'), when='@0.20.0:0.20.999')
    depends_on('py-numpy@1.11.0:', type=('build', 'run'), when='@0.21:')
    depends_on('py-scipy@0.9:', type=('build', 'run'), when='@:0.19')
    depends_on('py-scipy@0.13.3:', type=('build', 'run'), when='@0.20.0:0.20.999')
    depends_on('py-scipy@0.17.0:', type=('build', 'run'), when='@0.21:')
    depends_on('py-joblib@0.11:', type=('build', 'run'))
    depends_on('py-cython@0.23:', type='build')
    depends_on('py-cython@0.28.5:', type='build', when='@0.21:')
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

    def setup_environment(self, spack_env, run_env):
        # https://scikit-learn.org/stable/developers/advanced_installation.html#building-from-source
        if self.spec.satisfies('~openmp'):
            spack_env.set('SKLEARN_NO_OPENMP', 'True')
        # https://scikit-learn.org/stable/developers/advanced_installation.html#mac-osx
        elif self.spec.satisfies('@0.21: %clang platform=darwin +openmp'):
            spack_env.append_flags(
                'CPPFLAGS', '-Xpreprocessor -fopenmp')
            spack_env.append_flags(
                'CFLAGS', self.spec['llvm-openmp'].headers.include_flags)
            spack_env.append_flags(
                'CXXFLAGS',
                self.spec['llvm-openmp'].headers.include_flags)
            spack_env.append_flags(
                'LDFLAGS', self.spec['llvm-openmp'].libs.ld_flags)
            spack_env.append_flags(
                'DYLD_LIBRARY_PATH',
                self.spec['llvm-openmp'].libs.directories[0])

            run_env.append_flags(
                'DYLD_LIBRARY_PATH',
                self.spec['llvm-openmp'].libs.directories[0])

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if self.spec.satisfies('@0.21: %clang platform=darwin +openmp'):
            spack_env.append_flags(
                'DYLD_LIBRARY_PATH',
                self.spec['llvm-openmp'].libs.directories[0])

    def install_test(self):
        # https://scikit-learn.org/stable/developers/advanced_installation.html#testing
        with working_dir('spack-test', create=True):
            pytest = which('pytest')
            pytest(join_path(self.prefix, site_packages_dir, 'sklearn'))
