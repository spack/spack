import urllib
import llnl.util.tty as tty

from spack import *

class Openssl(Package):
    """The OpenSSL Project is a collaborative effort to develop a
       robust, commercial-grade, full-featured, and Open Source
       toolkit implementing the Secure Sockets Layer (SSL v2/v3) and
       Transport Layer Security (TLS v1) protocols as well as a
       full-strength general purpose cryptography library."""
    homepage = "http://www.openssl.org"
    url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"

    version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
    version('1.0.1r', '1abd905e079542ccae948af37e393d28')
    version('1.0.2d', '38dd619b2e77cbac69b99f52a053d25a')
    version('1.0.2e', '5262bfa25b60ed9de9f28d5d52d77fc5')
    version('1.0.2f', 'b3bf73f507172be9292ea2a8c28b659d')

    depends_on("zlib")
    parallel = False

    def url_for_version(self, version):
        # This URL is computed pinging the place where the latest version is stored. To avoid slowdown
        # due to repeated pinging, we store the URL in a private class attribute to do the job only once per version
        openssl_urls = getattr(Openssl, '_openssl_url', {})
        openssl_url = openssl_urls.get(version, None)
        # Same idea, but just to avoid issuing the same message multiple times
        warnings_given_to_user = getattr(Openssl, '_warnings_given', {})
        if openssl_url is None:
            latest = 'http://www.openssl.org/source/openssl-{version}.tar.gz'
            older = 'http://www.openssl.org/source/old/{version_number}/openssl-{version_full}.tar.gz'
            # Try to use the url where the latest tarballs are stored. If the url does not exist (404), then
            # return the url for older format
            version_number = '.'.join([str(x) for x in version[:-1]])
            older_url = older.format(version_number=version_number, version_full=version)
            latest_url = latest.format(version=version)
            response = urllib.urlopen(latest.format(version=version))
            if response.getcode() == 404:
                openssl_url = older_url
                # Checks if we already warned the user for this particular version of OpenSSL.
                # If not we display a warning message and mark this version
                if not warnings_given_to_user.get(version, False):
                    tty.warn('This installation depends on an old version of OpenSSL, which may have known security issues. ')
                    tty.warn('Consider updating to the latest version of this package.')
                    tty.warn('More details at {homepage}'.format(homepage=Openssl.homepage))
                    warnings_given_to_user[version] = True
            else:
                openssl_url = latest_url
            # Store the computed URL
            openssl_urls[version] = openssl_url
            # Store the updated dictionary of URLS
            Openssl._openssl_url = openssl_urls
            # Store the updated dictionary of warnings
            Openssl._warnings_given = warnings_given_to_user

        return openssl_url

    def install(self, spec, prefix):
        # OpenSSL uses a variable APPS in its Makefile. If it happens to be set
        # in the environment, then this will override what is set in the
        # Makefile, leading to build errors.
        env.pop('APPS', None)
        if spec.satisfies("=darwin-x86_64") or spec.satisfies("=ppc64"):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env['KERNEL_BITS'] = '64'
        config = Executable("./config")
        config("--prefix=%s" % prefix,
               "--openssldir=%s" % join_path(prefix, 'etc', 'openssl'),
               "zlib",
               "no-krb5",
               "shared")
        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r'-arch x86_64', '', 'Makefile')

        make()
        make("install")
