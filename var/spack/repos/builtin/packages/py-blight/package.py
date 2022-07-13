# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlight(PythonPackage):
    """A catch-all compile-tool wrapper."""

    homepage = "https://github.com/trailofbits/blight"
    pypi     = "blight/blight-0.0.47.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.0.47', sha256='eb4a881adb98e03a0a855b95bfcddb0f4b3ca568b00cb45b571f047ae75c5667')

    variant('dev', default=False, description='Enable dev stuff idk')

    depends_on('python@3.7:', type=('build', 'run'))

    # In process of changing build backend after 0.0.47 release.
    depends_on('py-setuptools', type='build')
  
    depends_on('py-click@7.1:8', type=('build', 'run'), when='@0.0.31:0.0.33,0.0.38:')
    depends_on('py-click@8.0:8', type=('build', 'run'), when='@0.0.34:0.0.37')
    depends_on('py-click@7.1:7', type=('build', 'run'), when='@:0.0.30')
    depends_on('py-typing-extensions', type=('build', 'run'), when='@0.0.9:')
    depends_on('py-pydantic@1.7:1', type=('build', 'run'), when='@0.0.26:')

    depends_on('py-flake8', type=('build', 'run'), when='+dev') 
    depends_on('py-black', type=('build', 'run'), when='+dev')
    # dev variant of blight needed the pyproject variant of isort until isort 5.0.0
    # moved that functionality to the program by default, removing the pyproject variant.
    # blight adjusted for this in 0.0.15. spack has isort versions before 5.0.0, but no
    # pyproject variant, so I'm arbitrarily placing a version requirement of >= 5.0.0 to
    # avoid potential issues, even though blight doesn't specify isort versions.
    depends_on('py-isort@5.0.0:', type=('build', 'run'), when='+dev')
    depends_on('py-pytest', type=('build', 'run'), when='+dev')
    depends_on('py-pytest-cov', type=('build', 'run'), when='+dev')
    depends_on('py-coverage+toml', type=('build', 'run'), when='+dev')
    depends_on('py-twine', type=('build', 'run'), when='+dev')
    depends_on('py-pdoc3', type=('build', 'run'), when='+dev')
    depends_on('py-mypy', type=('build', 'run'), when='@0.0.5:+dev')
