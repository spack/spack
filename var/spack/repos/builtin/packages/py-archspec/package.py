# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class PyArchspec(PythonPackage):
    """A library for detecting, labeling and reasoning about
    microarchitectures.
    """

    homepage = "https://archspec.readthedocs.io/en/latest/"
    pypi = "archspec/archspec-0.1.1.tar.gz"

    maintainers = ['alalazo']

    version('0.1.1', sha256='34bafad493b41208857232e21776216d716de37ab051a6a4a1cc1653f7e26423')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))

    depends_on('py-click@7.1.2:7', type=('build', 'run'))
    depends_on('py-six@1.13.0:1', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-poetry-core@1.0.0:', type='build')

    def patch(self):
        # See https://python-poetry.org/docs/pyproject/#poetry-and-pep-517
        with working_dir(self.build_directory):
            if self.spec.satisfies('@:0.1.3'):
                filter_file("poetry>=0.12", "poetry_core>=1.0.0", 'pyproject.toml')
                filter_file(
                    "poetry.masonry.api", "poetry.core.masonry.api", 'pyproject.toml'
                )
