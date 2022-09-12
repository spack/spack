from spack.package import *


class PyParsel(PythonPackage):
    """Parsel is a BSD-licensed Python library to extract and remove data from
    HTML and XML using XPath and CSS selectors and regular expressions.
    """

    homepage = "https://parsel.readthedocs.io"
    url = "https://github.com/scrapy/parsel/archive/refs/tags/v1.6.0.tar.gz"

    maintainers = ["frerappa"]

    version("1.6.0", sha256="15546bb637074725e4b2c0d7c579356636251389d9b296520543d835d615e83d")

    depends_on("py-cssselect", type="build")
    depends_on("py-lxml", type="build")
    depends_on("py-six", type="build")
    depends_on("py-w3lib", type="build")
