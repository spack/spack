# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAntspyx(PythonPackage):
    """Advanced Normalization Tools in Python."""

    homepage = "https://pypi.org/project/antspyx/"
    url = "https://github.com/ANTsX/ANTsPy/archive/refs/tags/v0.2.7.tar.gz"

    version('0.2.7', sha256='495868dcb975486203cd1ce901c803e4b5d71fad5ad5c2525612de8e030f6a34')
    version('0.2.4', sha256='357d9f93fdac8ca76f660d23f97239a5949284664866f8ba254b912afa953e55')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('cmake', type='build')
    depends_on('itk+review+antspy')
    depends_on('googletest')  # from ITK, somehow does not get passed through

    depends_on('py-pandas', type=('run'))
    depends_on('py-numpy', type=('run'))
    depends_on('py-scipy', type=('run'))
    depends_on('py-scikit-image', type=('run'))
    depends_on('py-scikit-learn', type=('run'))
    depends_on('py-statsmodels', type=('run'))
    depends_on('py-webcolors', type=('run'))
    depends_on('py-matplotlib', type=('run'))
    depends_on('py-pyyaml', type=('run'))
    depends_on('py-chart-studio', type=('run'))
    depends_on('py-pillow', type=('run'))
    depends_on('py-nibabel', type=('run'))

    patch('setup-purge-sklearn.diff')
    patch('fix-itk-gtest.diff')
    patch('submodule-imposter.diff', when='@0.2.4')

    patch('https://github.com/ANTsX/ANTsPy/commit/e0bec4569540f740640876d8195eb63a61ce6504.patch',
          sha256='535e1ea5463994f7d34f9df3ea137c59cfe8f10e44321bba7f386d9fb9c56b6e',
          when='@0.2.4')

    resource(
        name='submodule-imposter-pybind11',
        git='https://github.com/stnava/pybind11/',
        destination='ants/lib',
        when='@0.2.4'
    )

    resource(
        name='submodule-imposter-antscore',
        git='https://github.com/ANTsX/ANTs.git',
        commit='4528978446c73ed09927ea5ae1721b280d534dc0',
        destination='ants/lib',
        when='@0.2.4'
    )

    def patch(self):
        if self.spec.satisfies('@0.2.4'):
            for fn in (
                'ants/lib/ANTs/Utilities/itkLabeledPointSetFileReader.hxx',
                'ants/lib/ANTs/Utilities/itkGeneralToBSplineDisplacementFieldFilter.hxx'
            ):
                filter_file(r'(itkDebugMacro\(.*\))$', r'\1;', fn)

    def setup_build_environment(self, env):
        env.set('ITK_DIR', self.spec['itk'].prefix)
