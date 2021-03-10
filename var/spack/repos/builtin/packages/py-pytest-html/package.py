from spack import *



class PyPytestHtml(PythonPackage):
    """pytest-html is a plugin for pytest that generates a HTML report for test results"""

    homepage = "https://github.com/pytest-dev/pytest-html"
    pypi = "pytest-html/pytest-html-3.1.1.tar.gz"

    version('3.1.1', sha256='3ee1cf319c913d19fe53aeb0bc400e7b0bc2dbeb477553733db1dad12eb75ee3')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
