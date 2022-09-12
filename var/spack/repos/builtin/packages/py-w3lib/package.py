
from spack.package import *


class PyW3lib(PythonPackage):
    """This is a Python library of web-related functions, such as:
        - remove comments, or tags from HTML snippets
        - extract base url from HTML snippets
        - translate entites on HTML strings
        - convert raw HTTP headers to dicts and vice-versa
        - construct HTTP auth header
        - converting HTML pages to unicode
        - sanitize urls (like browsers do)
        - extract arguments from urls
    """

    homepage = "https://github.com/scrapy/w3lib"
    url = "https://github.com/scrapy/w3lib/archive/refs/tags/v1.22.0.tar.gz"

    maintainers = ["frerappa"]

    version("1.22.0", sha256="d388f06a11008c68f96c95224e224691e5ce9c13733d89bc85a550c448f83c97")
