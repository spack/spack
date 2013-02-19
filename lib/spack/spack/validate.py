import tty
from utils import ALLOWED_ARCHIVE_TYPES
from urlparse import urlparse

ALLOWED_SCHEMES    = ["http", "https", "ftp"]

def url(url_string):
    url = urlparse(url_string)
    if url.scheme not in ALLOWED_SCHEMES:
        tty.die("Invalid protocol in URL: '%s'" % url_string)

    if not any(url_string.endswith(t) for t in ALLOWED_ARCHIVE_TYPES):
        tty.die("Invalid file type in URL: '%s'" % url_string)
