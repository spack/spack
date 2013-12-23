import tty
from urlparse import urlparse

from spack.util.compression import allowed_archive

ALLOWED_SCHEMES    = ["http", "https", "ftp"]

def url(url_string):
    url = urlparse(url_string)
    if url.scheme not in ALLOWED_SCHEMES:
        tty.die("Invalid protocol in URL: '%s'" % url_string)

    if not allowed_archive(url_string):
        tty.die("Invalid file type in URL: '%s'" % url_string)
