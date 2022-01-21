# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNibetaseries(PythonPackage):
    """BetaSeries Correlations implemented in Nipype."""

    homepage = "https://github.com/HBClab/NiBetaSeries"
    pypi = "nibetaseries/nibetaseries-0.6.0.tar.gz"
    git = "https://github.com/HBClab/NiBetaSeries.git"

    version('master', branch='master')
    version('0.6.0', sha256='afddea1bf9b9de4ae446a5d9d2a56bdc88a5a9588bec5ecd3c8ac978fe416515')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools@40.8:', type='build')
    depends_on('py-cython', type='build')

    with when('@master'):
        depends_on('py-nipype@1.5.1:', type=('build', 'run'))
        depends_on('py-pybids@0.11.1:', type=('build', 'run'))
        depends_on('py-nibabel@3:', type=('build', 'run'))
        depends_on('py-nistats@0.0.1b2', type=('build', 'run'))
        depends_on('py-niworkflows@1.3.1:1.3', type=('build', 'run'))
        depends_on('py-nilearn', type=('build', 'run'))
        depends_on('py-pandas', type=('build', 'run'))
        depends_on('py-numpy', type=('build', 'run'))
        depends_on('py-duecredit', type=('build', 'run'))
        depends_on('py-scikit-learn@0.22.0:0.22', type=('build', 'run'))
        depends_on('py-matplotlib', type=('build', 'run'))
        depends_on('py-mne', type=('build', 'run'))
        # pypiwin32; platform_system=="Windows"

    with when('@:0.6'):
        depends_on('py-nipype@1.4.2:1.4', type=('build', 'run'))
        depends_on('py-pybids@0.9.3:0.9', type=('build', 'run'))
        depends_on('py-nibabel@2.4.0:2.4', type=('build', 'run'))
        depends_on('py-nistats@0.0.1b2', type=('build', 'run'))
        depends_on('py-nilearn@0.4.2:0.4', type=('build', 'run'))
        depends_on('py-pandas@0.24.0:0.24', type=('build', 'run'))
        depends_on('py-numpy', type=('build', 'run'))
        depends_on('py-niworkflows@1.0.2:1.0', type=('build', 'run'))
        depends_on('py-duecredit@0.6.4:0.6', type=('build', 'run'))
        depends_on('py-scikit-learn@0.19.2:0.19', type=('build', 'run'))
        depends_on('py-matplotlib@2.2.4:2.2', type=('build', 'run'))
        depends_on('py-mne@0.18.1:0.18', type=('build', 'run'))
        # pypiwin32; platform_system=="Windows"

    @run_after('install')
    def patch_bin(self):
        # pkg_resources fails to find the dependencies, resulting in errors
        # like: pkg_resources.DistributionNotFound: The 'sklearn' distribution
        # was not found and is required by nilearn
        filter_file("__requires__ = 'nibetaseries==0.post1+gaa7d2ea'", "",
                    join_path(self.prefix.bin, 'nibs'), string=True)
